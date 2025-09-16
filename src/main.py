import json
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QApplication,
    QComboBox,
    QPushButton,
    QDialog,
    QMessageBox,
)
from PySide6.QtCore import Slot, QSettings, QStringListModel
from PySide6.QtGui import QTextCursor

from enum import Enum
import time
import serial.tools.list_ports
import serial.serialutil

from mainwindow_ui import Ui_MainWindow
from settings_dialog import SettingsDialog
from port_settings_tab import save_serial_settings, load_serial_settings
from serial_thread import SerialThread
from serial_port import ReadingMode, SerialPort, RealSerialPort, FakeSerialPort

import pyqtgraph as pg
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class LineEnding(Enum):
    NO_LINE_ENDING = "No Line Ending"
    NEW_LINE = "New Line"
    CARRIAGE_RETURN = "Carriage Return"
    BOTH_NL_AND_CR = "Both NL & CR"


class ThreadControlButtonText(Enum):
    PAUSE_THREAD = "Stop Listening"
    RESUME_THREAD = "Start Listening"


FAKE_PORT_NAME = "fakePort"
MAX_SAMPLES = 50


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.saved_settings = QSettings("kjoskowiak", "SerialViewer")
        self.loaded_settings = load_serial_settings(self.saved_settings)
        # Needed in case the settings file has not been created yet
        save_serial_settings(self.saved_settings, self.loaded_settings)

        # Setup toolbar - qt designer support for toolbar is limited
        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(self.toolbar)

        self.portChoice = QComboBox()
        self.portChoice.setPlaceholderText("Choose serial device")
        self.portChoice.setCurrentText(FAKE_PORT_NAME)
        self.previousPortChoice = FAKE_PORT_NAME
        self.handle_refresh_port_list()
        self.toolbar.addWidget(self.portChoice)

        self.refreshPortList = QPushButton()
        self.refreshPortList.setText("Refresh Ports")
        self.toolbar.addWidget(self.refreshPortList)

        self.threadControlButton = QPushButton()
        self.threadControlButton.setText(ThreadControlButtonText.PAUSE_THREAD.value)
        self.toolbar.addWidget(self.threadControlButton)
        # End setup toolbar

        # Setup plot display
        self.plotData = {"default": [], "t": []}
        self.timeStart = time.monotonic()

        self.curves = {"default": self.plotDisplay.plot()}
        self.curves["default"].setPen((200,200,100))


        # Line ending choice setup
        self.lineEndChoice.setPlaceholderText("New Line")
        self.lineEndChoice.addItems([m.value for m in LineEnding])
        self.lineEndChoice.setCurrentText(LineEnding.NEW_LINE.value)

        # Serial reader thread
        self.serialThread = SerialThread(self.get_serial_port())
        self.serialThread.start()

        # Connecting signals & slots
        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self.handle_settings_action)
        self.refreshPortList.clicked.connect(self.handle_refresh_port_list)
        self.threadControlButton.clicked.connect(self.handle_thread_control_button)
        self.serialThread.new_data.connect(self.handle_new_data)
        self.portChoice.currentTextChanged.connect(self.handle_new_port_choice)
        self.textInput.returnPressed.connect(self.handle_user_input)

    def get_serial_port(self) -> SerialPort:
        port_id = self.portChoice.currentText()
        if port_id == FAKE_PORT_NAME:
            return FakeSerialPort(self.loaded_settings)
        return RealSerialPort(port_id, self.loaded_settings)

    def stop_serial_port(self) -> None:
        self.serialThread.pause()
        while not self.serialThread.is_paused():
            time.sleep(0.1)
        
    @Slot(str)
    def handle_new_port_choice(self, text):
        self.stop_serial_port()

        try:
            new_port = self.get_serial_port()
        except serial.serialutil.SerialException as e:
            QMessageBox.critical(self, f"Error while configuring port", str(e))
            self.portChoice.setCurrentText(self.previousPortChoice)
            new_port = None
        else:
            self.previousPortChoice = text

        self.serialThread.resume(new_port)
        
    @Slot()
    def handle_thread_control_button(self):
        if self.serialThread.is_paused():
            self.serialThread.resume()
            self.threadControlButton.setText(ThreadControlButtonText.PAUSE_THREAD.value)
        else:
            self.serialThread.pause()
            self.threadControlButton.setText(ThreadControlButtonText.RESUME_THREAD.value)

    @Slot(str)
    def handle_new_data(self, data: str):
        self.textDisplay.moveCursor(QTextCursor.MoveOperation.End)
        self.textDisplay.insertPlainText(data)
        self.textDisplay.moveCursor(QTextCursor.MoveOperation.End)

        if self.loaded_settings.reading_mode is ReadingMode.READ_LINE:
            parsed_data = json.loads(data)

            new_data_added = False

            if isinstance(parsed_data, (int, float)):
                new_data_added = True
                self.plotData["default"].append(parsed_data)

            elif isinstance(parsed_data, dict):
                for label, data_point in parsed_data.items():
                    # TODO: flatten the dict
                    assert isinstance(data_point, (int, float))
                    new_data_added = True
                    if label not in self.plotData:
                        self.plotData[label] = [data_point]
                        self.curves[label] = self.plotDisplay.plot()
                        self.curves[label].setPen((200,0,0), width=3)
                    else:
                        self.plotData[label].append(data_point)
                    
            if new_data_added:
                self.plotData["t"].append(time.monotonic() - self.timeStart)
                for label, curve in self.curves.items():
                    curve.setData(x=self.plotData["t"], y=self.plotData[label])

    @Slot()
    def handle_settings_action(self):
        dialog = SettingsDialog(self.loaded_settings, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            save_serial_settings(self.saved_settings, dialog.settings)
            self.loaded_settings = dialog.settings
            self.stop_serial_port()
            self.serialThread.resume(
                self.get_serial_port()
            )


    @Slot()
    def handle_refresh_port_list(self):        
        available_ports = sorted(
            [port_info[0] for port_info in serial.tools.list_ports.comports()]
        ) + [FAKE_PORT_NAME, self.previousPortChoice]  # Do not change the current port

        self.portChoice.blockSignals(True)  # Do not trigger a reconnect
        self.portChoice.clear()
        self.portChoice.addItems(available_ports)
        self.portChoice.setCurrentText(self.previousPortChoice)
        self.portChoice.blockSignals(False)

    @Slot()
    def handle_user_input(self):
        line = self.textInput.text().strip()
        self.textInput.setText("")
        ending = LineEnding(self.lineEndChoice.currentText())
        match ending:
            case LineEnding.NEW_LINE:
                line += "\n"
            case LineEnding.CARRIAGE_RETURN:
                line += "\r"
            case LineEnding.BOTH_NL_AND_CR:
                line += "\r\n"
            
        self.serialThread.send_line(line)

    def closeEvent(self, event):
        self.serialThread.shutdown()
        while self.serialThread.isRunning():
            time.sleep(0.01)
        super().closeEvent(event)

app = QApplication()

window = MainWindow()
window.show()

app.exec()
