from tortoise import Tortoise
from enums import Direction, SensorType

Name=Tortoise()

while True:

    touchSensorValue = Name.getSensorData(SensorType.touch, 1)

    if touchSensorValue == 1:

        print "Touch sensor is being pressed"
        Name.setLEDValue(1, 1)
        Name.moveForwards(50)

    else:

        print "Nothing is pressing the touch sensor"
        Name.setLEDValue(1, 0)
