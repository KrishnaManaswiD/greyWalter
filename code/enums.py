from enum import Enum

class State(Enum):
	paused = 0
	running = 1

class SensorType(Enum):
    touch = 0
    light = 1
    proximity = 2
    emergencyStop = 3

class ActuatorType(Enum):
    led = 0

class Direction(Enum):
    counterClockwise = -4
    backwards_right = -3
    backwards_left = -2
    backwards = -1
    forwards = 1
    forwards_left = 2
    forwards_right = 3
    clockwise = 4


