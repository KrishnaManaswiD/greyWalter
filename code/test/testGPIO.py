import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.IN)

while True:
        print GPIO.input(3)
        time.sleep(0.5)
