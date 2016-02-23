from tortoise import Tortoise,Direction,SensorType


def readFrontLightSensor(self):
	return self.getSensorData(SensorType.light, 1) 

def main():
	myTortoise = Tortoise()

	frontLightSensor = myTortoise.readFrontLightSensor
	print "Front Light Sensor is %s" % frontLightSensor
	

if __name__=="__main__":
	main()
