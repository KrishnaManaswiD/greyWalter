##########################################################
# This program will be run when the tortoise process ends,
# either naturally or because of an exception.
# 
# The program stops the motors to not drain baterry and 
# cleans up the raspberry pi.
##########################################################


import sys
import RPi.GPIO as GPIO  

# No warnings in this script
GPIO.setwarnings(False)

pins = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])]

GPIO.setup(pins[0], GPIO.OUT)
GPIO.setup(pins[1], GPIO.OUT)
GPIO.setup(pins[2], GPIO.OUT)
GPIO.setup(pins[3], GPIO.OUT)
GPIO.setup(pins[4], GPIO.OUT)
GPIO.setup(pins[5], GPIO.OUT)
GPIO.setup(pins[6], GPIO.OUT)
GPIO.setup(pins[7], GPIO.OUT)

GPIO.output(pins[0], 0)
GPIO.output(pins[1], 0)
GPIO.output(pins[2], 0)
GPIO.output(pins[3], 0)
GPIO.output(pins[4], 0)
GPIO.output(pins[5], 0)
GPIO.output(pins[6], 0)
GPIO.output(pins[7], 0)


# Sets all the pins to input
GPIO.cleanup()
