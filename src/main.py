
import logging
import threading
import time


from model import Model
from view import View

if __name__ == "__main__":

	# setup logger
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                      datefmt="%H:%M:%S")

  # create model thread
  model = Model("model")
  modelThd = threading.Thread(target=model.modelThread)

  # create main view thread
  view = View("view")
  # viewThd = threading.Thread(target=view.viewThread)

  # connect model and view
  model.setView(view)
  view.setModel(model)

  # start threads
  logging.info("Main    : starting model thread")
  modelThd.start()
  # logging.info("Main    : starting view thread")
  # viewThd.start()
  view.viewThread()
  

  # x.join()
  time.sleep(5)
  logging.warning("Main    : terminating in 2s")
  time.sleep(2)

  view.terminate()
  model.terminate()
  viewThd.join()
  modelThd.join()
  logging.info("Main    : exiting")

