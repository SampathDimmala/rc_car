import time
from machine import Pin, I2C

import netLib
import steer
import motor
import pca9685
import motorControl_i2c




socket = netLib.startServer()



while True:
  #listen to server and execute the commands in the netLib
  netLib.listenToServer(socket)
  