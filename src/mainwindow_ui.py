# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.textView = QWidget()
        self.textView.setObjectName(u"textView")
        self.verticalLayout_2 = QVBoxLayout(self.textView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textDisplay = QPlainTextEdit(self.textView)
        self.textDisplay.setObjectName(u"textDisplay")
        self.textDisplay.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textDisplay)

        self.tabWidget.addTab(self.textView, "")
        self.plotView = QWidget()
        self.plotView.setObjectName(u"plotView")
        self.verticalLayout_3 = QVBoxLayout(self.plotView)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.plotDisplay = PlotWidget(self.plotView)
        self.plotDisplay.setObjectName(u"plotDisplay")

        self.verticalLayout_3.addWidget(self.plotDisplay)

        self.tabWidget.addTab(self.plotView, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textInput = QLineEdit(self.centralwidget)
        self.textInput.setObjectName(u"textInput")

        self.horizontalLayout.addWidget(self.textInput)

        self.lineEndChoice = QComboBox(self.centralwidget)
        self.lineEndChoice.setObjectName(u"lineEndChoice")

        self.horizontalLayout.addWidget(self.lineEndChoice)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName(u"menu_Edit")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.actionSettings)
        self.menu_File.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Serial Viewer", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.textView), QCoreApplication.translate("MainWindow", u"Text View", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotView), QCoreApplication.translate("MainWindow", u"Plot View", None))
        self.textInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type text to send ...", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

