import ustruct
import time
from machine import Pin, I2C

# The PCA9685 class is a Python class that provides methods for controlling a PCA9685 PWM driver chip
# via I2C communication.
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        
    def _write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self._write(0x00, 0x00) # Mode1

    def freq(self, freq=None):
        """
        The `freq` function calculates and sets the frequency of a device based on a given value or reads
        the current frequency if no value is provided.
        
        :param freq: The `freq` parameter is used to set the frequency of the device. If no value is
        provided, the method calculates and returns the current frequency based on the device's
        configuration. If a value is provided, the method sets the frequency to the specified value
        :return: If the `freq` parameter is `None`, the function will return the calculated frequency based
        on the value read from register 0xfe. If the `freq` parameter is provided, the function will set the
        prescale value based on the desired frequency and return `None`.
        """
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        time.sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on

    def pwm(self, index, on=None, off=None):
        """
        The code defines two functions, `pwm` and `duty`, for controlling the pulse width modulation (PWM)
        of a device.
        
        :param index: The index parameter is used to specify which PWM channel to control. It is an integer
        value that represents the index of the PWM channel
        :param on: The "on" parameter in the "pwm" function represents the number of clock cycles the PWM
        signal should stay high. It determines the duration of the "on" state of the signal
        :param off: The "off" parameter in the "pwm" function represents the number of clock cycles the PWM
        signal should be off for. It determines the duration of the low state of the signal
        :return: The `pwm` function returns a tuple of two values, `on` and `off`, which represent the on
        and off times of the PWM signal.
        """
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index,  data)

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self.pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return value
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)

