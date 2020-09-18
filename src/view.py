# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 01:19:49


import logging
import time
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot

# custom widgets
from viewvideo import VideoWidget
from viewsignal import SignalWidget
from viewmap import MapWidget

class Window(QDialog):

  def __init__(self):
    super(Window, self).__init__()

    # Button to load data
    self.LoadButton = QPushButton('Load Data')
    # Button connected to `plot` method
    self.PlotButton = QPushButton('Plot')

    # set the layout
    self.horizontalGroupBox = QGroupBox("Grid")
    layout = QGridLayout()

    layout.setColumnStretch(0, 6)
    layout.setColumnStretch(1, 4)
    layout.setRowStretch(0, 5)
    layout.setRowStretch(1, 5)
    
    # Video widget
    self.wvideo = VideoWidget(self)
    layout.addWidget(self.wvideo,0,0,2,1)

    # Signal widget
    self.wsignal = SignalWidget(self)
    layout.addWidget(self.wsignal,0,1,1,1)

    # Signal widget
    self.wmap = MapWidget(self)
    layout.addWidget(self.wmap,1,1,1,1)

    self.setLayout(layout)

    self.setGeometry(100,100,1300,600)
    self.setWindowTitle("UI Testing")

  def update(self, model):
    self.wsignal.update(model)
    self.wvideo.update(model)
    self.wmap.update(model)


class View(object):
  """docstring for Model"""
  def __init__(self, name):
    self.name = name
    self.exit = False
    self.model = None

  def viewThread(self):
    logging.info("Thread %s: starting", self.name)
    
    app = QApplication(sys.argv)

    self.main = Window()
    self.main.show()

    sys.exit(app.exec_())

    # app = QApplication([])

    # window = MainWindows.main_window()
    # window.show()
    # app.exec_()

    # # self.setWindowTitle("Trainline")
    # # self.setGeometry(self.left, self.top, self.width, self.height)
    
    # self.createGridLayout()
    
    # windowLayout = QVBoxLayout()
    # windowLayout.addWidget(self.horizontalGroupBox)
    # window.setLayout(windowLayout)
    
    # self.show()

    # app.exec_()

    while not self.exit:
      # VIEW CODE COMES HERE!!!!!
      pass

    logging.info("Thread %s: finishing", self.name)


  def terminate(self):
    self.exit = True

  def setModel(self, model):
    self.model = model

  def update(self):
    self.main.update(self.model)

if __name__ == "__main__":
  print("view main()")