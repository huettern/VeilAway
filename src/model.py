# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 23:22:24
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-18 23:39:10


import logging
import time

class Model(object):
  """docstring for Model"""
  def __init__(self, name):
    self.name = name
    self.exit = False
    self.view = None

  def modelThread(self):
    logging.info("Thread %s: starting", self.name)
    
    while not self.exit:
      # MODEL CODE COMES HERE!!!!!
      pass

    logging.info("Thread %s: finishing", self.name)

  def terminate(self):
    self.exit = True

  def setView(self, view):
    self.view = view




if __name__ == "__main__":
  print("model main()")