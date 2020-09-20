# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'form.ui'
#
# Created: Mon Apr 30 13:43:19 2018
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_run = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_run.setGeometry(QtCore.QRect(40, 20, 311, 191))
        self.pushButton_run.setObjectName("pushButton_run")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 230, 721, 241))
        self.textEdit.setObjectName("textEdit")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 490, 721, 23))
        self.progressBar.setObjectName("progressBar")
        Form.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        Form.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Form)
        self.statusbar.setObjectName("statusbar")
        Form.setStatusBar(self.statusbar)
