from tortoise import Tortoise
from enums import Direction, SensorType
import time

def main():
	Bob=Tortoise()

	count = 0
	pressTime = time.time()
	lastPress = Bob.getSensorData(SensorType.touch, 6)
	print"testing push button"
	while True:
 		press = Bob.getSensorData(SensorType.touch, 6)
  		if press == 0 and lastPress != press:
    			count += 1
    			pressTime = time.time()
    			if count >= 5:
      				print"five presses"
      				count = 0
  		lastPress = press

if __name__ =="__main__":
	main()
