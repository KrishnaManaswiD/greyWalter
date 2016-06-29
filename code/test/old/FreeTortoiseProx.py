from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    proxSensor = Name.getSensorData(SensorType.proximity,1)
    if proxSensor == 1:
        print "Obstacle dected"
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
    else:
        print "No obstacle detected"
        Name.moveForwards(30)
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
