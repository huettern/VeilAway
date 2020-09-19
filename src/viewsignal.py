# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 14:02:08


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


class SignalWidget(QWidget):
  """docstring for SignalWidget"""
  def __init__(self, mainview):
    QWidget.__init__(self)
    self.mainLayout = QVBoxLayout(self)
    self.sig = None

    # self.testlabel = QLabel("Signal")
    # self.mainLayout.addWidget(self.testlabel)
    # self.setLayout(self.mainLayout)

    self.w = QtWebEngineWidgets.QWebEngineView()
    self.w.loadFinished.connect(self.onLoadFinished)
    with open('assets/signals.html', 'r') as file:
      html = file.read()
    self.w.setHtml(html)
    # self.w.resize(640, 480)
    self.mainLayout.addWidget(self.w)
    # w.show()

  def update(self, model):
    # self.testlabel.setText(model.getSignalName())
    self.sig = model.getNextSignal()
    # print("Signal View: Time to %d Distance To %d" %(self.sig.timeTo, self.sig.distanceTo))
    self.updateHtml()
  
  def updateHtml(self):
    timestring = "%d" % self.sig.timeTo
    distancestring = "%.2f km" % (self.sig.distanceTo/1000.0)
    # print("Timetring: %s Distancetring: %s" % (timestring, distancestring ))
    script  = ("document.getElementById(\"timevalue\").innerHTML = \"%s\";" % (timestring))
    script += ("document.getElementById(\"distancevalue\").innerHTML = \"%s\";" % (distancestring))
    self.w.page().runJavaScript(script, self.ready)

  def onLoadFinished(self, ok):
    if ok:
      self.updateHtml()

  def ready(self, returnValue):
    pass
    # print(returnValue)
