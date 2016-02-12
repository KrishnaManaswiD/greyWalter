# IMPORT MODULES FROM SUBFOLDERS #
""" It's neccesary in order to import modules not in the same folder, but in a different one.
This is the way to tell python the location on those subfolders: """
import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

sys.path.append('../')
# ------------------------------ #

from tortoise import Tortoise,Direction,SensorType

def main():
    wanderer = Tortoise()
	while True:
        delay = raw_input("Delay between steps (milliseconds)?")
        steps = raw_input("How many steps forward? ")
        wanderer.moveSomewhere(steps, delay/2, Direction.forward)
        steps = raw_input("How many steps backwards? ")
        wanderer.moveSomewhere(steps, delay/2, Direction.backward)
        touch1 = wanderer.readSensor(SensorType.touch,1)
        print "Touch Sensor 1 is %s" % touch1
        touch2 = wanderer.readSensor(SensorType.touch,2)
        print "Touch Sensor 2 is %s" % touch2
        touch3 = wanderer.readSensor(SensorType.touch,3)
        print "Touch Sensor 3 is %s" % touch3
        touch4 = wanderer.readSensor(SensorType.touch,4)
        print "Touch Sensor 4 is %s" % touch4
        touch5 = wanderer.readSensor(SensorType.touch,5)
        print "Touch Sensor 5 is %s" % touch5
        touch6 = wanderer.readSensor(SensorType.touch,6)
        print "Touch Sensor 6 is %s" % touch6
        proximity1 = wanderer.readSensor(SensorType.proximity,1)
        print "Proximity Sensor 1 is %s" % proximity1
        proximity2 = wanderer.readSensor(SensorType.proximity,2)
        print "Proximity Sensor 2 is %s" % proximity2
        light1 = wanderer.readSensor(SensorType.light,1)
        print "Light Sensor 1 value is %s" % light1
        light2 = wanderer.readSensor(SensorType.light,2)
        print "Light Sensor 2 value is %s" % light2

if __name__=="__main__":
	main()