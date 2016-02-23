from tortoise import Tortoise
from enums import Direction, SensorType


def main():
	Mike = Tortoise()

	while True:
		if Mike.getSensorData(SensorType.light, 1) < 6:
			Mike.doRandomStep()
			print "Where's the light?"
		elif 6<= Mike.getSensorData(SensorType.light, 1)  and Mike.getSensorData(SensorType.light, 1) <9:
			print "Found Light"
			Mike.moveMotors(30, Direction.forward)	
		else: 
			print "Argh! Too much light!"
			Mike.moveMotors(30, Direction.backward)

if __name__=="__main__":
	main()
