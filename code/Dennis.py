from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Arthur=Tortoise()

while True:

    Arthur.setLEDValue(1, 0)
    Arthur.setLEDValue(2, 0)

    rightSensor = Arthur.getSensorData(SensorType.proximity,1)
    leftSensor = Arthur.getSensorData(SensorType.proximity,2)
    if rightSensor == 1:
        print "Obstruction right"
        Arthur.setLEDValue(1, 1) 
	Arthur.turnOnTheSpot(20,Direction.backwards_right)
    elif leftSensor == 1:
        print "Obstruction left"
        Arthur.setLEDValue(2,1)
	Arthur.turnOnTheSpot(20,Direction.backwards_left)
    else:
        print "I'm wandering..."
        Arthur.moveForwards(30)

