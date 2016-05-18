from tortoise import Tortoise
from enums import Direction, SensorType

#In this version they fix the values and fill in the else.

# Change this to 1 when you've calibrated and have some values for not enough light, good light and too much light.
calibrated = 1;


# Name your tortoise here.
Frankie = Tortoise()

if (calibrated==0):
	print "Let's use different levels of light to see what calibrated readings we get"
	raw_input("First let's see what the room gives us, press enter when you're done")
	print Frankie.getSensorData(SensorType.light,1)
	raw_input("Now try it with a light source right up close and press enter when you're done")
	print Frankie.getSensorData(SensorType.light,1)
	raw_input("And now try somewhere in the middle")
	print Frankie.getSensorData(SensorType.light,1)

while True and (calibrated==1):
	# First we need a reading from the light sensor
	lightSensorReading = Frankie.getSensorData(SensorType.light,1)

	# Can you tune the light sensor values for the conditions based on your calibration findings?
	if lightSensorReading < 4:
		Frankie.doRandomStep()
		print "Where's the light?"
	elif 4<= lightSensorReading  and lightSensorReading <9:
		# What should we be printing here?
		print "I am a happy turtle"
		Frankie.moveMotors(30, Direction.forward)	
	else: 
		print "Argh! Too much light!"
		# So your tortoise has found too much light. How should they move now?
		Frankie.moveMotors(30, Direction.backward)	
