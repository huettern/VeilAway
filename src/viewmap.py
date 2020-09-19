# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 09:10:47

import io
import folium

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5 import QtGui

class MapWidget(QWidget):
  """docstring for MapWidget"""
  def __init__(self, mainview):
    super(MapWidget, self).__init__(mainview)

    # QWidget.setFrameStyle( QFrame.Panel | QFrame.Raised );
    # QWidget.frame = QtGui.QFrame()


    self.mainLayout = QVBoxLayout(self)
    # self.mainLayout.addWidget(QLabel("Map"))
    self.setLayout(self.mainLayout)

    m = folium.Map(
        location=[46.6807711,9.6756752], tiles="Stamen Toner", zoom_start=13
    )

    data = io.BytesIO()
    m.save(data, close_file=False)

    self.w = QtWebEngineWidgets.QWebEngineView()
    self.w.setHtml(data.getvalue().decode())
    # self.w.resize(640, 480)
    self.mainLayout.addWidget(self.w)
    # data.close()

    # frame = QFrame(self)
    # frame.setFrameShape(QFrame.StyledPanel)
    # frame.setLineWidth(0.6)
    
    # w.show()



  def update(self, model):

    coordinates = model.getMapLocation()

    m = folium.Map(
        location=coordinates, tiles="Stamen Toner", zoom_start=13
    )

    data = io.BytesIO()
    m.save(data, close_file=False)

    # print(data.getvalue().decode())
    # print(type(self.w))
    # self.mainLayout.addWidget(QLabel("asdf"))
    # self.w = QtWebEngineWidgets.QWebEngineView()
    self.w.setHtml(data.getvalue().decode())


    # m = folium.Map(
    #     location=[46.6807711,9.6756752], tiles="Stamen Toner", zoom_start=13
    # )
    # data = io.BytesIO()
    # m.save(data, close_file=False)
    # neww = QtWebEngineWidgets.QWebEngineView()
    # x = data.getvalue().decode()
    # neww.setHtml(x)
    # neww.setHtml(data.getvalue().decode())
    # self.mainLayout.addWidget(neww)

    # self.mainLayout.addWidget(self.w)
    # self.mainLayout.removeWidget(self.w)
    