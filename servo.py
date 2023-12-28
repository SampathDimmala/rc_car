import pca9685
import math


# The `Servos` class is a Python class that controls servos using the PCA9685 PWM driver.
class Servos:
    def __init__(self, i2c, address=0x40, freq=50, min_us=600, max_us=2400,
                 degrees=180):
        self.period = 1000000 / freq
        self.min_duty = self._us2duty(min_us)
        self.max_duty = self._us2duty(max_us)
        self.degrees = degrees
        self.freq = freq
        self.pca9685 = pca9685.PCA9685(i2c, address)
        self.pca9685.freq(freq)

    def _us2duty(self, value):
        """
        The above code defines a position function that sets the duty cycle of a servo motor based on the
        desired position in degrees, radians, microseconds, or directly in duty cycle.
        
        :param value: The `value` parameter in the `_us2duty` method represents the input value that needs
        to be converted to a duty cycle
        :return: The function `_us2duty` returns an integer value. The `position` function does not have a
        return statement, so it does not return any value.
        """
        return int(4095 * value / self.period)

    def position(self, index, degrees=None, radians=None, us=None, duty=None):
        """
        The `position` function calculates the duty cycle based on the given input (degrees, radians,
        microseconds, or duty cycle) and sets the duty cycle for a specific index on a PCA9685 device.
        
        :param index: The index parameter represents the index or channel number of the servo motor. It is
        used to identify which servo motor to control when there are multiple servo motors connected to the
        PCA9685 controller
        :param degrees: The degrees parameter represents the angle in degrees that you want to set for the
        servo motor
        :param radians: The "radians" parameter is used to specify the position in radians. It is used to
        calculate the duty cycle based on the given radians value and the range of motion in degrees
        :param us: The "us" parameter represents the pulse width in microseconds. It is used to set the
        position of a servo motor
        :param duty: The "duty" parameter represents the duty cycle of a PWM (Pulse Width Modulation)
        signal. It determines the amount of time the signal is high compared to the total period of the
        signal. In this code, the "duty" parameter is used to set the position of a servo
        :return: If none of the conditions for degrees, radians, us, or duty are met, then the function will
        return the duty cycle of the PCA9685 at the specified index.
        """
        span = self.max_duty - self.min_duty
        if degrees is not None:
            duty = self.min_duty + span * degrees / self.degrees
        elif radians is not None:
            duty = self.min_duty + span * radians / math.radians(self.degrees)
        elif us is not None:
            duty = self._us2duty(us)
        elif duty is not None:
            pass
        else:
            return self.pca9685.duty(index)
        duty = min(self.max_duty, max(self.min_duty, int(duty)))
        self.pca9685.duty(index, duty)

    def release(self, index):
        """
        The `release` function sets the duty cycle of a PCA9685 channel to 0, effectively releasing any
        attached device.
        
        :param index: The index parameter is the index of the servo motor that you want to release
        """
        self.pca9685.duty(index, 0)
