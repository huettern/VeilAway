# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 00:05:03


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class VideoWidget(QWidget):
  """docstring for VideoWidget"""
  def __init__(self, mainview):
    QWidget.__init__(self)
    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.addWidget(QLabel("Video"))
    self.setLayout(self.mainLayout)
    