# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 15:08:37


import logging
import time
import sys

from PyQt5.QtWidgets import QPushButton, QSpinBox, QSlider, QComboBox, QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QTimer, QObject
from PyQt5 import QtCore

# custom widgets
from viewvideo import VideoWidget
from viewsignal import SignalWidget
from viewmap import MapWidget

# view polling interval in [ms]
VIEW_UPDATE_INTERVAL = 100
MAP_UPDATE_INTERVAL = 1000

class Window(QDialog):

  def __init__(self):
    super(Window, self).__init__()
    self.mapUpdateCtr = 0

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

    self.setGeometry(100,100,1500,600)
    # self.showMaximized()
    self.setStyleSheet("background-color: white;")
    self.setWindowTitle("Trainline")

  def update(self, model):
    self.mapUpdateCtr += VIEW_UPDATE_INTERVAL
    if self.mapUpdateCtr >= MAP_UPDATE_INTERVAL:
      self.mapUpdateCtr = 0
      self.wmap.update(model)
    
    self.wsignal.update(model)
    self.wvideo.update(model)


class DebugWindow(QDialog):

  def __init__(self, model):
    super(DebugWindow, self).__init__()
    self.model = model
    self.horizontalGroupBox = QGroupBox("Grid")
    layout = QGridLayout()

    layout.setColumnStretch(0, 5)
    layout.setColumnStretch(1, 5)
    layout.setRowStretch(0, 5)
    layout.setRowStretch(1, 5)

    # first row: image selection
    row = 0
    layout.addWidget(QLabel("Image Type"),row,0,1,1)
    self.cbImgSelect = QComboBox()
    self.cbImgSelect.addItem("good weather")
    self.cbImgSelect.addItem("bad weather")
    self.cbImgSelect.addItem("night")
    layout.addWidget(self.cbImgSelect,row,1,1,1)
    self.cbImgSelect.currentIndexChanged.connect(self.cbImgChange)


    # direction select
    row += 1
    layout.addWidget(QLabel("Direction"),row,0,1,1)
    self.cbDirection = QComboBox()
    self.cbDirection.addItem("Thusis -> Filisur")
    self.cbDirection.addItem("Filisur -> Thusis")
    layout.addWidget(self.cbDirection,row,1,1,1)
    self.cbDirection.currentIndexChanged.connect(self.cbDirChange)

    # im name
    row += 1
    layout.addWidget(QLabel("Image"),row,0,1,1)
    self.lblImageName = QLabel()
    layout.addWidget(self.lblImageName,row,1,1,1)

    # overlay
    row += 1
    layout.addWidget(QLabel("Overlay"),row,0,1,1)
    self.checkboxOverlay = QCheckBox()
    layout.addWidget(self.checkboxOverlay,row,1,1,1)
    self.checkboxOverlay.stateChanged.connect(self.cbOverlay)

    # GPS mode
    row += 1
    layout.addWidget(QLabel("GPS mode"),row,0,1,1)
    self.btnGPSMode = QPushButton("Play")
    layout.addWidget(self.btnGPSMode,row,1,1,1)
    self.btnGPSMode.clicked.connect(self.cbGPSModeChange)

    # Velocity
    row += 1
    layout.addWidget(QLabel("Velocity"),row,0,1,1)
    self.sbVelocity = QSpinBox()
    self.sbVelocity.setMinimum(0)
    self.sbVelocity.setMaximum(100)
    self.sbVelocity.setValue(10)
    layout.addWidget(self.sbVelocity,row,1,1,1)
    self.sbVelocity.valueChanged.connect(self.cbGPSVelocityChange)

    # Position slider
    row += 1
    layout.addWidget(QLabel("Postion"),row,0,1,1)
    self.sliderPosition = QSlider()
    self.sliderPosition.setOrientation(QtCore.Qt.Orientation(1))
    layout.addWidget(self.sliderPosition,row,1,1,1)
    self.sliderPosition.sliderReleased.connect(self.cbSliderValueChanged)

    # pos
    row += 1
    layout.addWidget(QLabel("Position"),row,0,1,1)
    self.lblPosition = QLabel()
    layout.addWidget(self.lblPosition,row,1,1,1)
    # lat
    row += 1
    layout.addWidget(QLabel("Lat"),row,0,1,1)
    self.lblLat = QLabel()
    layout.addWidget(self.lblLat,row,1,1,1)
    # lon
    row += 1
    layout.addWidget(QLabel("Long"),row,0,1,1)
    self.lblLon = QLabel()
    layout.addWidget(self.lblLon,row,1,1,1)

    self.setLayout(layout)
    self.setWindowTitle("debug")

  def cbSliderValueChanged(self):
    self.model.setSliderValue(self.sliderPosition.value(), self.sliderPosition.minimum(), self.sliderPosition.maximum())

  def cbGPSVelocityChange(self, velocity):
    self.model.gpsEmulationVelocity = velocity

  def cbGPSModeChange(self):
    if self.btnGPSMode.text() == "Play":
      self.btnGPSMode.setText("Pause")
      self.model.gpsEmulationMode = "static"
    elif self.btnGPSMode.text() == "Pause":
      self.btnGPSMode.setText("Play")
      self.model.gpsEmulationMode = "velocity"
    
  def cbImgChange(self, idx):
    if idx == 0:
      # good weather
      self.model.setImageSource("good")
    elif idx == 1:
      # bad weather
      self.model.setImageSource("bad")
    elif idx == 2:
      # night
      self.model.setImageSource("night")

  def cbDirChange(self, idx):
    if idx == 0:
      self.model.setDirection("tf")
    elif idx == 1:
      self.model.setDirection("ft")

  def cbOverlay(self):
    self.model.overlayEnabled = self.checkboxOverlay.isChecked()

  def update(self, model):
    self.lblImageName.setText(model.currentImage)
    self.lblPosition.setText("%.3fkm" % (model.pos/1000.0) )
    self.lblLat.setText("%.5f" % model.lat)
    self.lblLon.setText("%.5f" % model.lon)

class View(QObject):
  """docstring for Model"""
  def __init__(self, name):
    super(View, self).__init__()
    self.name = name
    self.exit = False
    self.model = None

  def viewThread(self):
    logging.info("Thread %s: starting", self.name)
    
    app = QApplication(sys.argv)

    self.main = Window()
    self.main.show()
    self.debug = DebugWindow(self.model)
    self.debug.show()

    self.timer = QTimer(self)
    self.timer.setInterval(VIEW_UPDATE_INTERVAL)
    self.timer.timeout.connect(self.timerEvent)
    self.timer.start()
    print("after timer start")
    sys.exit(app.exec_())
    print("after app exec")

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

    # while not self.exit:
    #   # VIEW CODE COMES HERE!!!!!
    #   time.sleep(1)
    #   print("View heartbeat")
    #   pass

    logging.info("Thread %s: finishing", self.name)


  def timerEvent(self):
    # print("timer event")
    if self.model.getChanged():
      # print("view: model has changed")
      self.main.update(self.model)
      self.debug.update(self.model)

  def terminate(self):
    self.exit = True

  def setModel(self, model):
    self.model = model

  def update(self):
    self.main.update(self.model)

if __name__ == "__main__":
  print("view main()")