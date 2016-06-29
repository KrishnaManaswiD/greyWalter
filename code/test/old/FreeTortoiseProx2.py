from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    proxSensor = Name.getSensorData(SensorType.proximity,1)
    proxSensor2 = Name.getSensorData(SensorType.proximity,2)
    if proxSensor == 1 and proxSensor2 == 0:
        print "Obstacle detected in front"
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
	Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
	Name.moveBackwards(30)
    if proxSensor == 1 and proxSensor2 == 1:
	print "Obstacles detected in front and behind!"
	Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
	Name.setLEDValue(2, 1) #self.setLEDValue(position, value)
    if proxSensor == 0 and proxSensor2 == 1:
        print "Obstacle detected behind"
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
	Name.setLEDValue(2, 1) #self.setLEDValue(position, value)
	Name.moveForwards(30)
    else:
        print "No obstacle detected"
        #Name.moveForwards(30)
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
	Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
