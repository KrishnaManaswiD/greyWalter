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
        self.sensors.setSensor(enums.SensorType.emergencySwitch, 1, 3) # Previous: 6
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
            print "Glubdhrtfarrrg! I only have touch, light and proximity sensors. Oh, well, and an emergency button that stops my limbs."
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
                return -1

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




    def getActuatorState(self, actuator_type, pos):
        
        if (actuator_type != enums.ActuatorType.led):
            print "Glubdhrtfarrrg! I only have LEDs!"
            print "\tHINT: check the type of actuator ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if (pos < 1 or pos > 4):
            print "Master, I only have four LEDs."
            print "\tHINT: check the actuator you want to set ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        return self.actuators.getActuatorState(actuator_type, pos)



    def setActuatorValue(self, actuator_type, pos, value):

        if(actuator_type != enums.ActuatorType.led):
            print "Glubdhrtfarrrg! I can only set my LEDs!"
            print "\tHINT: check the type of actuator ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if(pos < 1 or pos > 4):
            print "Master, I only have four LEDs."
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

        if numberOfBlinks < 1:
            print "Hey, if you ask me to blink a negative number of times we may create a hole in the universe!"
            print "\tHINT: check the number of blinks ;)"
            self.blinkLED(1, 3, 0.5)
            return -1

        if delay < 0:
            print "You, human, won't be able to see me blinking at the speed of light."
            print "\tHINT: check the delay ;)"
            self.blinkLED(1, 3, 0.5)
            return -1


        try:
            for y in range(0, len(positions)):

                if positions[y] < 0 or positions[y] > 4:
                    print "Master, I only have four LEDs."
                    print "\tHINT: check the actuator you want to set ;)"
                    self.blinkLED(1, 3, 0.5)
                    return -1

        except TypeError: # It's not an array but an integer

            if positions < 0 or positions > 4:
                print "Master, I only have four LEDs."
                print "\tHINT: check the actuator you want to set ;)"
                self.blinkLED(1, 3, 0.5)
                return -1



        previousStateLEDs = [ self.getActuatorState(enums.ActuatorType.led, x) for x in range(1, 5)]

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

    
        # The previous state of the LEDs are restored
        for x in range(1, 5):
            self.setActuatorValue(enums.ActuatorType.led, x, previousStateLEDs[x - 1])
            
        return 0


    def moveMotors_oldVersion(self, steps, direction):

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

            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "[TORTOISE PAUSED]"
                    
                break;

            if self.getStateTortoise() == enums.State.paused:
                self.setStateTortoise(enums.State.running)
                print "[TORTOISE RESUMED]"
             

            if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:

                self.A.backward(int(self.delay) / 1000.00, 1)

            if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                self.B.backward(int(self.delay) / 1000.00, 1)

            if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                self.A.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)

            if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                self.B.forward(int(self.delay) / 1000.00, numberOfstepsCommanded)



        if self.getStateTortoise() == enums.State.running and numberOfStepsRemaining > 0:

                    if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:

                        self.A.backward(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                        self.B.backward(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                        self.A.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)

                    if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                        self.B.forward(int(self.delay) / 1000.00, numberOfStepsRemaining)


        self.A.stopMotors()
        self.B.stopMotors()

        return 0






    def moveMotors_improved1_oldversion(self, steps, direction):

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


        numberOfstepsCommanded = int(50)
        numberOfLoops = steps/numberOfstepsCommanded
        numberOfStepsRemaining = steps % numberOfstepsCommanded

        
       # motorBprocess = Process(target=self.B.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))

        for x in range(0,numberOfLoops):

            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:
                    self.setStateTortoise(enums.State.paused)
                    print "[TORTOISE PAUSED]"
                    
                break;

            if self.getStateTortoise() == enums.State.paused:
                self.setStateTortoise(enums.State.running)
                print "[TORTOISE RESUMED]"
             
            motorAprocess_backward = Process(target=self.A.backward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
            motorBprocess_backward = Process(target=self.B.backward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
            motorAprocess_forward = Process(target=self.A.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))
            motorBprocess_forward = Process(target=self.B.forward, args=(int(self.delay) / 1000.00, numberOfstepsCommanded))


            if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:

                motorAprocess_backward.start()

            if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                motorBprocess_backward.start()

            if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                motorAprocess_forward.start()

            if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                motorBprocess_forward.start()


            if motorAprocess_forward.is_alive():
                motorAprocess_forward.join()

            if motorBprocess_forward.is_alive():
                motorBprocess_forward.join()

            if motorAprocess_backward.is_alive():
                motorAprocess_backward.join()

            if motorBprocess_backward.is_alive():
                motorBprocess_backward.join()


        self.A.stopMotors()
        self.B.stopMotors()

        return 0




    def moveMotors(self, stepsLeft, stepsRight, direction):

            if( direction != enums.Direction.backward_right and direction != enums.Direction.backward_left and 
            direction != enums.Direction.forward_right and direction != enums.Direction.forward_left and direction != enums.Direction.forward and direction != enums.Direction.backward ) :

                    print "Hey, my master! I can only move backward or forward, and either left or right."
                    print "\tHINT: check the direction ;)"
                    self.blinkLED(1, 3, 0.5)
                    return -1

            if(stepsLeft < 0 or stepsRight < 0):
                    print "How am I going to move a negative number of steps? I can't travel back in time!"
                    print "\tHINT: check the number of steps ;)"
                    self.blinkLED(1, 3, 0.5)
                    return -1

            # If a stop command has been sent, the turtle will stop its movement
            if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                if self.getStateTortoise() == enums.State.running:

                    self.setStateTortoise(enums.State.paused)
                    print "[TORTOISE PAUSED]"

            else:
                if self.getStateTortoise() == enums.State.paused:
                        self.setStateTortoise(enums.State.running)
                        print "[TORTOISE RESUMED]"

                motorAprocess_backward = Process(target=self.A.backward, args=(int(self.delay) / 1000.00, stepsRight))
                motorBprocess_backward = Process(target=self.B.backward, args=(int(self.delay) / 1000.00, stepsLeft))
                motorAprocess_forward = Process(target=self.A.forward, args=(int(self.delay) / 1000.00, stepsLeft))
                motorBprocess_forward = Process(target=self.B.forward, args=(int(self.delay) / 1000.00, stepsRight))


                if direction == enums.Direction.backward_left or direction == enums.Direction.backward or direction == enums.Direction.counterClockwise:
                    
                    motorAprocess_backward.start()

                if direction == enums.Direction.backward_right or direction == enums.Direction.backward or direction == enums.Direction.clockwise:

                    motorBprocess_backward.start()

                if direction == enums.Direction.forward_right or direction == enums.Direction.forward or direction == enums.Direction.clockwise:

                    motorAprocess_forward.start()

                if direction == enums.Direction.forward_left or direction == enums.Direction.forward or direction == enums.Direction.counterClockwise:

                    motorBprocess_forward.start()


                # The main loop pools the emergencySwitch
                while motorAprocess_backward.is_alive() or motorBprocess_backward.is_alive() or motorAprocess_forward.is_alive() or motorBprocess_forward.is_alive():

                    # If a stop command has been sent, the turtle will stop its movement
                    if self.getSensorData(enums.SensorType.emergencySwitch, 1) == 0:

                        if self.getStateTortoise() == enums.State.running:

                            self.setStateTortoise(enums.State.paused)
                            print "[TORTOISE PAUSED]"

                            if motorAprocess_backward.is_alive():
                                motorAprocess_backward.terminate()
                                motorAprocess_backward.join()

                            if motorBprocess_backward.is_alive():
                                motorBprocess_backward.terminate()
                                motorBprocess_backward.join()

                            if motorAprocess_forward.is_alive():
                                motorAprocess_forward.terminate()
                                motorAprocess_forward.join()

                            if motorBprocess_forward.is_alive():
                                motorBprocess_forward.terminate()
                                motorBprocess_forward.join()
                            
                    elif self.getStateTortoise() == enums.State.paused:
                        self.setStateTortoise(enums.State.running)
                        print "[TORTOISE RESUMED]"


                    time.sleep(0.5)


            self.A.stopMotors()
            self.B.stopMotors()

            return 0



    def moveForward(self, steps):

        return self.move(steps, steps, enums.Direction.forward)



    def moveBackward(self, steps):

        return self.move(steps, steps, enums.Direction.backward)




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


