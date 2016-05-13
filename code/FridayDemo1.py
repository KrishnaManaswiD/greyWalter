from tortoise import Tortoise
from enums import Direction, SensorType

#In this version they fix the values and fill in the else.

# Change this to 1 when you've calibrated and have some values for not enough light, good light and too much light.
calibrated = 0;

def main():
	# Name your tortoise here.
	Name = Tortoise()

	while True && (calibrated==1):
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
