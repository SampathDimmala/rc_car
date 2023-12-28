import time
from machine import Pin, I2C

import netLib
import steer
import motor
import pca9685
import motorControl_i2c



# The code is creating a socket object by calling the `startServer()` function from the `netLib`
# module. This socket object is used to establish a connection with a server.

socket = netLib.startServer()



while True:
  #listen to server and execute the commands in the netLib
  netLib.listenToServer(socket)
  