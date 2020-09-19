# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 10:08:46


import logging
import time
import os.path

TRACK_PIC_DIR = "/home/noah/Trackpictures"
DW_TO_DIR = {
  "tfg": "nice_weather/nice_weather_thusis_filisur_20200827_pixelated",
  "tfb": "bad_weather/bad_weather_thusis_filisur_20200829_pixelated",
  "ftg": "nice_weather/nice_weather_filisur_thusis_20200824_pixelated",
  "ftb": None,
  "tfn": "night/night_thusis_filisur_20200828",
  "ftn": None,
}
IMG_NOT_FOUND = "assets/imnotfound.png"

class Model(object):
  """docstring for Model"""
  def __init__(self, name):
    self.name = name
    self.exit = False
    self.view = None
    self.hasChanged = False
    self.tmpImage = 1100
    self.imgSource = "g" # g for good weather, b for bad, n for night
    self.drivingDirection = "tf" # tf for thusis filisur
    self.currentImage = ""

  def modelThread(self):
    logging.info("Thread %s: starting", self.name)
    
    while not self.exit:
      # MODEL CODE COMES HERE!!!!!
      time.sleep(0.2)
      # print("set model changed true")
      self.hasChanged = True
      # self.view.update()
      pass

    logging.info("Thread %s: finishing", self.name)

  def terminate(self):
    self.exit = True

  def setView(self, view):
    self.view = view

  def getSignalName(self):
    return "Signal Name"

  def getImageName(self):
    folder = DW_TO_DIR[self.drivingDirection+self.imgSource]
    fname = ""
    if folder is not None:
      fname = ("%s/%s/image_%05d.jpg" % (TRACK_PIC_DIR, folder, self.tmpImage) )
      self.currentImage = ("image_%05d.jpg" % (self.tmpImage))
      print("loading %s" % fname)
    else:
      print("folder %s not found" % (folder))
    
    if not os.path.isfile(fname):
      fname = IMG_NOT_FOUND
    self.tmpImage += 1
    return fname

  def getMapLocation(self):
    return [47.3775499,8.4666755]

  def getChanged(self):
    if self.hasChanged:
      self.hasChanged = False
      return True
    return False

  def setImageSource(self, weather):
    if weather == "good":
      self.imgSource = "g"
    elif weather == "bad":
      self.imgSource = "b"
    elif weather == "night":
      self.imgSource = "n"

  def setDirection(self, direction):
    self.drivingDirection = direction

if __name__ == "__main__":
  print("model main()")