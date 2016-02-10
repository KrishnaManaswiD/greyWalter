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
from enum import Enum

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


	def main(self):
		while True:
            delay = raw_input("Delay between steps (milliseconds)?")
            steps = raw_input("How many steps forward? ")
            moveSomewhere(self, steps, delay/2, Direction.forward)
            steps = raw_input("How many steps backwards? ")
            moveSomewhere(self, steps, delay/2, Direction.backward)
                

    def moveSomewhere(self, steps, delay, direction):
        if direction == Direction.static return
        for x in range(0,steps):
            if direction == Direction.backward_left || direction == Direction.backward || direction == Direction.counterClockwise:
                self.A.backwards(int(delay) / 1000.00, int(1))
            if direction == Direction.backward_right || direction == Direction.backward || direction == Direction.clockwise:
                self.B.backwards(int(delay) / 1000.00, int(1))
            if direction == Direction.forward_right || direction == Direction.forward || direction == Direction.clockwise:
                self.A.forward(int(delay) / 1000.00, int(1))
            if direction == Direction.forward_left || direction == Direction.forward || direction == Direct.counterClockwise:
                self.B.forward(int(delay) / 1000.00, int(1))
