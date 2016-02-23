# IMPORT MODULES FROM SUBFOLDERS #
""" It's neccesary in order to import modules not in the same folder, but in a different one.
This is the way to tell python the location on those subfolders: """
import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Subfolder "lowlevel"
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"lowlevel")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# ------------------------------ #

from motors import Motor
from sensors import Sensor
from enum import Enum
import time
import numpy as np
import thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)



class State(Enum):
	paused = 0
	running = 1

class SensorType(Enum):
    touch = 0
    light = 1
    proximity = 2

class Direction(Enum):
    counterClockwise = -4
    backward_right = -3
    backward_left = -2
    backward = -1
    static = 0
    forward = 1
    forward_left = 2
    forward_right = 3
    clockwise = 4


class Tortoise:

	def __init__(self):

		global isLightCalibrated
		global lowerBoundLight
		global upperBoundLight

		isLightCalibrated = False
		lowerBoundLight = 0
		upperBoundLight = 0

		self.A = Motor(4, 17, 23, 24)
		self.B = Motor(5, 18, 22, 27)
		#self.sensor = Sensor(1,2,3,5,6,7,8,9,10,11)
		self.delay = 8
		self.switchForEmergencyStop_pin = 6
		self.state = State.paused

		if not isLightCalibrated:
			self.calibrateLight()

		try:
	 		thread.start_new_thread(self.pauseAndResume, ())
		except:
			print "Error: unable to start thread"

		while self.state == State.paused:
			time.sleep(0.1)
	


	def pauseAndResume(self):
		GPIO.setup(self.switchForEmergencyStop_pin, GPIO.IN)

		while True:
	
			if GPIO.input(self.switchForEmergencyStop_pin) == GPIO.HIGH:
				if self.state == State.running:
					self.state = State.paused
				elif self.state == State.paused:
					self.state = State.running

			time.sleep(0.1)



	def isPaused(self):
		return self.state == State.paused


	def calibrateLight(self):
		global lowerBoundLight, upperBoundLight, isLightCalibrated

		raw_input("Now we are in cinema mode. Let's do some tricks. Please, turn the lights off and press enter.")
		lowerBoundLight = max(self.sensor.readSensor(SensorType.light, 1), self.sensor.readSensor(SensorType.light, 2))

		raw_input("Now please place a light source in front of the tortoise's eyes and press enter.")
		upperBoundLight = min((self.sensor.readSensor(SensorType.light, 1), self.sensor.readSensor(SensorType.light, 2)))

		isLightCalibrated = True

		print("Gert lush, me babber! (That's very Bristolian)")



	def getSensorData(self,sensor_type,pos):
		if self.state == State.running:
			value = self.sensor.readSensor(sensor_type,pos)

			if sensor_type == SensorType.light:
				# Scale
				return round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9))

			else:
				return value


	def moveMotors(self, steps, direction):

		if direction == Direction.static:
		    print "Are you kiddin' me??"
		    return

		for x in range(0,steps):
	
		    # If a stop command has been sent, the turtle will stop its movement
		    if self.state == State.paused:
			break;

		    if direction == Direction.backward_left or direction == Direction.backward or direction == Direction.counterClockwise:
			self.A.backwards(int(self.delay) / 1000.00, int(1))
		    if direction == Direction.backward_right or direction == Direction.backward or direction == Direction.clockwise:
			self.B.backwards(int(self.delay) / 1000.00, int(1))
		    if direction == Direction.forward_right or direction == Direction.forward or direction == Direction.clockwise:
			self.A.forward(int(self.delay) / 1000.00, int(1))
		    if direction == Direction.forward_left or direction == Direction.forward or direction == Direction.counterClockwise:
			self.B.forward(int(self.delay) / 1000.00, int(1))

		print "Cheers, drive!"


	def naturalTurn(self, totalSteps, straightStep, sideStep, direction):

		if straightStep < 0 or sideStep < 0: return
		if not direction == Direction.forward_left and not direction == Direction.forward_right and not direction == Direction.backward_left and not direction == Direction.backward_right:
		    print "Don't mess around."
		    return

		for x in range(0, int(totalSteps/(straightStep+sideStep))):
		    if direction == Direction.forward_left:
		        self.moveMotors(straightStep, Direction.forward)
		        self.moveMotors(sideStep, Direction.forward_left)
		    if direction == Direction.forward_right:
		        self.moveMotors(straightStep, Direction.forward)
		        self.moveMotors(sideStep, Direction.forward_right)
		    if direction == Direction.backward_left:
		        self.moveMotors(straightStep, Direction.backward)
		        self.moveMotors(sideStep, Direction.backward_left)
		    if direction == Direction.backward_right:
		        self.moveMotors(straightStep, Direction.backward)
		        self.moveMotors(sideStep, Direction.backward_right)

	def gentleTurn(self, steps, direction):
        	self.naturalTurn(steps, 3, 1, direction)

	def sharpTurn(self, steps, direction):
        	self.naturalTurn(steps, 1, 3, direction)

	def tryCircle(self, direction):
		self.gentleTurn(2000, direction)

	def defaultCircle(self):
		self.tryCircle(Direction.forward_right)

	def doRandomStep(self):

		# Random number between 15 and (503*3 + 15)
		numberOfSteps = int(509*3*np.random.random_sample() + 15)

		# Random number between 0 and 1
		randomNumber = np.random.random_sample()		

		if(randomNumber < 0.4):
			self.moveMotors(numberOfSteps, Direction.forward)
		else:
			# Random direction: left of right
			if(np.random.random_sample() < 0.5):
				direction = Direction.forward_left
			else:
				direction = Direction.forward_right
		

			if(randomNumber < 0.7):
				self.gentleTurn(numberOfSteps, direction)
			else:
				self.sharpTurn(numberOfSteps, direction)

