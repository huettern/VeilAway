# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 10:43:53

# Media player source: https://stackoverflow.com/questions/57842104/how-to-play-videos-in-pyqt

from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QPainter
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)


class VideoWidget(QWidget):
  """docstring for VideoWidget"""
  def __init__(self, mainview):
    super(VideoWidget, self).__init__(mainview)
    layout = QVBoxLayout()
    self.pic = QLabel(self)
    self.pic.setPixmap(QPixmap("/home/noah/Trackpictures/nice_weather/nice_weather_thusis_filisur_20200827_pixelated/image_05000.jpg"))
    layout.addWidget(self.pic)
    self.setLayout(layout)

  def update(self, model):
    img_fname = model.getImageName()
    arImg = model.getARImageInfo()

    image = QImage(img_fname)
    
    if arImg['show']:
      overlay = QImage(arImg['fname'])

    painter = QPainter()
    painter.begin(image)
    if arImg['show']:
      painter.drawImage(image.width()/2+arImg['loc_x'], image.height()/2+arImg['loc_y'], overlay)
    painter.end()
     
    # label = QLabel()
    self.pic.setPixmap(QPixmap.fromImage(image))
    # label.show()

    # pm = QPixmap(img_fname)
    

    # self.pic.setPixmap(pm)