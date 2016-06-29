from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

Name=Tortoise()

lastFrontSwitch = 0
lastBackSwitch = 0

while True:
	currentFrontSwitch = Name.getSensorData(SensorType.touch,3)
	currentBackSwitch = Name.getSensorData(SensorType.touch,1)
    
	forwards = abs(lastBackSwitch - currentBackSwitch)
	backwards = abs(lastFrontSwitch - currentFrontSwitch)

	if forwards==1 and backwards==0:
		lastFrontSwitch=currentFrontSwitch
		print "Moving forwards"
        	Name.moveForwards(5)
		
	if backwards ==1 and forwards==0:
		lastbackSwitch=currentBackSwitch
		print "Moving backwards"
		Name.moveBackwards(5)
	else:
		print "No switches on"

