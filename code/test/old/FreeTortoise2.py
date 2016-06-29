from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    touchSensor = Name.getSensorData(SensorType.touch,1)
    if touchSensor == 1:
        print "Switch is on"
        Name.moveBackwards(30)
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
	if touchSensor == 1:
		print "Back switch has been hit"
		Name.moveForwards(30)
		Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
    else:
        print "Switch is off"
        Name.moveForwards(30)
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
        Name.setLEDValue(2, 1) #self.setLEDValue(position, value)
