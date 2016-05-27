from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

# F  B 
# 0  0  move forwards
# 1  0  move backwards
# 1  1  move forwards
# 0  1  move backwards

Name=Tortoise()

while True:

    forwardSwitch = Name.getSensorData(SensorType.touch, 1)
    backwardSwitch = Name.getSensorData(SensorType.touch, 2)
#    if (forwardSwitch == backwardSwitch):
    if (forwardSwitch == 0 and backwardSwitch == 0) or (forwardSwitch == 1 and backwardSwitch == 1):
	print "monkey"
	if forwardSwitch == 1:
                print "Switch 1 is on"
        else:
                print "Switch 1 is off"

        if backwardSwitch == 1:
                print "Switch 2 is on"
        else:
                print "Switch 2 is off"

	print " "
        Name.moveForwards(30)
        Name.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Name.setLEDValue(2, 0) #self.setLEDValue(position, value)

#    if (forwardSwitch != backwardSwitch):
    if (forwardSwitch == 1 and backwardSwitch == 0) or (forwardSwitch == 0 and backwardSwitch == 1):
	print "donkey"
	if forwardSwitch == 1:
                print "Switch 1 is on"
        else:
                print "Switch 1 is off"

        if backwardSwitch == 1:
                print "Switch 2 is on"
        else:
                print "Switch 2 is off"

	print " "
        Name.moveBackwards(30)
        Name.setLEDValue(1, 0) #self.setLEDValue(position, value)
        Name.setLEDValue(2, 1) #self.setLEDValue(position, value)
