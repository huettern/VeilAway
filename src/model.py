# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 09:08:40


import logging
import time

class Model(object):
  """docstring for Model"""
  def __init__(self, name):
    self.name = name
    self.exit = False
    self.view = None
    self.hasChanged = False

  def modelThread(self):
    logging.info("Thread %s: starting", self.name)
    
    while not self.exit:
      # MODEL CODE COMES HERE!!!!!
      time.sleep(1)
      print("set model changed true")
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
    return "/home/noah/Trackpictures/nice_weather/nice_weather_thusis_filisur_20200827_pixelated/image_01100.jpg"

  def getMapLocation(self):
    return [47.3775499,8.4666755]

  def getChanged(self):
    if self.hasChanged:
      self.hasChanged = False
      return True
    return False

if __name__ == "__main__":
  print("model main()")