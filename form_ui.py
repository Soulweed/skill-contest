# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.original = QtGui.QFrame(self.centralwidget)
        self.original.setGeometry(QtCore.QRect(10, 20, 311, 221))
        self.original.setFrameShape(QtGui.QFrame.StyledPanel)
        self.original.setFrameShadow(QtGui.QFrame.Raised)
        self.original.setObjectName(_fromUtf8("original"))
        self.process = QtGui.QFrame(self.centralwidget)
        self.process.setGeometry(QtCore.QRect(320, 20, 311, 221))
        self.process.setFrameShape(QtGui.QFrame.StyledPanel)
        self.process.setFrameShadow(QtGui.QFrame.Raised)
        self.process.setObjectName(_fromUtf8("process"))
        self.ok_btn = QtGui.QPushButton(self.centralwidget)
        self.ok_btn.setGeometry(QtCore.QRect(310, 390, 99, 27))
        self.ok_btn.setCheckable(False)
        self.ok_btn.setObjectName(_fromUtf8("ok_btn"))
        self.process_btn = QtGui.QPushButton(self.centralwidget)
        self.process_btn.setGeometry(QtCore.QRect(420, 390, 99, 27))
        self.process_btn.setObjectName(_fromUtf8("process_btn"))
        self.exit_btn = QtGui.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(530, 390, 99, 27))
        self.exit_btn.setObjectName(_fromUtf8("exit_btn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMain_Window = QtGui.QMenu(self.menubar)
        self.menuMain_Window.setObjectName(_fromUtf8("menuMain_Window"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMain_Window.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.ok_btn.setText(_translate("MainWindow", "Snap", None))
        self.process_btn.setText(_translate("MainWindow", "Egde", None))
        self.exit_btn.setText(_translate("MainWindow", "Exit", None))
        self.menuMain_Window.setTitle(_translate("MainWindow", "File", None))

