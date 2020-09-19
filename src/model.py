# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-19 18:32:04


import logging
import time
import json
import os

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

SIGNAL_IMG_DIR = "assets/signals/png/120"

SIGNAL_TYPES = ["40", "60", "90", "stop", "vmax"]

MODEL_LOOP_TIME = 0.2 # s


def relativeToCoordinates(rel):
  print("TODO: UNIMPLEMENTED")
  return [47.3775499,8.4666755]

def coordinatesToRelative(c):
  print("TODO: UNIMPLEMENTED")
  return 12123


class Signal(object):
  def __init__(self):
    self.distant = None # can be None or any of SIGNAL_TYPES
    self.main = None # can be None or any of SIGNAL_TYPES
    self.id = None
    self.elementType = None
    self.coordinates = [0,0]
    self.relative = 0 # in km

    # Items to display
    self.timeTo = 30 # s
    self.distanceTo = 1000 # m


  def fromJson(self, j):
    if 'ID' in j.keys():
      self.id = j['ID']
    else:
      print("CRITICAL: sign has no ID")

    if 'Element Type' in j.keys():
      self.elementType = j['Element Type']
    
    hRel, hCo = False, False
    if 'Relative Position' in j.keys():
      hRel = True
      self.relative = j['Relative Position']
    if ('Latitude' in j.keys()) and ('Longitude' in j.keys()):
      hCo = True
      self.coordinates = [j['Latitude'], j['Longitude']]

    # calculate missing
    if not hRel:
      self.relative = coordinatesToRelative(self.coordinates)
    if not hCo:
      self.coordinates = relativeToCoordinates(self.relative)

  def fromTest(self):
    self.distant = SIGNAL_TYPES[0] # can be None or any of SIGNAL_TYPES
    self.main = SIGNAL_TYPES[0] # can be None or any of SIGNAL_TYPES
    self.id = "C5"
    self.elementType = "Main & distant signal"
    self.coordinates = [46.69915247,9.44028485]
    self.relative = 41.128


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
    self.overlayEnabled = False
    self.gpsEmulationMode = "static" # static or velocity
    self.gpsEmulationVelocity = 10 # km/h

    # current vehicle position
    self.pos = 41.111 # km
    self.lat = 46.6981226
    self.lon = 9.4412016
    self.currentImage = 'image_00101.jpg'

    # last signal
    self.lastSignLocation = 23300
    self.lastDistanceToNext = 1000

    # next signal
    self.nextSignal = Signal()

    # read data json
    self.imToRel = json.load(open('assets/img_to_rel_pos.json'))
    self.export = json.load(open('assets/export.json'))

  def modelThread(self):
    logging.info("Thread %s: starting", self.name)
    
    while not self.exit:
      # MODEL CODE COMES HERE!!!!!
      time.sleep(MODEL_LOOP_TIME)
      # print(self.gpsEmulationMode)

      # run gps emulation
      if self.gpsEmulationMode == "velocity":
        if self.drivingDirection == "tf":
          self.pos += (MODEL_LOOP_TIME/3600.0)*self.gpsEmulationVelocity
        elif self.drivingDirection == "ft":
          self.pos -= (MODEL_LOOP_TIME/3600.0)*self.gpsEmulationVelocity

      self.hasChanged = True

    logging.info("Thread %s: finishing", self.name)

  def terminate(self):
    self.exit = True

  def setView(self, view):
    self.view = view

  def getSignalName(self):
    return "Signal Name"

  def getNextSignal(self):
    # TODO: implement signal logic
    self.nextSignal.fromTest()
    # TODO: implement time/distance calculation
    # self.nextSignal.timeTo -= 0.1
    # self.nextSignal.distanceTo -= 1
    return self.nextSignal

  def getImageName(self):
    im = self.calcCurrentImage()
    return im

  def getARImageInfo(self):
    imInfoList = []
    y_off = -350
    if self.nextSignal.main:
      imInfo = {}
      imInfo['loc_x'] = 0
      imInfo['loc_y'] = y_off
      imInfo['fname'] = SIGNAL_IMG_DIR+"/main"+self.nextSignal.main+".png"
      imInfo['show'] = self.overlayEnabled
      imInfoList.append(imInfo)
    if self.nextSignal.distant:
      imInfo = {}
      imInfo['loc_x'] = -40
      imInfo['loc_y'] = y_off+125
      imInfo['fname'] = SIGNAL_IMG_DIR+"/distant"+self.nextSignal.distant+".png"
      imInfo['show'] = self.overlayEnabled
      imInfoList.append(imInfo)

    return imInfoList

  def getMapLocation(self):
    return [self.lat,self.lon]

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

  def calcCurrentImage(self):
    # Search closest
    nrst = 0
    for dist in self.export['Relative Position']:
      if self.export['Relative Position'][dist] > self.pos:
        nrst = dist
        break
    self.currentImage = self.export['Closest Image'][nrst]
    self.lat = self.export['Latitude'][nrst]
    self.lon = self.export['Longitude'][nrst]

    # print(nrst)
    # print("found nearest. our %d theirs %d index %s" % (self.pos, self.export['Relative Position'][nrst], nrst))
    # print("closest image: " + self.currentImage)
    # print("lat %f lon %f" % (self.lat, self.lon))

    folder = DW_TO_DIR[self.drivingDirection+self.imgSource]
    fname = ("%s/%s/%s" % (TRACK_PIC_DIR, folder, self.currentImage) )

    if not os.path.isfile(fname):
      fname = IMG_NOT_FOUND

    # # For now, just use a simple counter
    # folder = DW_TO_DIR[self.drivingDirection+self.imgSource]
    # fname = ""
    # if folder is not None:
    #   fname = ("%s/%s/image_%05d.jpg" % (TRACK_PIC_DIR, folder, self.tmpImage) )
    #   self.currentImage = ("image_%05d.jpg" % (self.tmpImage))
    #   # print("loading %s" % fname)
    # else:
    #   # print("folder %s not found" % (folder))
    #   pass
    
    # self.tmpImage += 1
    return fname

  def calcARSignalPosition(self):
    # middle of frame for now
    return [0,0]

  def setSliderValue(self, slider, mn, mx):
    print("Model: slider set to %d in (%d %d)" % (slider, mn, mx) )

if __name__ == "__main__":
  print("model main()")