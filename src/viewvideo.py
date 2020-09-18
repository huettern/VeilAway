# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 00:46:56

# Media player source: https://stackoverflow.com/questions/57842104/how-to-play-videos-in-pyqt

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)


class VideoWidget(QWidget):
  """docstring for VideoWidget"""
  def __init__(self, mainview):
    super(VideoWidget, self).__init__(mainview)
    # QWidget.__init__(self)

    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    videoWidget = QVideoWidget()


    layout = QVBoxLayout()
    layout.addWidget(videoWidget)
    # layout.addLayout(controlLayout)
    # layout.addWidget(self.statusBar)

    self.setLayout(layout)

    self.mediaPlayer.setVideoOutput(videoWidget)

    fileName = "/home/noah/Downloads/video.mp4"
    if fileName != '':
      print("------------------------------")
      self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
      self.play()
    self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
    self.mediaPlayer.positionChanged.connect(self.positionChanged)
    self.mediaPlayer.durationChanged.connect(self.durationChanged)
    self.mediaPlayer.error.connect(self.handleError)

    # self.mainLayout = QVBoxLayout(self)
    # self.mainLayout.addWidget(QLabel("Video"))
    # self.setLayout(self.mainLayout)

  def play(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      print("pause")
      self.mediaPlayer.pause()
    else:
      print("play")
      self.mediaPlayer.play()

  def mediaStateChanged(self, state):
    print("mediaStateChanged")
    # if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #   self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
    # else:
    #   self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

  def positionChanged(self, position):
    print("positionChanged")
    # print("position changed" + str(position))
    # self.positionSlider.setValue(position)

  def durationChanged(self, duration):
    print("durationChanged")
    # print("position changed" + str(position))
    # self.positionSlider.setRange(0, duration)

  def setPosition(self, position):
    self.mediaPlayer.setPosition(position)

  def handleError(self):
    # self.playButton.setEnabled(False)
    self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())
