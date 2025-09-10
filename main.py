from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QPlainTextEdit,
    QToolBar,
    QApplication,
    QComboBox,
)
from PySide6.QtCore import (
    QThreadPool,
    QRunnable,
)
from PySide6.QtGui import (
    QAction,
)


import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Viewer")

        # Actions
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setStatusTip("Exit the application.")
        self.exit_action.triggered.connect(self.close)

        # Menus
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.file_menu.addAction(self.exit_action)

        # Status bar
        self.status = self.statusBar()

        # Toolbar
        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(self.toolbar)

        self.portChoice = QComboBox()
        self.portChoice.setPlaceholderText("Choose serial device")
        self.toolbar.addWidget(self.portChoice)


        # Tabs
        self.textDisplay = QPlainTextEdit()
        self.graphDisplay = pg.PlotWidget()
        self.graphDisplay.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        )

        self.tabs = QTabWidget()
        self.tabs.addTab(self.textDisplay, "Text Display")
        self.tabs.addTab(self.graphDisplay, "Graph Display")

        # Central widget
        self.setCentralWidget(self.tabs)

        # Threads
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)


app = QApplication()

window = MainWindow()
window.show()

app.exec()
