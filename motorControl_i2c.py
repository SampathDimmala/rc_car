import pca9685
from machine import Pin

MOTOR1_IN1 = 1
MOTOR1_IN2 = 2
MOTOR2_IN3 = 3
MOTOR2_IN4 = 4
SLEEP = 6

# The `motorControl_i2c_module` class initializes and controls a motor connected via I2C
# communication.
class motorControl_i2c_module:
    def __init__(self, i2c, address=0x40):
        #Set the pwm values for both motors to 0
        self.pwm_gen = pca9685.PCA9685(i2c,address)
        self.pwm_gen.freq(50) #set the pwm

        # Initialize the DRV SLEEP pin to high to enable the H bridge
        self.drv_sleep = Pin(SLEEP, Pin.OUT, value=True)

        self.motor1_in1 = self.pwm_gen.duty(MOTOR1_IN1, 0)
        self.motor1_in2 = self.pwm_gen.duty(MOTOR1_IN2, 0)
        self.motor2_in3 = self.pwm_gen.duty(MOTOR2_IN3, 0)
        self.motor2_in4 = self.pwm_gen.duty(MOTOR2_IN4, 0)

    def move_forward_control(self, pwm_val):
        """
        The code defines functions to control the movement of two motors, allowing the robot to move
        forward, backward, or halt.
        
        :param pwm_val: The `pwm_val` parameter is the PWM (Pulse Width Modulation) value that determines
        the speed of the motors. It is a numerical value that ranges from 0 to 4095, where 0 represents no
        movement and 4095 represents maximum speed
        """
        #set motor 1 pwm vals
        self.pwm_gen.duty(MOTOR1_IN1, 0)
        self.pwm_gen.duty(MOTOR1_IN2, pwm_val)

        #set motor 2 pwm vals
        self.pwm_gen.duty(MOTOR2_IN3, pwm_val)
        self.pwm_gen.duty(MOTOR2_IN4, 0)

    def move_backward_control(self, pwm_val):
        #set motor 1 pwm vals
        self.pwm_gen.duty(MOTOR1_IN1, pwm_val)
        self.pwm_gen.duty(MOTOR1_IN2, 0)

        #set motor 2 pwm vals
        self.pwm_gen.duty(MOTOR2_IN3, 0)
        self.pwm_gen.duty(MOTOR2_IN4, pwm_val)

    def control_motors(self, action, pwm_val):
        if action == "forward":
            self.move_forward_control(pwm_val)
        elif action == "backward":
            self.move_backward_control(pwm_val)
        elif action == "halt":
            self.halt()

    def halt(self):
        # Stop both motors
        self.pwm_gen.duty(MOTOR1_IN1, 0)
        self.pwm_gen.duty(MOTOR1_IN2, 0)

        #set motor 2 pwm vals
        self.pwm_gen.duty(MOTOR2_IN3, 0)
        self.pwm_gen.duty(MOTOR2_IN4, 0)                
