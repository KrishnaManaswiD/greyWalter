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
			Mike.moveForward(30)	
		else: 
			print "Argh! Too much light!"
			Mike.moveBackward(30)

if __name__=="__main__":
	main()
