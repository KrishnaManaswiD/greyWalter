from tortoise import Tortoise
from enums import Direction, SensorType

#In this version they fix the values and fill in the else.

# Change this to 1 when you've calibrated and have some values for not enough light, good light and too much light.
calibrated = 0;

def main():
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

		# Oh no our light sensor values are so silly, can you replace them with more sensible ones based on your calibration findings?
		if lightSensorReading < 1000:
			Name.doRandomStep()
			print "Where's the light?"
		elif 1000<= lightSensorReading  and lightSensorReading <1645:
			# What should we be printing here?
			Name.moveMotors(30, Direction.forward)	
		else: 
			print "Argh! Too much light!"
			# So the tortoise has found too much light. How should they move now?

if __name__=="__main__":
	main()
