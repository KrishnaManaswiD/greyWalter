from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType
Walter=Tortoise()

lastMove = "forward"

while True:

    frontSwitch = Walter.getSensorData(SensorType.touch, 1)
    backSwitch = Walter.getSensorData(SensorType.touch, 2)

    if frontSwitch ==1 and backSwitch ==0:

        print "Obstacle in front - moving backwards"    
        Walter.setLEDValue(1, 0) #self.setLEDValue(position, value)
        Walter.setLEDValue(2, 1) #self.setLEDValue(position, value)
        lastMove = "back"

    elif backSwitch ==1 and frontSwitch ==1:

        print "Can't move!"    

    elif frontSwitch ==0 and backSwitch ==1:

        print "Obstacle behind - moving forwards"    
        Walter.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Walter.setLEDValue(2, 0) #self.setLEDValue(position, value)
        lastMove = "forward"

    else:
        print "Exploring"
        Walter.setLEDValue(1, 1) #self.setLEDValue(position, value)
        Walter.setLEDValue(2, 1) #self.setLEDValue(position, value)


    if lastMove == "forward":
            Walter.moveForwards(100)
    else:
        Walter.moveBackwards(100)
