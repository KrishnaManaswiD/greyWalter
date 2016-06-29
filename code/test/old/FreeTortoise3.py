from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

while True:

    touchSensor = Name.getSensorData(SensorType.touch,1)
    print "Front switch is:" 
    print touchSensor
    touchSensor2 = Name.getSensorData(SensorType.touch,3)
    print "Back switch is: " 
    print touchSensor2
    if touchSensor == 1:
        print "Switch is on"
        Name.moveBackwards(30)
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
	touchSensor2Loop = Name.getSensorData(SensorType.touch,3)
	print "Back switch as read inside loop: " 
        print touchSensor2Loop
	if touchSensor2 == 1:
		print "Back switch has been hit"
		Name.moveForwards(30)
		Name.setLEDValue(2, 0) #self.setLEDValue(position, value)
		if touchSensor == 0:
			break
   # else:
        #print "Switch is off"
        #Name.moveForwards(30)
        #Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
        #Name.setLEDValue(2, 1) #self.setLEDValue(position, value)
