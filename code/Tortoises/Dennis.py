from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Dennis=Tortoise()

while True:

    Dennis.setLEDValue(1, 0)
    Dennis.setLEDValue(2, 0)

    rightSensor = Dennis.getSensorData(SensorType.proximity,1)
    leftSensor = Dennis.getSensorData(SensorType.proximity,2)
    if rightSensor == 1:
        print "Obstruction right"
        Dennis.setLEDValue(1, 1) 
	Dennis.turnOnTheSpot(20,Direction.backwards_right)
    elif leftSensor == 1:
        print "Obstruction left"
        Dennis.setLEDValue(2,1)
	Dennis.turnOnTheSpot(20,Direction.backwards_left)
    else:
        print "I'm wandering..."
        Dennis.moveForwards(30)

