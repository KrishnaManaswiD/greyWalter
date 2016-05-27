from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Elmer=Tortoise()

while True:

    proxSensor = Elmer.getSensorData(SensorType.proximity,1)
    proxSensor2 = Elmer.getSensorData(SensorType.proximity,2)
    if proxSensor == 1 and proxSensor2 == 0:
        print "Obstacle detected in front"
        Elmer.setLEDValue(1, 1) #self.setLEDValue(position, value)
    	Elmer.setLEDValue(2, 0) #self.setLEDValue(position, value)
    	Elmer.moveBackwards(150)
    elif proxSensor == 1 and proxSensor2 == 1:
    	print "Obstacles detected in front and behind!"
    	Elmer.setLEDValue(1, 1) #self.setLEDValue(position, value)
   	Elmer.setLEDValue(2, 1) #self.setLEDValue(position, value)
    elif proxSensor == 0 and proxSensor2 == 1:
        print "Obstacle detected behind"
        Elmer.setLEDValue(1, 0) #self.setLEDValue(position, value)
    	Elmer.setLEDValue(2, 1) #self.setLEDValue(position, value)
    	Elmer.moveForwards(150)
    else:
        print "No obstacle detected"
        Elmer.setLEDValue(1, 0) #self.setLEDValue(position, value)
   	Elmer.setLEDValue(2, 0) #self.setLEDValue(position, value)
