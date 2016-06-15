from tortoise import Tortoise
from enums import Direction, SensorType

def main():
	Bob=Tortoise()
	while True:
		if Bob.getSensorData(SensorType.light,1)<4:
			Bob.doRandomStep()
			print "where are you?"
		elif Bob.getSensorData(SensorType.light,1)<9:
			Bob.moveForward(30)
			print "ah-ha!"
		else :
			Bob.moveBackward(30)
			print "Burning burning!"

if __name__ =="__main__":
	main()

