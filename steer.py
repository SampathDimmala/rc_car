import servo
import time
from machine import Pin, I2C

class SteeringControl:
    def __init__(self, i2c):
        # self.i2c = self.initI2c()
        self.steer = servo.Servos(i2c)
        self.currentPosition = 90
        self.steer.position(0, self.currentPosition)

    def turn(self,index, degrees):
        degrees = min(max(degrees, 0), 180)  # Constrain degrees to 0-180

        shift = abs(self.currentPosition - degrees)
        self.currentPosition = degrees

        self.steer.position(index, degrees)
        time.sleep(shift * 0.01043)
        time.sleep(0.2)
        self.steer.release(index)

