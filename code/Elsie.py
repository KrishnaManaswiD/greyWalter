from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Elsie=Tortoise()

while True:
    proxSensor1 = Elsie.getSensorData(SensorType.proximity,1)
    proxSensor = Elsie.getSensorData(SensorType.proximity,2)
    if proxSensor == 1:
        print "Obstacle detected behind"
        Elsie.setLEDValue(2, 1) #self.setLEDValue(position, value)
        Elsie.setLEDValue(1,0)
        Elsie.moveForwards(150)
    elif proxSensor1 == 1:
        print "Obstacle in front"
        Elsie.setLEDValue(1,1)
        Elsie.setLEDValue(2,0)
        Elsie.moveBackwards(150)
    else:
        print "No obstacle detected"
        Elsie.setLEDValue(2, 0) #self.setLEDValue(position, value)
        Elsie.setLEDValue(1,0)
        Elsie.doRandomMovement()
