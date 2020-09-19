#!/usr/bin/env python

# from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import functools


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
import PyQt5.QtCore as QtCore
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5 import QtGui, QtWebEngineWidgets

from PyQt5.QtWidgets import QSizePolicy, QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        #self.setFixedSize(800, 500)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        label = self.label = QLabel()
        sp = QSizePolicy()
        sp.setVerticalStretch(0)
        label.setSizePolicy(sp)
        vbox.addWidget(label)

        view = self.view = QtWebEngineWidgets.QWebView()
        
        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        view.page().networkAccessManager().setCache(cache)
        view.page().networkAccessManager()
        
        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.page().setLinkDelegationPolicy(QtWebEngineWidgets.QWebPage.DelegateAllLinks)
        view.load(QtCore.QUrl('map.html'))
        view.loadFinished.connect(self.onLoadFinished)
        view.linkClicked.connect(QDesktopServices.openUrl)
        
        vbox.addWidget(view)

        button = QPushButton('Go to Paris')
        panToParis = functools.partial(self.panMap, 2.3272, 48.8620)
        button.clicked.connect(panToParis)
        vbox.addWidget(button)

    def onLoadFinished(self):
        with open('map.js', 'r') as f:
            frame = self.view.page().mainFrame()
            frame.evaluateJavaScript(f.read())

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        self.label.setText('Lng: {:.5f}, Lat: {:.5f}'.format(lng, lat))

    def panMap(self, lng, lat):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript('map.panTo(L.latLng({}, {}));'.format(lat, lng))

if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    app.exec_()