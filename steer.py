import servo
import time
from machine import Pin, I2C

# The `SteeringControl` class initializes a servo motor and sets its initial position to 90 degrees.
class SteeringControl:
    def __init__(self, i2c):
        # self.i2c = self.initI2c()
        self.steer = servo.Servos(i2c)
        self.currentPosition = 90
        self.steer.position(0, self.currentPosition)

    def turn(self,index, degrees):
        """
        The function "turn" adjusts the position of a steering mechanism to a specified degree and then
        releases it.
        
        :param index: The `index` parameter represents the index or identifier of the steering mechanism
        that you want to control. It is used to specify which steering mechanism you want to turn
        :param degrees: The "degrees" parameter represents the angle at which the object should be turned.
        It is a value between 0 and 180, where 0 represents no turn and 180 represents a full turn
        """
        degrees = min(max(degrees, 0), 180)  # Constrain degrees to 0-180

        shift = abs(self.currentPosition - degrees)
        self.currentPosition = degrees

        self.steer.position(index, degrees)
        time.sleep(shift * 0.01043)
        time.sleep(0.2)
        self.steer.release(index)

