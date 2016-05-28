from tortoise import Tortoise
from enums import Direction, SensorType, ActuatorType
import random

Cora=Tortoise()

learnAssoc = 0.0
assocFlag = 0

while True:

    Cora.setLEDValue(1, 0) 
    responseFlag = 0

    responseSensor = Cora.getSensorData(SensorType.touch,1)
    stimulusSensor = Cora.getSensorData(SensorType.touch,2)

    print "Resp=%f stim=%f learn=%f assoc=%f" % (responseSensor,stimulusSensor,learnAssoc,assocFlag)

    # response always triggered by main sensor
    if responseSensor == 1:
        responseFlag = 1

    if stimulusSensor == 1:
        # update accumulator
        if responseSensor == 1:
            learnAssoc = 0.6*learnAssoc + 0.4
            Cora.setLEDValue(1, 1) 
        else:
            learnAssoc = 0.75*learnAssoc
        # check association thresholds
        if (learnAssoc > 0.8 and assocFlag == 0):
            assocFlag = 1
            Cora.setLEDValue(2, 1) 
        elif (learnAssoc < 0.2 and assocFlag == 1):
            assocFlag = 0
            Cora.setLEDValue(2, 0) 
        # trigger response if associated
        if assocFlag == 1:
            responseFlag = 1
   
    if responseFlag == 1:        
	Cora.moveForwards(100)
    else:
        if random.random()<0.5:
            Cora.turnOnTheSpot(10,Direction.backwards_right)
        else:
            Cora.turnOnTheSpot(10,Direction.backwards_left)

