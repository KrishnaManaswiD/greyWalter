# IMPORT MODULES FROM SUBFOLDERS #
#It's neccesary in order to import modules not in the same folder, but in a different one.
#This is the way to tell python the location on those subfolders:
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
import RPi.GPIO as GPIO
from multiprocessing import Process

# Numbering of the pins
GPIO.setmode(GPIO.BCM)



class Tortoise:

    def __init__(self):

        # Variables that control the calibration of the light sensors

        """ 
            The purpose was to avoid calibration everytime the tortoise object is created. 
            However, this hasn't been implemented yet. The idea could be to save the light 
            values in a file and read that file when creating the tortoise object. 
            Light conditions could have changed, so this should be done carefully. 

            At the moment, the tortoise object is created without calibration. If the users
            want to use the light sensors, they need will need to execute the calibrateLight
            function before using those sensors.
        """

        global isLightCalibrated
        global lowerBoundLight
        global upperBoundLight

        isLightCalibrated = False
        lowerBoundLight = 0
        upperBoundLight = 0
        # --- Variables that control the calibration of the light sensors ---


        # No warnings from the GPIO library
        GPIO.setwarnings(False)


        # Variables that control the random motion
        self.lastRandomCommand = None
        self.timesSameRandomCommandExecuted = 0
        self.numberRepeatsRandomCommand = -1
        self.lastRandomStepsWheelA = None
        self.lastRandomStepsWheelB = None
        self.lastRandomDirection = None
        # --- Variables that control the random motion ---



        


        # Setting the motors, sensors and actuators    

        # Pin numbers of the motors
        motorPins = [13, 6, 5, 7, 20, 10, 9, 11]
        self.A = Motor(motorPins[0], motorPins[1], motorPins[2], motorPins[3])
        self.B = Motor(motorPins[4], motorPins[5], motorPins[6], motorPins[7])

        self.sensors = Sensors()
        self.actuators = Actuators()

        # Position 1 of the light sensors area in the PCB assigned to pin 17
        self.sensors.setSensor(enums.SensorType.light, 1, 17) 

        # Position 2 of the light sensors area in the PCB assigned to pin 4
        self.sensors.setSensor(enums.SensorType.light, 2, 4)

        # Position 1 of the touch sensors area in the PCB assigned to pin 27
        self.sensors.setSensor(enums.SensorType.touch, 1, 27) 

        # Position 2 of the touch sensors area in the PCB assigned to pin 2
        self.sensors.setSensor(enums.SensorType.touch, 2, 2)

        # Position 3 of the touch sensors area in the PCB assigned to pin 18
        self.sensors.setSensor(enums.SensorType.touch, 3, 18)

        # Position 4 of the touch sensors area in the PCB assigned to pin 3
        self.sensors.setSensor(enums.SensorType.emergencyStop, 4, 3) 

        # Position 1 of the proximity sensors area in the PCB assigned to pin 19
        self.sensors.setSensor(enums.SensorType.proximity, 1, 19)

        # Position 2 of the proximity sensors area in the PCB assigned to pin 21
        self.sensors.setSensor(enums.SensorType.proximity, 2, 21) 

        # Position 3 of the proximity sensors area in the PCB assigned to pin 22
        self.sensors.setSensor(enums.SensorType.proximity, 3, 22) 

        # Position 4 of the proximity sensors area in the PCB assigned to pin 26
        self.sensors.setSensor(enums.SensorType.proximity, 4, 26) 

         # Positions of the LEDs area in the PCB assigned to pins 8, 16, 25, 12
        ledPins = [8, 16, 25, 12]
        self.actuators.initActuator(enums.ActuatorType.led, 1, ledPins[0]) 
        self.actuators.initActuator(enums.ActuatorType.led, 2, ledPins[1]) 
        self.actuators.initActuator(enums.ActuatorType.led, 3, ledPins[2]) 
        self.actuators.initActuator(enums.ActuatorType.led, 4, ledPins[3])
        # --- Setting the motors, sensors and actuators ---


        # Times pressed the touch sensor for the latching behavour
        self.lastTouch = [-1,-1,-1]

        # Minimum milliseconds to send to the motors as delay
        self.minDelayMotors = 2


        # Creation of a file with the PID of the process

        """
            The reasons of termination of a user process could be because of normal termination 
            or because of an error (exceptions, ctrl-c, ...). When an error happens, the motors
            and may be still on. In this case, the motors and LEDs should be turned off
            for the battery not to drain. 

            The solution implemented is to have a background process (a watchdog) running 
            continously. This process checks if the user process doesn't exist anymore (termination).
            If it doesn't, it stops the motors, switches off the LEDs and cleans up all the pins.
            In order to identy that the user script has finished, a file with the name [PID].pid is
            created in the folder ~/.tortoise_pids/, where [PID] is the PID of the user process.
        """

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
        # --- Creation of a file with the PID of the process ---



        # Waiting for the user to press the e-stop button
        self.state = enums.State.paused

        messages.printMessage('greetings')
        while self.getSensorData(enums.SensorType.emergencyStop, 4) == 0:
            time.sleep(0.1)

        messages.printMessage('running')

        self.state = enums.State.running
        # --- Waiting for the user to press the e-stop button ---



    def getStateTortoise(self):
        return self.state


    def setStateTortoise(self, toState):
        self.state = toState


    def calibrateLight(self):
        global lowerBoundLight, upperBoundLight, isLightCalibrated

        messages.printMessage('calibration_ambient')
        raw_input()
        lowerBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)

        messages.printMessage('calibration_light_source')
        raw_input()
        upperBoundLight = self.sensors.readSensor(enums.SensorType.light, 1)

        isLightCalibrated = True

        messages.printMessage('calibration_complete')



    def getSensorData(self, sensor_type, position):

        if (sensor_type == enums.SensorType.touch):

            if (position < 1 or position > 3):

                messages.printMessage('bad_touch_sensor')
                self.blinkLEDs_error()
                return -1

        elif (sensor_type == enums.SensorType.emergencyStop):

            if (position != 4):

                messages.printMessage('bad_emergency_sensor')
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

        else:
                messages.printMessage('bad_sensor')
                self.blinkLEDs_error()
                return -1


        # The value of the sensor is read at lowlevel
        value = self.sensors.readSensor(sensor_type, position)


        # For the light sensor, 'value' is the count of the light
        if sensor_type == enums.SensorType.light:
            return value
            if (upperBoundLight - lowerBoundLight) == 0:
                messages.printMessage('no_calibration')
                self.blinkLEDs_error()
                return -1

            # A scale to the range [0, 9] is done
            lightVal = int(9 - round(abs(value-upperBoundLight)/(abs(upperBoundLight - lowerBoundLight)/9)))

            if lightVal < 0:
                messages.printMessage('no_calibration')
                self.blinkLEDs_error()
                return -1

            return lightVal


        # For the touch sensor, 'value' is the number of times the sensor has been pressed
        elif sensor_type == enums.SensorType.touch:

            # Returns if the sensor has been pressed since the last time it was queried
            return self.getSwitchTriggered(position,value)

        # For the e-stop, 'value' is the number of times the sensor has been pressed
        elif sensor_type == enums.SensorType.emergencyStop:

            # Returns if it's either 1 (ON) or 0 (OFF)
            return value % 2

        # For the proximity sensor, 'value' is either 1 (ON) or 0 (OFF)
        elif sensor_type == enums.SensorType.proximity:

            # Returns 1 (ON) or 0 (OFF)
            return value



    def getSwitchTriggered(self, position, value):

        if self.lastTouch[position-1] < 0:

            self.lastTouch[position-1] = value
            return 0

        elif self.lastTouch[position-1] == value:

            return 0

        else:

            self.lastTouch[position-1] = value
            return 1


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


        # If no TypeError exception raised, 'positions' is an array
        try:

            # All positions are checked
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


        # The current state of the LEDs is saved to restore it later
        previousStateLEDs = [ self.getLEDValue(x) for x in range(1, 5) ]

        cont = True

        # If blocking == True, it's an infinite loop to "stop" the execution of the program and keep blinkind the LEDs
        while cont:

            for x in range(0, numberOfBlinks):

                # If no TypeError exception raised, 'positions' is an array
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


            # Depending on the parameter, it blocks or not
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
        if self.getSensorData(enums.SensorType.emergencyStop, 4) == 0:

            if self.getStateTortoise() == enums.State.running:

                self.setStateTortoise(enums.State.paused)
                messages.printMessage('paused')

        else:

            if self.getStateTortoise() == enums.State.paused:
                    self.setStateTortoise(enums.State.running)
                    messages.printMessage('resumed')


            # The threads are created. They aren't started yet though.
            motorAprocess_backwards = Process(target=self.A.backwards, args=(delayWheelA / 1000.00, stepsWheelA))
            motorBprocess_backwards = Process(target=self.B.backwards, args=(delayWheelB / 1000.00, stepsWheelB))
            motorAprocess_forwards = Process(target=self.A.forwards, args=(delayWheelA / 1000.00, stepsWheelA))
            motorBprocess_forwards = Process(target=self.B.forwards, args=(delayWheelB / 1000.00, stepsWheelB))


            # The specific wheels are started in order to accomplish the desired movement in the direction commanded

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




            # The main loop pools the emergencyStop while the motors are running
            while motorAprocess_backwards.is_alive() or motorBprocess_backwards.is_alive() or motorAprocess_forwards.is_alive() or motorBprocess_forwards.is_alive():

                # If a stop command has been sent, the turtle will stop its movement and exit this function
                if self.getSensorData(enums.SensorType.emergencyStop, 4) == 0:

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


        # When the movement finishes, the motors are turned off
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

    
        # Only wheel A moves
        if direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right:
            return self.moveMotors(steps, 0, self.minDelayMotors, 0, direction)

        # Only wheel B moves
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



    def shuffle45degrees(self, direction):

        return self.shuffleOnTheSpot(180, direction)


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

            # The delay of the wheel with less movements is worked out so that both wheels finish more or less at the same time
            delay = (stepsWheelA * self.minDelayMotors) / stepsWheelB

            return self.moveMotors(stepsWheelA, stepsWheelB, self.minDelayMotors, delay, direction)

        elif direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left:

            # The delay of the wheel with less movements is worked out so that both wheels finish more or less at the same time
            delay = (stepsWheelB * self.minDelayMotors) / stepsWheelA

            return self.moveMotors(stepsWheelA, stepsWheelB, delay, self.minDelayMotors, direction)




    def turn45degrees_sharp(self, direction):

        if direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right:

            return self.turn(400, 75, direction)

        elif direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left:

            return self.turn(75, 400, direction)



    def turn30degrees_wide(self, direction):

        if direction == enums.Direction.backwards_right or direction == enums.Direction.forwards_right:

            return self.turn(450, 250, direction)

        elif direction == enums.Direction.backwards_left or direction == enums.Direction.forwards_left:

            return self.turn(250, 450, direction)
        


    def doRandomMovement(self):

        # New random command
        if self.numberRepeatsRandomCommand == -1 or self.timesSameRandomCommandExecuted == self.numberRepeatsRandomCommand:

            # The number of times the command is repeated is chosen randomly with decreasing probabilities up to 3 times.
            self.numberRepeatsRandomCommand = np.random.choice([0, 1, 2, 3], 1, p = [0.6, 0.25, 0.1, 0.05])

            # As this is a new command, no repetitions done
            self.timesSameRandomCommandExecuted = 0

            # Random steps for wheel A
            self.lastRandomStepsWheelA = np.random.randint(30, 300)

            # Random number between 0 and 1 for decision on the random movement
            randomNumber = np.random.random_sample()

            # 40% probability of moving forwards/backwards
            if(randomNumber < 0.4):

                # 75% of probability of moving forwards
                if(randomNumber < 0.30):

                    self.moveForwards(self.lastRandomStepsWheelA)
                    self.lastRandomCommand = self.moveForwards

                # 25% probability of moving backwards
                else:

                    self.moveBackwards(self.lastRandomStepsWheelA)
                    self.lastRandomCommand = self.moveBackwards


            # 10% probability of shuffling
            elif (randomNumber < 0.5):

                # Equal probability of going clockwise or counter clockwise
                self.lastRandomDirection = np.random.choice([enums.Direction.clockwise, enums.Direction.counterClockwise], 1)

                self.shuffle45degrees(self.lastRandomDirection)

                self.lastRandomCommand = self.shuffle45degrees


            # 10% probability of turning 30 or 45 degrees
            elif (randomNumber < 0.6):

                # Equal probability of moving forwards/backwards lef/right
                self.lastRandomDirection = np.random.choice([enums.Direction.forwards_right, enums.Direction.forwards_left, enums.Direction.backwards_right, enums.Direction.backwards_left], 1)

                # Equal probability of turning 30 degrees wide or 45 degrees sharp
                if(randomNumber < 0.55):

                    self.turn45degrees_sharp(self.lastRandomDirection)
                    self.lastRandomCommand = self.turn45degrees_sharp

                else:

                    self.turn30degrees_wide(self.lastRandomDirection)
                    self.lastRandomCommand = self.turn30degrees_wide


            # 40% of turning randomly
            else:

                # Random steps for wheel B
                self.lastRandomStepsWheelB = np.random.randint(30, 300)

                # Equal probability of moving forwards/backwards lef/right
                self.lastRandomDirection = np.random.choice([enums.Direction.forwards_right, enums.Direction.forwards_left, enums.Direction.backwards_right, enums.Direction.backwards_left], 1)

                if(self.lastRandomDirection == enums.Direction.forwards_left or self.lastRandomDirection == enums.Direction.backwards_left):

                    if(self.lastRandomStepsWheelA >= self.lastRandomStepsWheelB):
                
                        aux = self.lastRandomStepsWheelA
                        self.lastRandomStepsWheelA = self.lastRandomStepsWheelB - 1 # To avoid the case of equals
                        self.lastRandomStepsWheelB = aux

                else:

                    if(self.lastRandomStepsWheelB >= self.lastRandomStepsWheelA):
                
                        aux = self.lastRandomStepsWheelA
                        self.lastRandomStepsWheelA = self.lastRandomStepsWheelB
                        self.lastRandomStepsWheelB = aux - 1 # To avoid the case of equals


                self.turn(self.lastRandomStepsWheelA, self.lastRandomStepsWheelB, self.lastRandomDirection)
    
                self.lastRandomCommand = self.turn



        # Repeat last command
        else:
    
            self.timesSameRandomCommandExecuted = self.timesSameRandomCommandExecuted + 1


            if self.lastRandomCommand == self.moveForwards:

                self.moveForwards(self.lastRandomStepsWheelA)

            elif self.lastRandomCommand == self.moveBackwards:

                self.moveBackwards(self.lastRandomStepsWheelA)

            elif self.lastRandomCommand == self.shuffle45degrees:

                self.shuffle45degrees(self.lastRandomDirection)

            elif self.lastRandomCommand == self.turn45degrees_sharp:

                self.turn45degrees_sharp(self.lastRandomDirection)

            elif self.lastRandomCommand == self.turn30degrees_wide:

                self.turn30degrees_wide(self.lastRandomDirection)

            elif self.lastRandomCommand == self.turn:

                self.turn(self.lastRandomStepsWheelA, self.lastRandomStepsWheelB, self.lastRandomDirection)  



