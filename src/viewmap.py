# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:44:09
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 20:42:15

import io
import folium

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5 import QtGui

tk = "pk.eyJ1IjoiYmVlYmxlNDJicm94IiwiYSI6ImNrZmEwbzU2aTByN3oyem1hNGNsbmgyZ2YifQ.Wd6RYuQR8YQYWl21tzadEg"
tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(tk)

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
    self.tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
    ).add_to(m)

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
        location=coordinates, tiles="Stamen Toner", zoom_start=15
    )
    self.tile.add_to(m)

    folium.Marker(coordinates).add_to(m)

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
    