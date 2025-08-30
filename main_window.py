from PySide6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QMenu,
    QComboBox,
    QPushButton,
)
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtCore import (
    Slot, Signal, QObject, QRunnable, QThreadPool, QMetaObject
)
from serial.tools.list_ports import comports
import serial

class SerialReaderSignals(QObject):
    byteAvailable = Signal(bytes)


class SerialReaderWorker(QRunnable):

    def __init__(self, port: str):
        super().__init__()
        self._should_stop = False
        self._port = port
        self.signals = SerialReaderSignals()

    @Slot()
    def run(self):
        print("thread_start")
        ser = serial.Serial(self._port)
        print(ser.name)
        while not self._should_stop:
            byte = ser.read()
            self.signals.byteAvailable.emit(byte)
        print("thread complete")

    @Slot()
    def shouldStop(self):
        self._should_stop = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Port Viewer")
        self.resize(900, 600)
        self.move(
            self.screen().geometry().center() - self.frameGeometry().center()
        )
        
        self._listening = False
        file_menu = self.menuBar().addMenu("&File")
        self.quit_action = self._create_action(
            "E&xit", file_menu, self.close
        )

        toolbar = self.addToolBar("Tools")
        self._devices_list = QStandardItemModel()
        self._devices_combobox = QComboBox()
        self._devices_combobox.setPlaceholderText("Choose device")
        self._devices_combobox.setModel(self._devices_list)

        refresh_devices_button = QPushButton("Refresh devices")
        refresh_devices_button.clicked.connect(self._refresh_devices)

        toolbar.addWidget(self._devices_combobox)
        toolbar.addWidget(refresh_devices_button)

        start_button = QPushButton("Start listening")
        start_button.clicked.connect(self.start_listening)
        toolbar.addWidget(start_button)

        self._stop_button = QPushButton("Stop listening")
        self._stop_button.clicked.connect(self.stop_listening)
        toolbar.addWidget(self._stop_button)       
        
        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self.setCentralWidget(self._text_edit)

        self._worker: SerialReaderWorker | None = None
        self._connection: QMetaObject.Connection | None = None

        self._refresh_devices()

    @Slot()
    def _refresh_devices(self):
        self._devices_list.clear()
        for port, _desc, _hwid in sorted(comports()):
            self._devices_list.appendRow(QStandardItem(port))

    @Slot()
    def start_listening(self):
        if not self._listening:
            self._listening = True
            self._worker = SerialReaderWorker(self._devices_combobox.currentText())
            self._worker.signals.byteAvailable.connect(self.append_byte_to_text_view)
            QThreadPool.globalInstance().start(self._worker)
            self._connection = self._stop_button.clicked.connect(self._worker.shouldStop)

    @Slot()
    def stop_listening(self):
        self._listening = False

    @Slot()
    def append_byte_to_text_view(self, byte: bytes):
        text = byte.decode("utf-8")
        self._text_edit.insertPlainText(text)
        self._text_edit.ensureCursorVisible()

    def _create_action(self, text: str, menu: QMenu, slot):
        action = QAction(text, self)
        menu.addAction(action)
        action.triggered.connect(slot)
        return action
    
    def _close_app(self):
        if self._worker is not None:
            self._worker.shouldStop()
        self.close()



