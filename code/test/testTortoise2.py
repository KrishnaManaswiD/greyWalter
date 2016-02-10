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
		#pass
		wanderer.moveMotors(100, enums.Direction.forward)
		#print wanderer.getSensorData(enums.SensorType.light, 1)
		if wanderer.getSensorData(enums.SensorType.proximity, 1) == 1:
                        print "1"
			wanderer.setActuatorValue(enums.ActuatorType.led, 1,1)
		else:
                        print "0"
			wanderer.setActuatorValue(enums.ActuatorType.led, 1,0)
		#time.sleep(0.1)

if __name__ == "__main__":
	main()
