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
        motorPins = [13, 6, 5, 7, 20, 10, 9, 11]
        ledPins = [8, 16, 25, 12]

        # CREATING FILE WITH PID

        # PID of process
        pid = os.getpid()

        # ~/.tortoise_pids/
        directory = os.path.expanduser("~") + "/.tortoise_pids/"

        # Filename: [PID].pid
        f = open(directory + str(pid) + ".pid", "w")

        # First line: motor pins
        f.write(str(motorPins[0]) + " " + str(motorPins[1]) + " " + str(motorPins[2]) + " " + str(motorPins[3]) + " " + str(motorPins[4]) + " " + str(motorPins[5]) + " " + str(motorPins[6]) + " " + str(motorPins[7]) + "\n")

        # Second line: LED pins
        f.write(str(ledPins[0]) + " " + str(ledPins[1]) + " " + str(ledPins[2]) + " " + str(ledPins[3]) + "\n")

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
        self.sensors.setSensor(enums.SensorType.emergencyStop, 1, 3) # Previous: 6
        self.sensors.setSensor(enums.SensorType.touch, 1, 27) # Previous: 8
        self.sensors.setSensor(enums.SensorType.touch, 2, 2) # Previous: 13
        self.sensors.setSensor(enums.SensorType.touch, 3, 18) # Previous: 7
        self.sensors.setSensor(enums.SensorType.proximity, 1, 19) # Previous: 10
        self.sensors.setSensor(enums.SensorType.proximity, 2, 21) # Previous: 11
        self.sensors.setSensor(enums.SensorType.proximity, 3, 22) # Previous: x
        self.sensors.setSensor(enums.SensorType.proximity, 4, 26) # Previous: x

        self.actuators.initActuator(enums.ActuatorType.led,1, ledPins[0]) # Previous: 19
        self.actuators.initActuator(enums.ActuatorType.led,2, ledPins[1]) # Previous: 26
        self.actuators.initActuator(enums.ActuatorType.led,3, ledPins[2]) # Previous: x
        self.actuators.initActuator(enums.ActuatorType.led,4, ledPins[3]) # Previous: x

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
        while self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:
            time.sleep(0.1)

        print "[TORTOISE RUNNING]"

        self.state = enums.State.running

#    def pauseAndResume(self):

#        while True:
#
#            if self.getSensorData(enums.SensorType.emergencyStop, 1):
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

        raw_input("Press enter to take a reading at normal light levels.")
        #lowerBoundLight = max(self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2))
        lowerBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
        #print "Light in normal conditions is: ", lowerBoundLight

        raw_input("Now please place a light source in front of the light sensor and press enter.")
        #upperBoundLight = min((self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2)))
        upperBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
#        print "Light when there is a light source is:", upperBoundLight

        isLightCalibrated = True

        print("Calibration complete!")



    def getSensorData(self, sensor_type, position):

        if (sensor_type == enums.SensorType.touch):

            if (position < 1 or position > 3):

                print "You've asked for a touch sensor that doesn't exist."
                print "\tHINT: check the position of the sensor you want to set."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

        elif (sensor_type == enums.SensorType.light):

            if (position != 1 and position!=2):

                print "I only have one light sensor."
                print "\tHINT: check the position of the sensor you want to set."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

        elif (sensor_type == enums.SensorType.proximity):

            if (position < 1 or position > 4):

                print "You've asked for a proximity sensor that doesn't exist."
                print "\tHINT: check the position of the sensor you want to set."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

        elif (sensor_type == enums.SensorType.emergencyStop):

            if (position != 1):

                print "You've asked for a emergency stop that doesn't exist."
                print "\tHINT: check the position of the sensor you want to set."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

        else:
                print "You've asked for a sensor that doesn't exist."
                print "\tHINT: check the type of the sensor you want to read."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1


        value = self.sensors.readSensor(sensor_type, position)

        if sensor_type == enums.SensorType.light:
            return value
            if (upperBoundLight - lowerBoundLight) == 0:
                print "The light sensor hasn't been calibrated properly. Try calibrating again."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

            # Scale 
            lightVal = int(9 - round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9)))

            if lightVal < 0:
                print "The light sensor hasn't been calibrated properly. Try calibrating again."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1

            return lightVal

        elif sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencyStop:

            return value % 2

        else:
            return value




    def getLEDState(self, position):
        
        if (position < 1 or position > 4):
            print "You've asked for an LED that doesn't exist."
            print "\tHINT: check the position of the LED you want to set."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        return self.actuators.getActuatorState(enums.ActuatorType.led, position)



    def setLEDValue(self, position, value):

        if(position < 1 or position > 4):
            print "You've asked for an LED that doesn't exist."
            print "\tHINT: check the position of the LED you want to set."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        if(value != 0 and value != 1):
            print "In binary code, we only have 0s and 1s."
            print "\tHINT: check the value you want to set (0 = OFF, 1 = ON)."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        self.actuators.setActuator(enums.ActuatorType.led, position, value)
        return 0



    def blinkLEDs(self, positions, numberOfBlinks, delay, blocking = True):

        if numberOfBlinks < 0:
            print "I can't blink a negative number of times!"
            print "\tHINT: check the number of blinks."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        if numberOfBlinks == 0:
            print "Do you want me to blink or not?"
            print "\tHINT: check the number of blinks."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        if delay < 0:
            print "I can't blink that fast."
            print "\tHINT: check the delay."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1


        try:
            for y in range(0, len(positions)):

                if positions[y] < 0 or positions[y] > 4:
                    print "You've asked for an LED that doesn't exist."
                    print "\tHINT: check the position of the LED you want to set."
                    self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                    return -1

        except TypeError: # It's not an array but an integer

            if positions < 0 or positions > 4:
                print "You've asked for an LED that doesn't exist."
                print "\tHINT: check the position of the LED you want to set."
                self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
                return -1



        previousStateLEDs = [ self.getLEDState(x) for x in range(1, 5) ]

        cont = True

        # Infinite loop to "stop" the execution of the program and keep blinkind the LEDs
        while cont:

            for x in range(0, numberOfBlinks):

                try:
                    for y in range(0, len(positions)):

                        self.actuators.setActuator(enums.ActuatorType.led, positions[y], 1)

                    time.sleep(delay)

                    for y in range(0, len(positions)):
                        self.actuators.setActuator(enums.ActuatorType.led, positions[y], 0)

                    time.sleep(delay)

                except TypeError: # It's not an array but an integer

                    self.actuators.setActuator(enums.ActuatorType.led, positions, 1)
                    time.sleep(delay)
                    self.actuators.setActuator(enums.ActuatorType.led, positions, 0)
                    time.sleep(delay)

                
            cont = blocking


        
        # If it doesn't block, the previous state of the LEDs is restored
        for x in range(1, 5):
            self.setLEDValue(x, previousStateLEDs[x - 1])
            
        return 0


#    def moveMotors_oldVersion(self, steps, direction):

#        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and 
#            direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left and direction != enums.Direction.forwards and direction != enums.Direction.backwards ) :
#            print "Hey, my master! I can only move backwards or forwards, and either left or right."
#            print "\tHINT: check the direction ;)"
#            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
#            return -1

#        if(steps < 0):
#            print "How am I going to move a negative number of steps? I can't travel back in time!"
#            print "\tHINT: check the number of steps ;)"
#            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
#            return -1


#        numberOfstepsCommanded = int(1)
#        numberOfLoops = steps/numberOfstepsCommanded
#        numberOfStepsRemaining = steps % numberOfstepsCommanded

#        
#       # motorBprocess = Process(target=self.B.forwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))

#        for x in range(0,numberOfLoops):

#            # If a stop command has been sent, the turtle will stop its movement
#            if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

#                if self.getStateTortoise() == enums.State.running:
#                    self.setStateTortoise(enums.State.paused)
#                    print "[TORTOISE PAUSED]"
#                    
#                break;

#            if self.getStateTortoise() == enums.State.paused:
#                self.setStateTortoise(enums.State.running)
#                print "[TORTOISE RESUMED]"
#             

#            if direction == enums.Direction.backwards_left or direction == enums.Direction.backwards or direction == enums.Direction.counterClockwise:

#                self.A.backwards(int(self.delay) / 1000.00, 1)

#            if direction == enums.Direction.backwards_right or direction == enums.Direction.backwards or direction == enums.Direction.clockwise:

#                self.B.backwards(int(self.delay) / 1000.00, 1)

#            if direction == enums.Direction.forwards_right or direction == enums.Direction.forwards or direction == enums.Direction.clockwise:

#                self.A.forwards(int(self.delay) / 1000.00, numberOfstepsCommanded)

#            if direction == enums.Direction.forwards_left or direction == enums.Direction.forwards or direction == enums.Direction.counterClockwise:

#                self.B.forwards(int(self.delay) / 1000.00, numberOfstepsCommanded)



#        if self.getStateTortoise() == enums.State.running and numberOfStepsRemaining > 0:

#                    if direction == enums.Direction.backwards_left or direction == enums.Direction.backwards or direction == enums.Direction.counterClockwise:

#                        self.A.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)

#                    if direction == enums.Direction.backwards_right or direction == enums.Direction.backwards or direction == enums.Direction.clockwise:

#                        self.B.backwards(int(self.delay) / 1000.00, numberOfStepsRemaining)

#                    if direction == enums.Direction.forwards_right or direction == enums.Direction.forwards or direction == enums.Direction.clockwise:

#                        self.A.forwards(int(self.delay) / 1000.00, numberOfStepsRemaining)

#                    if direction == enums.Direction.forwards_left or direction == enums.Direction.forwards or direction == enums.Direction.counterClockwise:

#                        self.B.forwards(int(self.delay) / 1000.00, numberOfStepsRemaining)


#        self.A.stopMotors()
#        self.B.stopMotors()

#        return 0






#    def moveMotors_improved1_oldversion(self, steps, direction):

#        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and 
#            direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left and direction != enums.Direction.forwards and direction != enums.Direction.backwards ) :
#            print "Hey, my master! I can only move backwards or forwards, and either left or right."
#            print "\tHINT: check the direction ;)"
#            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
#            return -1

#        if(steps < 0):
#            print "How am I going to move a negative number of steps? I can't travel back in time!"
#            print "\tHINT: check the number of steps ;)"
#            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
#            return -1


#        numberOfstepsCommanded = int(50)
#        numberOfLoops = steps/numberOfstepsCommanded
#        numberOfStepsRemaining = steps % numberOfstepsCommanded

#        
#       # motorBprocess = Process(target=self.B.forwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))

#        for x in range(0,numberOfLoops):

#            # If a stop command has been sent, the turtle will stop its movement
#            if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

#                if self.getStateTortoise() == enums.State.running:
#                    self.setStateTortoise(enums.State.paused)
#                    print "[TORTOISE PAUSED]"
#                    
#                break;

#            if self.getStateTortoise() == enums.State.paused:
#                self.setStateTortoise(enums.State.running)
#                print "[TORTOISE RESUMED]"
#             
#            motorAprocess_backwards = Process(target=self.A.backwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
#            motorBprocess_backwards = Process(target=self.B.backwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
#            motorAprocess_forwards = Process(target=self.A.forwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
#            motorBprocess_forwards = Process(target=self.B.forwards, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))


#            if direction == enums.Direction.backwards_left or direction == enums.Direction.backwards or direction == enums.Direction.counterClockwise:

#                motorAprocess_backwards.start()

#            if direction == enums.Direction.backwards_right or direction == enums.Direction.backwards or direction == enums.Direction.clockwise:

#                motorBprocess_backwards.start()

#            if direction == enums.Direction.forwards_right or direction == enums.Direction.forwards or direction == enums.Direction.clockwise:

#                motorAprocess_forwards.start()

#            if direction == enums.Direction.forwards_left or direction == enums.Direction.forwards or direction == enums.Direction.counterClockwise:

#                motorBprocess_forwards.start()


#            if motorAprocess_forwards.is_alive():
#                motorAprocess_forwards.join()

#            if motorBprocess_forwards.is_alive():
#                motorBprocess_forwards.join()

#            if motorAprocess_backwards.is_alive():
#                motorAprocess_backwards.join()

#            if motorBprocess_backwards.is_alive():
#                motorBprocess_backwards.join()


#        self.A.stopMotors()
#        self.B.stopMotors()

#        return 0




    def moveMotors(self, stepsLeft, stepsRight, direction):

        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and 
        direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left and direction != enums.Direction.forwards and direction != enums.Direction.backwards ) :

            print "I can only move backwards or forwards, and either left or right."
            print "\tHINT: check the direction."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        if(stepsLeft < 0 or stepsRight < 0):
            print "I can't move a negative number of steps!"
            print "\tHINT: check the number of steps."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        # If a stop command has been sent, the turtle will stop its movement
        if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

            if self.getStateTortoise() == enums.State.running:

                self.setStateTortoise(enums.State.paused)
                print "[TORTOISE PAUSED]"

        else:
            if self.getStateTortoise() == enums.State.paused:
                    self.setStateTortoise(enums.State.running)
                    print "[TORTOISE RESUMED]"

            motorAprocess_backwards = Process(target=self.A.backwards, args=(int(self.delay) / 1000.00, stepsRight))
            motorBprocess_backwards = Process(target=self.B.backwards, args=(int(self.delay) / 1000.00, stepsLeft))
            motorAprocess_forwards = Process(target=self.A.forwards, args=(int(self.delay) / 1000.00, stepsLeft))
            motorBprocess_forwards = Process(target=self.B.forwards, args=(int(self.delay) / 1000.00, stepsRight))


            if direction == enums.Direction.backwards_left or direction == enums.Direction.backwards or direction == enums.Direction.counterClockwise:
                
                motorAprocess_backwards.start()

            if direction == enums.Direction.backwards_right or direction == enums.Direction.backwards or direction == enums.Direction.clockwise:

                motorBprocess_backwards.start()

            if direction == enums.Direction.forwards_right or direction == enums.Direction.forwards or direction == enums.Direction.clockwise:

                motorAprocess_forwards.start()

            if direction == enums.Direction.forwards_left or direction == enums.Direction.forwards or direction == enums.Direction.counterClockwise:

                motorBprocess_forwards.start()


            # The main loop pools the emergencyStop
            while motorAprocess_backwards.is_alive() or motorBprocess_backwards.is_alive() or motorAprocess_forwards.is_alive() or motorBprocess_forwards.is_alive():

                # If a stop command has been sent, the turtle will stop its movement
                if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

                    if self.getStateTortoise() == enums.State.running:

                        self.setStateTortoise(enums.State.paused)
                        print "[TORTOISE PAUSED]"

                        if motorAprocess_backwards.is_alive():
                            motorAprocess_backwards.terminate()
                            motorAprocess_backwards.join()

                        if motorBprocess_backwards.is_alive():
                            motorBprocess_backwards.terminate()
                            motorBprocess_backwards.join()

                        if motorAprocess_forwards.is_alive():
                            motorAprocess_forwards.terminate()
                            motorAprocess_forwards.join()

                        if motorBprocess_forwards.is_alive():
                            motorBprocess_forwards.terminate()
                            motorBprocess_forwards.join()
                        
                elif self.getStateTortoise() == enums.State.paused:
                    self.setStateTortoise(enums.State.running)
                    print "[TORTOISE RESUMED]"


                time.sleep(0.5)


        self.A.stopMotors()
        self.B.stopMotors()

        return 0



    def moveForwards(self, steps):

        return self.moveMotors(steps, steps, enums.Direction.forwards)



    def moveBackwards(self, steps):

        return self.moveMotors(steps, steps, enums.Direction.backwards)




    def naturalTurn(self, totalSteps, straightStep, sideStep, direction):

        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and 
            direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left ) :
            print "I can only turn backwards or forwards, and either left or right."
            print "\tHINT: check the direction."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        if(totalSteps < 0 or straightStep < 0 or sideStep < 0):
            print "How am I going to move a negative number of steps? I can't travel back in time!"
            print "\tHINT: check the number of steps."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1


        if (straightStep + sideStep) > totalSteps: 
#            print "I can't move as you wish."
#            print "\tHINT: check the number of straight steps, side steps and total steps ;)"
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1


        for x in range(0, int(totalSteps/(straightStep+sideStep))):
            if direction == enums.Direction.forwards_left:
                self.moveMotors(straightStep, enums.Direction.forwards)
                self.moveMotors(sideStep, enums.Direction.forwards_left)
            if direction == enums.Direction.forwards_right:
                self.moveMotors(straightStep, enums.Direction.forwards)
                self.moveMotors(sideStep, enums.Direction.forwards_right)
            if direction == enums.Direction.backwards_left:
                self.moveMotors(straightStep, enums.Direction.backwards)
                self.moveMotors(sideStep, enums.Direction.backwards_left)
            if direction == enums.Direction.backwards_right:
                self.moveMotors(straightStep, enums.Direction.backwards)
                self.moveMotors(sideStep, enums.Direction.backwards_right)

        return 0


    def gentleTurn(self, steps, direction):

        return self.naturalTurn(steps, 3, 1, direction)


    def sharpTurn(self, steps, direction):

        return self.naturalTurn(steps, 1, 3, direction)


    def tryCircle(self, direction):

        if( direction != enums.Direction.clockwise and direction != enums.Direction.counterClockwise):
            print "I can only rotate clockwise or counterclockwise."
            print "\tHINT: check the direction."
            self.blinkLEDs([1, 2, 3, 4], 3, 0.2)
            return -1

        return self.gentleTurn(2000, direction)


    def defaultCircle(self):
        self.tryCircle(enums.Direction.forwards_right)


    # TODO: improve random motion
    def doRandomMovement(self):

        # Random number between 15 and (503/2 + 15)
        numberOfSteps = int(509/4*np.random.random_sample() + 15)

        # Random number between 0 and 1
        randomNumber = np.random.random_sample()

        if(randomNumber < 0.4):
            self.moveMotors(numberOfSteps, enums.Direction.forwards)
        else:
            # Random enums.Direction: left of right
            if(np.random.random_sample() < 0.5):
                direction = enums.Direction.forwards_left
            else:
                direction = enums.Direction.forwards_right


            if(randomNumber < 0.7):
                self.gentleTurn(numberOfSteps, direction)
            else:
                self.sharpTurn(numberOfSteps, direction)


