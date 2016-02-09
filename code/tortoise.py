# IMPORT MODULES FROM SUBFOLDERS #
""" It's neccesary in order to import modules not in the same folder, but in a different one.
This is the way to tell python the location on those subfolders: """
import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Subfolder "lowlevel"
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"lowlevel")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# ------------------------------ #

from motors import Motor
from sensors import Sensors
from actuators import Actuators

import enums
import time
import numpy as np
#import thread
#import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#def synchronized(method):

#    def new_method(self, *arg, **kws):
#        with self.lock:
#            return method(self, *arg, **kws)


#    return new_method


class Tortoise:

    def __init__(self):

        global isLightCalibrated
        global lowerBoundLight
        global upperBoundLight

#        self.lock = threading.RLock()

        isLightCalibrated = False
        lowerBoundLight = 0
        upperBoundLight = 0

        motorPins = [4, 17, 23, 24, 27, 22, 18, 5]

        # CREATING FILE WITH PID

        # PID of process
        pid = os.getpid()

        # ~/.tortoise_pids/
        directory = os.path.expanduser("~") + "/.tortoise_pids/"

        # Filename: [PID].pid
        f = open(directory + str(pid) + ".pid", "w")

        f.write(str(motorPins[0]) + " " + str(motorPins[1]) + " " + str(motorPins[2]) + " " + str(motorPins[3]) + " " + str(motorPins[4]) + " " + str(motorPins[5]) + " " + str(motorPins[6]) + " " + str(motorPins[7]) + "\n")

        f.close()
        # ----------------------


        # TODO: change to self.Motor.Left
        self.A = Motor(motorPins[0], motorPins[1], motorPins[2], motorPins[3])
        self.B = Motor(motorPins[4], motorPins[5], motorPins[6], motorPins[7])
        self.sensors = Sensors()
        self.actuators = Actuators()
        self.delay = 2
        self.state = enums.State.paused

        self.sensors.setSensor(enums.SensorType.light, 1, 16)
        self.sensors.setSensor(enums.SensorType.light, 2, 2)
        #self.sensors.setSensor(enums.SensorType.touch, 1, 8)
        self.sensors.setSensor(enums.SensorType.touch, 2, 8)
        #self.sensors.setSensor(enums.SensorType.touch, 3, 13)
        #self.sensors.setSensor(enums.SensorType.touch, 4, 7)
        #self.sensors.setSensor(enums.SensorType.touch, 5, 8)
        #self.sensors.setSensor(enums.SensorType.touch, 6, 9)
        #self.sensors.setSensor(enums.SensorType.proximity, 1, 10)
        #self.sensors.setSensor(enums.SensorType.proximity, 2, 11)
        self.sensors.setSensor(enums.SensorType.emergencySwitch, 1, 6)

        self.actuators.initActuator(enums.ActuatorType.led,1,19)
        self.actuators.initActuator(enums.ActuatorType.led,2,26)

        #print "light sensor value:"
        #print self.sensors.readSensor(enums.SensorType.light, 1)
        if not isLightCalibrated:
            self.calibrateLight()

#        try:
#             thread.start_new_thread(self.pauseAndResume, ())
#        except:
#            print "Error: unable to start thread"

        print(chr(27) + "[2J")
        print "Tortoise alive! Press the pause/resume button to set me going."
        while self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:
            time.sleep(0.1)

        self.state = enums.State.running

#    def pauseAndResume(self):

#        while True:
#
#            if self.getSensorData(enums.SensorType.emergencySwitch, 1):
#                if self.getStateTortoise() == enums.State.running:
#                    self.setStateTortoise(enums.State.paused)
#                    print "Tortoise paused!"
#                elif self.getStateTortoise() == enums.State.paused:
#                    self.setStateTortoise(enums.State.running)
#                    print "Tortoise running!"

#                # For having time to switch state
#                time.sleep(0.5)

#            time.sleep(0.1)



#    @synchronized
    def getStateTortoise(self):
        return self.state

#    @synchronized
    def setStateTortoise(self, toState):
        self.state = toState

    def calibrateLight(self):
        global lowerBoundLight, upperBoundLight, isLightCalibrated

        raw_input("Base condition press enter.")
        #lowerBoundLight = max(self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2))
        lowerBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
        print "Light in dark conditions is: ", lowerBoundLight

        raw_input("Now please place a light source in front of the tortoise's eyes and press enter.")
        #upperBoundLight = min((self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2)))
        upperBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
        print "Light when there is a light source is:", upperBoundLight

        isLightCalibrated = True

        print("Finished")

    def getSensorData(self,sensor_type,pos):
        #if self.getStateTortoise() == enums.State.running:
        value = self.sensors.readSensor(sensor_type,pos)
        #added error checking + LED blinking
        if value<0:
            blinkLED()
            return -1
        #print "value", value
        if sensor_type == enums.SensorType.light:
            # Scale #TODO fix division by 0
            lightVal = int(9 - round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9)))
            # TODO What the heck?
            if lightVal < 0:
                lightVal = 0
            return lightVal
        elif sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencySwitch:
            return value % 2
        else:
            return value

    def setActuatorValue(self,actuator_type,pos,value):
        #if self.getStateTortoise() == enums.State.running:
        #added error checking + LED blinking
        if self.actuators.setActuator(actuator_type,pos,value)<0:
            blinkLED()
            return -1

    #internal function for LED error signal
    def blinkLED():
        self.actuators.setActuator(enums.ActuatorType.led, 1,1)
        time.sleep(0.5)
        self.actuators.setActuator(enums.ActuatorType.led, 1,0)
        time.sleep(0.5)
        self.actuators.setActuator(enums.ActuatorType.led, 1,1)
        time.sleep(0.5)
        self.actuators.setActuator(enums.ActuatorType.led, 1,0)

    def moveMotors(self, steps, direction):
        if steps<0:
            raise RuntimeError('Motor delay can only be a positive number!')
            blinkLED()
            return -1
        elif direction == enums.Direction.static or abs(direction)>4:
            raise RuntimeError('Illegal Direction Type!')
            blinkLED()
            return -1

        numberOfstepsCommanded = int(10)
        numberOfLoops = steps/numberOfstepsCommanded
        numberOfStepsRemaining = steps % numberOfstepsCommanded
        for x in range(0,numberOfLoops):

            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "Tortoise paused"
                    
                break;

            if self.getStateTortoise() == enums.State.paused:
                self.setStateTortoise(enums.State.running)
                print "Tortoise running"

            if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:
                self.A.backwards(int(self.delay) / 1000.00, numberOfstepsCommanded)
            elif direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:
                self.B.backwards(int(self.delay) / 1000.00, numberOfstepsCommanded)
            elif direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:
                self.A.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)
            elif direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:
                self.B.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)


        if numberOfStepsRemaining > 0:
            
            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "Tortoise paused"

                else:

                    if self.getStateTortoise() == enums.State.paused:
                        self.setStateTortoise(enums.State.running)
                        print "Tortoise running"

                    if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:
                        self.A.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)
                    elif direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:
                        self.B.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)
                    elif direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:
                        self.A.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)
                    elif direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:
                        self.B.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)



        self.A.stopMotors()
        self.B.stopMotors()



    def naturalTurn(self, totalSteps, straightStep, sideStep, direction):

        if straightStep < 0 or sideStep < 0: return
        if not direction == enums.Direction.forward_left and not direction == enums.Direction.forward_right and not direction == enums.Direction.backward_left and not direction == enums.Direction.backward_right:
            raise RuntimeError('Illegal Direction Type!')
            blinkLED()
            return -1

        for x in range(0, int(totalSteps/(straightStep+sideStep))):
            if direction == enums.Direction.forward_left:
                self.moveMotors(straightStep, enums.Direction.forward)
                self.moveMotors(sideStep, enums.Direction.forward_left)
            if direction == enums.Direction.forward_right:
                self.moveMotors(straightStep, enums.Direction.forward)
                self.moveMotors(sideStep, enums.Direction.forward_right)
            if direction == enums.Direction.backward_left:
                self.moveMotors(straightStep, enums.Direction.backward)
                self.moveMotors(sideStep, enums.Direction.backward_left)
            if direction == enums.Direction.backward_right:
                self.moveMotors(straightStep, enums.Direction.backward)
                self.moveMotors(sideStep, enums.Direction.backward_right)

    def gentleTurn(self, steps, direction):
        self.naturalTurn(steps, 3, 1, direction)

    def sharpTurn(self, steps, direction):
        self.naturalTurn(steps, 1, 3, direction)

    def tryCircle(self, direction):
        self.gentleTurn(2000, direction)

    def defaultCircle(self):
        self.tryCircle(enums.Direction.forward_right)

    def doRandomStep(self):

        # Random number between 15 and (503/2 + 15)
        numberOfSteps = int(509/4*np.random.random_sample() + 15)

        # Random number between 0 and 1
        randomNumber = np.random.random_sample()

        if(randomNumber < 0.4):
            self.moveMotors(numberOfSteps, enums.Direction.forward)
        else:
            # Random enums.Direction: left of right
            if(np.random.random_sample() < 0.5):
                direction = enums.Direction.forward_left
            else:
                direction = enums.Direction.forward_right


            if(randomNumber < 0.7):
                self.gentleTurn(numberOfSteps, direction)
            else:
                self.sharpTurn(numberOfSteps, direction)


