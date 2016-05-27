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

    wanderer.setLEDValue(1, 1)
    wanderer.setLEDValue(2, 1)
    wanderer.setLEDValue(3, 1)
    wanderer.setLEDValue(4, 1)

    while True:

        wanderer.moveForwards(2000)
        

if __name__ == "__main__":
	main()
