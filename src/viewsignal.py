# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 19:07:15


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


import base64
import datetime

SIGNALS_DIR = "assets/signals/png/120"

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
    s = self.sig.timeTo
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    timestring = '{:02}:{:02}'.format(int(minutes), int(seconds))
    distancestring = "%.2f km" % (self.sig.distanceTo)
    
    script  = ("document.getElementById(\"timevalue\").innerHTML = \"%s\";" % (timestring))
    script += ("document.getElementById(\"distancevalue\").innerHTML = \"%s\";" % (distancestring))

    if self.sig.distant:
      im1 = SIGNALS_DIR+"/distant"+self.sig.distant+".png" if self.sig.distant else ""
      # print(im1)
      data = open(im1, "rb").read()
      im1str = "data:image/png;base64,"+base64.b64encode(data).decode("utf-8")
    else:
      im1str = ""
    script += ("document.getElementById(\"valueimg1\").src=\"%s\";" % (im1str))
    if self.sig.main:
      im2 = SIGNALS_DIR+"/main"+self.sig.main+".png" if self.sig.main else ""
      # print(im2)
      data = open(im2, "rb").read()
      im2str = "data:image/png;base64,"+base64.b64encode(data).decode("utf-8") 
    else:
      im2str = ""
    script += ("document.getElementById(\"valueimg2\").src=\"%s\";" % (im2str))

    idstring = self.sig.id
    typestirng = self.sig.elementType

    script += ("document.getElementById(\"idvalue\").innerHTML = \"%s\";" % (idstring))
    script += ("document.getElementById(\"typevalue\").innerHTML = \"%s\";" % (typestirng))

    self.w.page().runJavaScript(script, self.ready)

  def onLoadFinished(self, ok):
    if ok:
      self.updateHtml()

  def ready(self, returnValue):
    pass
    # print(returnValue)
