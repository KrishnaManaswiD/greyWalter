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

t = Tortoise()

while(True):

    t.turn45degrees_sharp(enums.Direction.forwards_left)
    t.turn45degrees_sharp(enums.Direction.forwards_left)
    time.sleep(1)

    t.turn45degrees_sharp(enums.Direction.backwards_left)
    t.turn45degrees_sharp(enums.Direction.backwards_left)
    time.sleep(1)

    t.turn45degrees_sharp(enums.Direction.forwards_right)
    t.turn45degrees_sharp(enums.Direction.forwards_right)
    time.sleep(1)

    t.turn45degrees_sharp(enums.Direction.backwards_right)
    t.turn45degrees_sharp(enums.Direction.backwards_right)
    time.sleep(1)
