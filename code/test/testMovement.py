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

        print "Moving forwards"
        wanderer.moveForwards(500)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()


        print "Moving backwards"
        wanderer.moveBackwards(500)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()


        print "Turning on the spot forwards_left"
        wanderer.turnOnTheSpot(500, enums.Direction.forwards_left)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning on the spot forwards_right"
        wanderer.turnOnTheSpot(500, enums.Direction.forwards_right)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning on the spot backwards_left"
        wanderer.turnOnTheSpot(500, enums.Direction.backwards_left)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning on the spot bakwards_right"
        wanderer.turnOnTheSpot(500, enums.Direction.backwards_right)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning naturally forwards_left"
        wanderer.turnNaturally(200, 500, enums.Direction.forwards_left)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning naturally backwards_left"
        wanderer.turnNaturally(200, 500, enums.Direction.backwards_left)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning naturally forwards_right"
        wanderer.turnNaturally(500, 200, enums.Direction.forwards_right)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Turning naturally backwards_right"
        wanderer.turnNaturally(500, 200, enums.Direction.backwards_right)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Gyrating clockwise"
        wanderer.gyrateOnTheSpot(500, enums.Direction.clockwise)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        print "Gyrating counter clockwise"
        wanderer.gyrateOnTheSpot(500, enums.Direction.counterClockwise)
        time.sleep(0.5)

        print
        print "\tPress enter to continue"
        print
        raw_input()

        

if __name__ == "__main__":
	main()
