# IMPORT MODULES FROM SUBFOLDERS #
""" It's neccesary in order to import modules not in the same folder, but in a different one.
This is the way to tell python the location on those subfolders: """
import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

sys.path.append('../')
# ------------------------------ #

from tortoise import Tortoise
import enums
import time

def main():
        wanderer = Tortoise()

	while True:

                emergencySwitch = wanderer.getSensorData(enums.SensorType.emergencySwitch, 1)
                touchSensor_1 = wanderer.getSensorData(enums.SensorType.touch, 1)
                touchSensor_2 = wanderer.getSensorData(enums.SensorType.touch, 2)
                touchSensor_3 = wanderer.getSensorData(enums.SensorType.touch, 3)

                if touchSensor_1 == 1:
                        print "Switch 1 is on"
                else:
                        print "Switch 1 is off"

                if touchSensor_2 == 1:
                        print "Switch 2 is on"
                else:
                        print "Switch 2 is off"

                if touchSensor_3 == 1:
                        print "Switch 3 is on"
                else:
                        print "Switch 3 is off"

                if emergencySwitch == 1:
                        print "Emergency switch is on"
                else:
                        print "Emergency switch is off"

                print

                time.sleep(1)

if __name__ == "__main__":
	main()
