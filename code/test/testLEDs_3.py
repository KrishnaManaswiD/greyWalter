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

        wanderer.setActuatorValue(enums.ActuatorType.led, 1, 1)
        wanderer.setActuatorValue(enums.ActuatorType.led, 2, 0)
        wanderer.setActuatorValue(enums.ActuatorType.led, 3, 1)
        wanderer.setActuatorValue(enums.ActuatorType.led, 4, 0)

        print "LEDs 1 and 3 set"
        print
        print "\tPress enter to continue"
        raw_input()

        print "Blinking LED 1, 2, 3 and 4"
        wanderer.blinkLED([3, 4, 1, 2], 3, 0.3)

        print "Check status of LEDs after blinking"
        print
        print "\tPress enter to continue"
        raw_input()



        wanderer.setActuatorValue(enums.ActuatorType.led, 1, 1)
        wanderer.setActuatorValue(enums.ActuatorType.led, 2, 1)
        wanderer.setActuatorValue(enums.ActuatorType.led, 3, 1)
        wanderer.setActuatorValue(enums.ActuatorType.led, 4, 1)

        print "LEDs 1, 2, 3 and 4 set"
        print
        print "\tPress enter to continue"
        raw_input()

        print "Blinking LED 1, 2, 3 and 4"
        wanderer.blinkLED([3, 4, 1, 2], 3, 0.3)

        print "Check status of LEDs after blinking"
        print
        print "\tPress enter to continue"
        raw_input()


if __name__ == "__main__":
	main()
