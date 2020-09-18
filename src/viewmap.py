# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 00:05:33


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class MapWidget(QWidget):
  """docstring for MapWidget"""
  def __init__(self, mainview):
    QWidget.__init__(self)
    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.addWidget(QLabel("Map"))
    self.setLayout(self.mainLayout)

