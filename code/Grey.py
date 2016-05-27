from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Grey=Tortoise()

while True:

    touchSensor = Grey.getSensorData(SensorType.touch,1)
    if touchSensor == 1:
        print "Switch is on"
        Grey.setLEDValue(1, 1) #self.setLEDValue(position, value)
	Grey.moveForwards(50)
    else:
        print "Switch is off"
        Grey.setLEDValue(1, 0) #self.setLEDValue(position, value)
