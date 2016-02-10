import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dist_sense_pin = 21
GPIO.setup(dist_sense_pin,GPIO.IN)

while True:
	if(GPIO.input(dist_sense_pin) == GPIO.HIGH):
		print "pin is high"
	else:
		print "pin is low"
