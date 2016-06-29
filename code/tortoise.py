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
import messages

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
        self.minDelayMotors = 2
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

        self.actuators.initActuator(enums.ActuatorType.led, 1, ledPins[0]) # Previous: 19
        self.actuators.initActuator(enums.ActuatorType.led, 2, ledPins[1]) # Previous: 26
        self.actuators.initActuator(enums.ActuatorType.led, 3, ledPins[2]) # Previous: x
        self.actuators.initActuator(enums.ActuatorType.led, 4, ledPins[3]) # Previous: x

        #print "light sensor value:"
        #print self.sensors.readSensor(enums.SensorType.light, 1)
        #if not isLightCalibrated:
                #self.calibrateLight()

#        try:
#             thread.start_new_thread(self.pauseAndResume, ())
#        except:
#            print "Error: unable to start thread"

        messages.printMessage('greetings')
        while self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:
            time.sleep(0.1)

        messages.printMessage('running')

        self.state = enums.State.running


    def getStateTortoise(self):
        return self.state


    def setStateTortoise(self, toState):
        self.state = toState


    def calibrateLight(self):
        global lowerBoundLight, upperBoundLight, isLightCalibrated

        messages.printMessage('calibration_ambient')
        raw_input()
        #lowerBoundLight = max(self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2))
        lowerBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
        #print "Light in normal conditions is: ", lowerBoundLight

        messages.printMessage('calibration_light_source')
        raw_input()
        #upperBoundLight = min((self.sensors.readSensor(enums.SensorType.light, 1), self.sensors.readSensor(enums.SensorType.light, 2)))
        upperBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)
#        print "Light when there is a light source is:", upperBoundLight

        isLightCalibrated = True

        messages.printMessage('calibration_complete')



    def getSensorData(self, sensor_type, position):

        if (sensor_type == enums.SensorType.touch):

            if (position < 1 or position > 3):

                messages.printMessage('bad_touch_sensor')
                self.blinkLEDs_error()
                return -1

        elif (sensor_type == enums.SensorType.light):

            if (position != 1 and position!=2):

                messages.printMessage('bad_light_sensor')
                self.blinkLEDs_error()
                return -1

        elif (sensor_type == enums.SensorType.proximity):

            if (position < 1 or position > 4):

                messages.printMessage('bad_proximity_sensor')
                self.blinkLEDs_error()
                return -1

        elif (sensor_type == enums.SensorType.emergencyStop):

            if (position != 1):

                messages.printMessage('bad_emergency_sensor')
                self.blinkLEDs_error()
                return -1

        else:
                messages.printMessage('bad_sensor')
                self.blinkLEDs_error()
                return -1


        value = self.sensors.readSensor(sensor_type, position)

        if sensor_type == enums.SensorType.light:
            return value
            if (upperBoundLight - lowerBoundLight) == 0:
                messages.printMessage('no_calibration')
                self.blinkLEDs_error()
                return -1

            # Scale
            lightVal = int(9 - round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9)))

            if lightVal < 0:
                messages.printMessage('no_calibration')
                self.blinkLEDs_error()
                return -1

            return lightVal

        elif sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencyStop:

            return value % 2

        else:
            return value




    def getLEDValue(self, position):

        if (position < 1 or position > 4):
            messages.printMessage('bad_LED')
            self.blinkLEDs_error()
            return -1

        return self.actuators.getActuatorValue(enums.ActuatorType.led, position)



    def setLEDValue(self, position, value):

        if(position < 1 or position > 4):
            messages.printMessage('bad_LED')
            self.blinkLEDs_error()
            return -1

        if(value != 0 and value != 1):
            messages.printMessage('bad_LED_value')
            self.blinkLEDs_error()
            return -1

        self.actuators.setActuatorValue(enums.ActuatorType.led, position, value)
        return 0



    def blinkLEDs(self, positions, numberOfBlinks, delay, blocking = False):

        if numberOfBlinks < 0:
            messages.printMessage('blinks_negative')
            self.blinkLEDs_error()
            return -1

        if numberOfBlinks == 0:
            messages.printMessage('blinks_zero')
            self.blinkLEDs_error()
            return -1

        if delay < 0:
            messages.printMessage('blinking_fast')
            self.blinkLEDs_error()
            return -1


        try:
            for y in range(0, len(positions)):

                if positions[y] < 0 or positions[y] > 4:
                    messages.printMessage('bad_LED')
                    self.blinkLEDs_error()
                    return -1

        except TypeError: # It's not an array but an integer

            if positions < 0 or positions > 4:
                messages.printMessage('bad_LED')
                self.blinkLEDs_error()
                return -1



        previousStateLEDs = [ self.getLEDValue(x) for x in range(1, 5) ]

        cont = True

        # Infinite loop to "stop" the execution of the program and keep blinkind the LEDs
        while cont:

            for x in range(0, numberOfBlinks):

                try:
                    for y in range(0, len(positions)):

                        self.actuators.setActuatorValue(enums.ActuatorType.led, positions[y], 1)

                    time.sleep(delay)

                    for y in range(0, len(positions)):
                        self.actuators.setActuatorValue(enums.ActuatorType.led, positions[y], 0)

                    time.sleep(delay)

                except TypeError: # It's not an array but an integer

                    self.actuators.setActuatorValue(enums.ActuatorType.led, positions, 1)
                    time.sleep(delay)
                    self.actuators.setActuatorValue(enums.ActuatorType.led, positions, 0)
                    time.sleep(delay)


            cont = blocking



        # If it doesn't block, the previous state of the LEDs is restored
        for x in range(1, 5):
            self.setLEDValue(x, previousStateLEDs[x - 1])

        return 0


    def blinkLEDs_error(self):
        self.blinkLEDs([1, 2, 3, 4], 3, 0.2, blocking = True)



    def moveMotors(self, stepsWheelA, stepsWheelB, delayWheelA, delayWheelB, direction):

        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left and direction != enums.Direction.forwards and direction != enums.Direction.backwards  and direction != enums.Direction.clockwise and direction != enums.Direction.counterClockwise  ) :

            messages.printMessage('bad_direction')
            self.blinkLEDs_error()
            return -1

        if(stepsWheelA < 0 or stepsWheelB < 0):
            messages.printMessage('bad_steps')
            self.blinkLEDs_error()
            return -1

        if((stepsWheelA > 0 and delayWheelA < self.minDelayMotors) or (stepsWheelB > 0 and delayWheelB < self.minDelayMotors)):
            messages.printMessage('bad_delay')
            self.blinkLEDs_error()
            return -1

        # If a stop command has been sent, the turtle will stop its movement
        if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

            if self.getStateTortoise() == enums.State.running:

                self.setStateTortoise(enums.State.paused)
                messages.printMessage('paused')

        else:

            if self.getStateTortoise() == enums.State.paused:
                    self.setStateTortoise(enums.State.running)
                    messages.printMessage('resumed')

            motorAprocess_backwards = Process(target=self.A.backwards, args=(delayWheelA / 1000.00, stepsWheelA))
            motorBprocess_backwards = Process(target=self.B.backwards, args=(delayWheelB / 1000.00, stepsWheelB))
            motorAprocess_forwards = Process(target=self.A.forwards, args=(delayWheelA / 1000.00, stepsWheelA))
            motorBprocess_forwards = Process(target=self.B.forwards, args=(delayWheelB / 1000.00, stepsWheelB))


            if direction == enums.Direction.backwards_left or direction == enums.Direction.backwards or direction == enums.Direction.backwards_right:

                if stepsWheelA > 0:
                    motorAprocess_backwards.start()

                if stepsWheelB > 0:
                    motorBprocess_backwards.start()

            elif direction == enums.Direction.forwards_right or direction == enums.Direction.forwards or direction == enums.Direction.forwards_left:

                if stepsWheelA > 0:
                    motorAprocess_forwards.start()

                if stepsWheelB > 0:
                    motorBprocess_forwards.start()

            elif direction == enums.Direction.clockwise:

                if stepsWheelA > 0:
                    motorAprocess_backwards.start()

                if stepsWheelB > 0:
                    motorBprocess_forwards.start()

            elif direction == enums.Direction.counterClockwise:

                if stepsWheelA > 0:
                    motorAprocess_forwards.start()

                if stepsWheelB > 0:
                    motorBprocess_backwards.start()




            # The main loop pools the emergencyStop
            while motorAprocess_backwards.is_alive() or motorBprocess_backwards.is_alive() or motorAprocess_forwards.is_alive() or motorBprocess_forwards.is_alive():

                # If a stop command has been sent, the turtle will stop its movement
                if self.getSensorData(enums.SensorType.emergencyStop, 1) == 0:

                    if self.getStateTortoise() == enums.State.running:

                        self.setStateTortoise(enums.State.paused)
                        messages.printMessage('paused')

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
                    messages.printMessage('resumed')


                time.sleep(0.5)


        self.A.stopMotors()
        self.B.stopMotors()

        return 0



    def moveForwards(self, steps):

        return self.moveMotors(steps, steps, self.minDelayMotors, self.minDelayMotors, enums.Direction.forwards)



    def moveBackwards(self, steps):

        return self.moveMotors(steps, steps, self.minDelayMotors, self.minDelayMotors, enums.Direction.backwards)



    def turnOnTheSpot(self, steps, direction):

        if(steps < 0):
            messages.printMessage('bad_steps')
            self.blinkLEDs_error()
            return -1

        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and
            direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left ) :
            messages.printMessage('bad_direction_turn')
            self.blinkLEDs_error()
            return -1



        if direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right:
            return self.moveMotors(steps, 0, self.minDelayMotors, 0, direction)

        elif direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left:
            return self.moveMotors(0, steps, 0, self.minDelayMotors, direction)



    def shuffleOnTheSpot(self, steps, direction):

        if(steps < 0):
            messages.printMessage('bad_steps')
            self.blinkLEDs_error()
            return -1

        if( direction != enums.Direction.clockwise and direction != enums.Direction.counterClockwise ) :
            messages.printMessage('bad_shuffle')
            self.blinkLEDs_error()
            return -1



        return self.moveMotors(steps, steps, self.minDelayMotors, self.minDelayMotors, direction)





    def turn(self, stepsWheelA, stepsWheelB, direction):

        if( direction != enums.Direction.backwards_right and direction != enums.Direction.backwards_left and
            direction != enums.Direction.forwards_right and direction != enums.Direction.forwards_left ) :
            messages.printMessage('bad_direction_turn')
            self.blinkLEDs_error()
            return -1

        if (direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right) and (stepsWheelB >= stepsWheelA):
            messages.printMessage('bad_turn')
            self.blinkLEDs_error()
            return -1

        if (direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left) and (stepsWheelA >= stepsWheelB):
            messages.printMessage('bad_turn')
            self.blinkLEDs_error()
            return -1

        if(stepsWheelA < 0 or stepsWheelB < 0):
            messages.printMessage('bad_steps')
            self.blinkLEDs_error()
            return -1



        if direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right:

            delay = (stepsWheelA * self.minDelayMotors) / stepsWheelB

            return self.moveMotors(stepsWheelA, stepsWheelB, self.minDelayMotors, delay, direction)

        elif direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left:

            delay = (stepsWheelB * self.minDelayMotors) / stepsWheelA

            return self.moveMotors(stepsWheelA, stepsWheelB, delay, self.minDelayMotors, direction)



    def doRandomMovement2():

        numberOfSteps = int()        




    def doRandomMovement(self):

        # Random number between 30 and (509/4 + 30)
        numberOfSteps = int(509/4*np.random.random_sample() + 30)

        # Random number between 0 and 1
        randomNumber = np.random.random_sample()

        if(randomNumber < 0.4):

            if(randomNumber < 0.2):

                self.moveForwards(numberOfSteps)

            else:

                self.moveBackwards(numberOfSteps)

        else:

            # Random enums.Direction: left of right
            if(np.random.random_sample() < 0.5):
                direction = enums.Direction.forwards_left
            else:
                direction = enums.Direction.forwards_right


            if(randomNumber < 0.7):
                self.turnOnTheSpot(numberOfSteps, direction)
            else:
                self.turnOnTheSpot(numberOfSteps, direction)


