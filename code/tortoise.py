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
from sensors import Sensor
from enum import Enum

class SensorType(Enum):
    touch = 0
    light = 1
    proximity = 2

class Direction(Enum):
    counterClockwise = -4
    backward_right = -3
    backward_left = -2
    backward = -1
    static = 0
    forward = 1
    forward_left = 2
    forward_right = 3
    clockwise = 4

class Tortoise:

    def __init__(self):
        self.A = Motor(4, 17, 23, 24)
        self.B = Motor(14, 15, 18, 27)
        self.sensor = Sensor(1,2,3,5,6,7,8,9,10,11)

    def readSensor(self,sensor_type,pos):
        self.sensor.readSensor(sensor_type,pos)

    def moveSomewhere(self, steps, delay, direction):

        if direction == Direction.static:
            print "Are you kiddin' me??"
            return

        for x in range(0,steps):
            if direction == Direction.backward_left or direction == Direction.backward or direction == Direction.counterClockwise:
                self.A.backwards(int(delay) / 1000.00, int(1))
            if direction == Direction.backward_right or direction == Direction.backward or direction == Direction.clockwise:
                self.B.backwards(int(delay) / 1000.00, int(1))
            if direction == Direction.forward_right or direction == Direction.forward or direction == Direction.clockwise:
                self.A.forward(int(delay) / 1000.00, int(1))
            if direction == Direction.forward_left or direction == Direction.forward or direction == Direct.counterClockwise:
                self.B.forward(int(delay) / 1000.00, int(1))


    def naturalTurn(self, totalSteps, straightStep, sideStep, delay, direction):

        if forwardStep < 0 or sideStep < 0: return
        if not direction == Direction.forward_left or not direction == Direction.forward_right or not direction == Direction.backward_left or not direction == Direction.backward_right:
            print "Don't mess around."
            return

        for x in range(0, totalSteps):
            if direction == Direction.forward_left:
                self.moveSomewhere(staightStep, delay, Direction.forward)
                self.moveSomewhere(sideStep, delay, Direction.left)
            if direction == Direction.forward_right:
                self.moveSomewhere(straightStep, delay, Direction.forward)
                self.moveSomewhere(sideStep, delay, Direction.right)
            if direction == Direction.backward_left:
                self.moveSomewhere(straightStep, delay, Direction.backward)
                self.moveSomewhere(sideStep, delay, Direction.left)
            if direction == Direction.backward_right:
                self.moveSomewhere(straightStep, delay, Direction.backward)
                self.moveSomewhere(sideStep, delay, Direction.right)

    def gentleTurn(self, steps, direction):
        self.naturalTurn(steps, 3, 1, direction)

    def sharpTurn(self, steps, direction):
        self.naturalTurn(steps, 1, 3, direction)

    def tryCircle(self, direction):
        self.gentleTurn(2000, direction)

    def defaultCircle(self):
        self.tryCircle(Direction.forward_right)