from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType

# F  B 
# 0  0  move forwards
# 1  0  move backwards
# 1  1  move forwards
# 0  1  move backwards

Walter=Tortoise()

while True:

    forwardSwitch = Walter.getSensorData(SensorType.touch, 1)
    backwardSwitch = Walter.getSensorData(SensorType.touch, 2)
#    if (forwardSwitch == backwardSwitch):
    if (forwardSwitch == 0 and backwardSwitch == 0) or (forwardSwitch == 1 and backwardSwitch == 1):
	print "Moving forwards"
	if forwardSwitch == 1:
                print "Switch 1 is on"
        else:
                print "Switch 1 is off"

        if backwardSwitch == 1:
                print "Switch 2 is on"
        else:
                print "Switch 2 is off"

	print " "
        Walter.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Walter.setLEDValue(2, 0) #self.setLEDValue(position, value)
	Walter.moveForwards(100)

#    if (forwardSwitch != backwardSwitch):
    if (forwardSwitch == 1 and backwardSwitch == 0) or (forwardSwitch == 0 and backwardSwitch == 1):
	print "Moving backwards"
	if forwardSwitch == 1:
                print "Switch 1 is on"
        else:
                print "Switch 1 is off"

        if backwardSwitch == 1:
                print "Switch 2 is on"
        else:
                print "Switch 2 is off"

	print " "
        Walter.setLEDValue(1, 0) #self.setLEDValue(position, value)
        Walter.setLEDValue(2, 1) #self.setLEDValue(position, value)
        Walter.moveBackwards(100)
