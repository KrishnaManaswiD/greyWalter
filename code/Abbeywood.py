from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    touchSensor = Name.getSensorData(SensorType.touch,1)
    if touchSensor == 1:
        print "Switch is on"
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
	Name.moveForwards(50)
    else:
        print "Switch is off"
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
