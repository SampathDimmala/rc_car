import time
from machine import I2C, Pin, Timer
import servo
import steer
from vl5310 import VL53L0X
from netLib import i2c_1, i2c_0, steer_tof,drive

PROXIMITY_SERVO_INDEX = 6
distance =0
current_proximity_position =90
servo_direction = True



###########################################################################
#TIME OF FLIGHT CODE
tof = VL53L0X(i2c_0)

budget  = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)

# Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the 
# given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
# to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
# Valid values are (even numbers only):

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

##################################################################################
#INTERRUPT CODE
def timer_callback(timer):
    #Code to execute when timer interrupt occurs
    print("irq\n")
    #Get the distance readings and save them and increment the servo motor position
    global distance
    global PROXIMITY_SERVO_INDEX
    global current_proximity_position

    if servo_direction and current_proximity_position <115:
        current_proximity_position += 5
    elif not servo_direction and current_proximity_position >65:
        current_proximity_position -=5

    steer_tof.turn(PROXIMITY_SERVO_INDEX,current_proximity_position)
    distance = tof.ping() - 50 #Reading is in mm with 50mm being the correction value

    if distance <300:
        drive.control_motors("halt", 0)
        time.sleep_ms(500)
        

# Create a timer object
timer = Timer()

# Initialize the timer interrupt
# Timer.PERIODIC means the interrupt repeats at the interval
# The interval is given in milliseconds, so 50ms is specified as 50
timer.init(period=50, mode=Timer.PERIODIC, callback=timer_callback)
