# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 00:57:18


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class SignalWidget(QWidget):
  """docstring for SignalWidget"""
  def __init__(self, mainview):
    QWidget.__init__(self)
    self.mainLayout = QVBoxLayout(self)
    self.testlabel = QLabel("Signal")
    self.mainLayout.addWidget(self.testlabel)
    self.setLayout(self.mainLayout)

  def update(self, model):
    self.testlabel.setText(model.getSignalName())