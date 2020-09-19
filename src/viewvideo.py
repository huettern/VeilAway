# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 21:17:28

# Media player source: https://stackoverflow.com/questions/57842104/how-to-play-videos-in-pyqt

from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QPainter
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QProgressBar)


PBAR_ENABLE = True

class VideoWidget(QWidget):
  """docstring for VideoWidget"""
  def __init__(self, mainview):
    super(VideoWidget, self).__init__(mainview)
    layout = QVBoxLayout()
    self.pic = QLabel(self)
    self.pic.setPixmap(QPixmap("/home/noah/Trackpictures/nice_weather/nice_weather_thusis_filisur_20200827_pixelated/image_05000.jpg"))
    layout.addWidget(self.pic)
    self.setLayout(layout)

    if PBAR_ENABLE:
        self.pbar = QProgressBar()
        self.pbar.setRange(0,999)
        self.pbar.setValue(333)
        self.pbar.setTextVisible(False)
        layout.addWidget(self.pbar)

  def update(self, model):
    img_fname = model.getImageName()
    arImgList = model.getARImageInfo()

    image = QImage(img_fname)

    painter = QPainter()
    painter.begin(image)

    for imInfo in arImgList:
        if imInfo['show']:
            overlay = QImage(imInfo['fname'])
            painter.drawImage(image.width()/2+imInfo['loc_x'], image.height()/2+imInfo['loc_y'], overlay)
    painter.end()
     
    # label = QLabel()
    self.pic.setPixmap(QPixmap.fromImage(image))
    # label.show()

    # progress bar
    if PBAR_ENABLE:
        start = model.lastSignLocation
        stop = start + model.lastDistanceToNext
        self.pbar.setRange(100*start,100*stop)
        self.pbar.setValue(100*(stop-model.nextSignal.distanceTo))
        # print("start %f stop %f value %f" % (start, stop, stop-model.nextSignal.distanceTo))


    # pm = QPixmap(img_fname)
    

    # self.pic.setPixmap(pm)