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

class Tortoise:

	def __init__(self):
		self.A = Motor(4, 17, 23, 24)
		self.B = Motor(14, 15, 18, 27)


	def main(self):
		while True:
			delay = raw_input("Delay between steps (milliseconds)?")	
			steps = raw_input("How many steps forward? ")
			self.A.forward(int(delay) / 1000.00, int(steps))
			steps = raw_input("How many steps backwards? ")
			self.A.backwards(int(delay) / 1000.00, int(steps))

