from tortoise import Tortoise
from enums import Direction, SensorType
# In this version, they test the robot first and then fix the values and fill in the else. If format is good, but too much work, then prefill else.

# Change this to 1 when you've calibrated and have some values for not enough light, good light and too much light.
calibrated = 0;

# Name your tortoise here.
Name = Tortoise()

if (calibrated==0):
	print "Let's use different levels of light to see what calibrated readings we get"
	raw_input("First let's see what the room gives us, press enter when you're done")
	print Name.getSensorData(SensorType.light,1)
	raw_input("Now try it with a light source right up close and press enter when you're done")
	print Name.getSensorData(SensorType.light,1)
	raw_input("And now try somewhere in the middle")
	print Name.getSensorData(SensorType.light,1)

while True and (calibrated==1):
	# First we need a reading from the light sensor
	lightSensorReading = Name.getSensorData(SensorType.light,1)
	
	# Can you tune the light sensor values for the conditions based on your calibration findings?
	if lightSensorReading < 1:
		Name.moveMotors(30, Direction.forwards)
		print "Where's the light?"
	elif 1<= lightSensorReading  and lightSensorReading <2:
		print "Found the light!"
		Name.moveMotors(30, Direction.backwards)	
	else: 
		print "Argh! Too much light!"
		Name.doRandomStep()
