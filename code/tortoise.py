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
from multiprocessing import Process


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

        GPIO.setwarnings(False)

#        self.lock = threading.RLock()

        isLightCalibrated = False
        lowerBoundLight = 0
        upperBoundLight = 0

        # Previous: [4, 17, 23, 24, 27, 22, 18, 5]
        motorPins = [13, 6, 5, 7, 20, 10, 9,11]

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


        self.sensors.setSensor(enums.SensorType.light, 1, 17) # Previous: 16
        self.sensors.setSensor(enums.SensorType.light, 2, 4) # Previous: 2
        self.sensors.setSensor(enums.SensorType.emergencySwitch, 1, 3) # Previous: 6
        self.sensors.setSensor(enums.SensorType.touch, 1, 27) # Previous: 8
        self.sensors.setSensor(enums.SensorType.touch, 2, 2) # Previous: 13
        self.sensors.setSensor(enums.SensorType.touch, 3, 18) # Previous: 7
        self.sensors.setSensor(enums.SensorType.proximity, 1, 19) # Previous: 10
        self.sensors.setSensor(enums.SensorType.proximity, 2, 21) # Previous: 11
        self.sensors.setSensor(enums.SensorType.proximity, 3, 22) # Previous: x
        self.sensors.setSensor(enums.SensorType.proximity, 4, 26) # Previous: x

        self.actuators.initActuator(enums.ActuatorType.led,1, 8) # Previous: 19
        self.actuators.initActuator(enums.ActuatorType.led,2, 16) # Previous: 26
        self.actuators.initActuator(enums.ActuatorType.led,3, 25) # Previous: x
        self.actuators.initActuator(enums.ActuatorType.led,4, 12) # Previous: x

        #print "light sensor value:"
        #print self.sensors.readSensor(enums.SensorType.light, 1)
        #if not isLightCalibrated:
                #self.calibrateLight()

#        try:
#             thread.start_new_thread(self.pauseAndResume, ())
#        except:
#            print "Error: unable to start thread"

        print(chr(27) + "[2J")
        print "Tortoise alive! Press the pause/resume button to set me going."
        while self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:
            time.sleep(0.1)

        print "[TORTOISE RUNNING]"

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

        if (sensor_type == enums.SensorType.touch):

            if (pos < 1 or pos > 3):

                print "Master, I only have three touch sensors."
                print "\tHINT: check the position of the sensor you want to set ;)"
                self.blinkLED(1, 3, 0.5)
                return -1

        elif (sensor_type == enums.SensorType.light):

            if (pos != 1 and pos!=2):

                print "Master, I only have one light sensor."
                print "\tHINT: check the position of the sensor you want to set ;)"
                self.blinkLED(1, 3, 0.5)
                return -1

        elif (sensor_type == enums.SensorType.proximity):

            if (pos < 1 or pos > 4):

                print "Master, I only have two proximity sensors."
                print "\tHINT: check the position of the sensor you want to set ;)"
                self.blinkLED(1, 3, 0.5)
                return -1

        elif (sensor_type == enums.SensorType.emergencySwitch):

            if (pos != 1):

                print "Master, I only have two touch sensors."
                print "\tHINT: check the position of the sensor you want to set ;)"
                self.blinkLED(1, 3, 0.5)
                return -1

        else:
            print "Glubdhrtfarrrg! I only have touch, light and proximity sensors. Oh, well, and an eergency button that stops my limbs."
            print "\tHINT: check the type of sensor ;)"
            self.blinkLED(1, 3, 0.5)
            return -1


        value = self.sensors.readSensor(sensor_type,pos)

        if sensor_type == enums.SensorType.light:
            return value
            if (upperBoundLight - lowerBoundLight) == 0:
                print "I am blind!"
                print "\tHINT: the light sensor seems to be not calibrated ;)"
                self.blinkLED(1, 3, 0.5)
                #return -1

            # Scale 
            lightVal = int(9 - round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9)))

            if lightVal < 0:
                print "I am blind!"
                print "\tHINT: the light sensor seems to be not calibrated ;)"
                self.blinkLED(1, 3, 0.5)
                return -1

            return lightVal

        elif sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencySwitch:

            return value % 2

        else:
            return value


    def setActuatorValue(self, actuator_type, pos, value):

        if(actuator_type != enums.ActuatorType.led):
            print "Glubdhrtfarrrg! I can only set my LEDs!"
            print "\tHINT: check the type of actuator ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if(pos < 1 or pos > 2):
            print "Master, I only have two LEDs."
            print "\tHINT: check the actuator you want to set ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if(value != 0 and value != 1):
            print "In binary code, we only have 0s and 1s."
            print "\tHINT: check the value you want to set ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        self.actuators.setActuator(actuator_type, pos, value)
        return 0


    def blinkLED(self, positions, numberOfBlinks, delay):

        for x in range(0, numberOfBlinks):

            try:
                for y in range(0, len(positions)):
                    self.actuators.setActuator(enums.ActuatorType.led, positions[y], 1)

                time.sleep(delay)

                for y in range(0, len(positions)):
                    self.actuators.setActuator(enums.ActuatorType.led, positions[y], 0)

            except TypeError: # It's not an array but an integer

                self.actuators.setActuator(enums.ActuatorType.led, positions, 1)
                time.sleep(delay)
                self.actuators.setActuator(enums.ActuatorType.led, positions, 0)

            # TODO: remove if threaded
            if x != (numberOfBlinks - 1):
                time.sleep(delay)



    def moveMotors(self, steps, direction):

        if( direction != enums.Direction.backward_right and direction != enums.Direction.backward_left and 
            direction != enums.Direction.forward_right and direction != enums.Direction.forward_left and direction != enums.Direction.forward and direction != enums.Direction.backward ) :
            print "Hey, my master! I can only move backward or forward, and either left or right."
            print "\tHINT: check the direction ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if(steps < 0):
            print "How am I going to move a negative number of steps? I can't travel back in time!"
            print "\tHINT: check the number of steps ;)"
            self.blinkLED(1, 3, 0.5)
            return -1


        numberOfstepsCommanded = int(1)
        numberOfLoops = steps/numberOfstepsCommanded
        numberOfStepsRemaining = steps % numberOfstepsCommanded

        
       # motorBprocess = Process(target=self.B.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))

        for x in range(0,numberOfLoops):

            motorAprocess = Process(target=self.A.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
            motorBprocess = Process(target=self.B.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))

            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "[TORTOISE PAUSED]"
                    
                break;

            if self.getStateTortoise() == enums.State.paused:
                self.setStateTortoise(enums.State.running)
                print "[TORTOISE RESUMED]"
             
            #print "Before starting"

            if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:

                self.A.backwards(int(self.delay) / 1000.00, numberOfstepsCommanded)

            if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                self.B.backwards(int(self.delay) / 1000.00, numberOfstepsCommanded)

            if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                #motorAprocess.start()
                self.A.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)

            if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                #motorBprocess.start()
                self.B.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)

            if motorAprocess.is_alive() and motorBprocess.is_alive():
                    motorAprocess.join()
                    motorBprocess.join()

            print "HERE"

        if numberOfStepsRemaining > 0:
            
            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "[TORTOISE PAUSED]"

                else:

                    if self.getStateTortoise() == enums.State.paused:
                        self.setStateTortoise(enums.State.running)
                        print "[TORTOISE RESUMED]"


                    if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:

                        self.A.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                        self.B.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                        self.A.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                        self.B.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)


        self.A.stopMotors()
        self.B.stopMotors()

        return 0



    def naturalTurn(self, totalSteps, straightStep, sideStep, direction):

        if( direction != enums.Direction.backward_right and direction != enums.Direction.backward_left and 
            direction != enums.Direction.forward_right and direction != enums.Direction.forward_left ) :
            print "Hey, my master! I can only turn backward or forward, and either left or right."
            print "\tHINT: check the direction ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if(totalSteps < 0 or straightStep < 0 or sideStep < 0):
            print "How am I going to move a negative number of steps? I can't travel back in time!"
            print "\tHINT: check the number of steps ;)"
            self.blinkLED(1, 3, 0.5)
            return -1


        if (straightStep + sideStep) > totalSteps: 
            print "I can't move as you wish."
            print "\tHINT: check the number of straight steps, side steps and total steps ;)"
            self.blinkLED(1, 3, 0.5)
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

        return 0


    def gentleTurn(self, steps, direction):

        return self.naturalTurn(steps, 3, 1, direction)


    def sharpTurn(self, steps, direction):

        return self.naturalTurn(steps, 1, 3, direction)


    def tryCircle(self, direction):

        if( direction != enums.Direction.clockwise and direction != enums.Direction.counterClockwise):
            print "Hey, my master! I can only rotate clockwise or counterclockwise."
            print "\tHINT: check the direction ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        return self.gentleTurn(2000, direction)


    def defaultCircle(self):
        self.tryCircle(enums.Direction.forward_right)


    # TODO: improve random motion
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


