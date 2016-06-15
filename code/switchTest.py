from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    touchSensor = Name.getSensorData(SensorType.touch,1)
    if touchSensor == 1:
        print "Switch is on"
        Name.moveForward(30)
        Name.setActuatorValue(ActuatorType.led, 1, 1)
    else:
        print "Switch is off"
        Name.setActuatorValue(ActuatorType.led, 1, 0)
