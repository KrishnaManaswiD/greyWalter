############################################################
# This program will be run when the tortoise process ends,
# either naturally or because of an exception.
# 
# The program stops the motors and LEDs to not drain battery 
# and cleans up the raspberry pi.
############################################################


import sys
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

# No warnings in this script
GPIO.setwarnings(False)

pinsMotors = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])]

pinsLEDs = [int(sys.argv[9]), int(sys.argv[10]), int(sys.argv[11]), int(sys.argv[12])]

GPIO.setup(pinsMotors[0], GPIO.OUT)
GPIO.setup(pinsMotors[1], GPIO.OUT)
GPIO.setup(pinsMotors[2], GPIO.OUT)
GPIO.setup(pinsMotors[3], GPIO.OUT)
GPIO.setup(pinsMotors[4], GPIO.OUT)
GPIO.setup(pinsMotors[5], GPIO.OUT)
GPIO.setup(pinsMotors[6], GPIO.OUT)
GPIO.setup(pinsMotors[7], GPIO.OUT)

GPIO.setup(pinsLEDs[0], GPIO.OUT)
GPIO.setup(pinsLEDs[1], GPIO.OUT)
GPIO.setup(pinsLEDs[2], GPIO.OUT)
GPIO.setup(pinsLEDs[3], GPIO.OUT)


GPIO.output(pinsMotors[0], 0)
GPIO.output(pinsMotors[1], 0)
GPIO.output(pinsMotors[2], 0)
GPIO.output(pinsMotors[3], 0)
GPIO.output(pinsMotors[4], 0)
GPIO.output(pinsMotors[5], 0)
GPIO.output(pinsMotors[6], 0)
GPIO.output(pinsMotors[7], 0)

GPIO.output(pinsLEDs[0], 0)
GPIO.output(pinsLEDs[1], 0)
GPIO.output(pinsLEDs[2], 0)
GPIO.output(pinsLEDs[3], 0)


# Sets all the pins to input
GPIO.cleanup()
