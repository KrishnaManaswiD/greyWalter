from enum import Enum

class State(Enum):
	paused = 0
	running = 1

class SensorType(Enum):
    touch = 0
    light = 1
    proximity = 2
    emergencySwitch = 3

class ActuatorType(Enum):
   led = 0

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


