from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Elsie=Tortoise()

while True:

    proxSensor = Elsie.getSensorData(SensorType.proximity,1)
    if proxSensor == 1:
        print "Obstacle detected behind"
        Elsie.setLEDValue(1, 1) #self.setLEDValue(position, value)
	Elsie.moveForwards(150)
    else:
        print "No obstacle detected"
        Elsie.setLEDValue(1, 0) #self.setLEDValue(position, value)
        Elsie.doRandomMovement()
