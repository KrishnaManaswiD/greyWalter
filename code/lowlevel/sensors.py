import RPi.GPIO as GPIO
import time
import enums

GPIO.setmode(GPIO.BCM)

class Sensor:

    def __init__(self,lightSensor_pin1,lightSensor_pin2,touchSensor_pin1,touchSensor_pin2,touchSensor_pin3,touchSensor_pin4,touchSensor_pin5,touchSensor_pin6,proximitySensor_pin1,proximitySensor_pin2):

        self.busy = False
        self.touch = 0
        self.light = 1
        self.proximity = 2

        self.lightSensor_pin1 = lightSensor_pin1
        self.lightSensor_pin2 = lightSensor_pin2
        self.touchSensor_pin1 = touchSensor_pin1
        self.touchSensor_pin2 = touchSensor_pin2
        self.touchSensor_pin3 = touchSensor_pin3
        self.touchSensor_pin4 = touchSensor_pin4
        self.touchSensor_pin5 = touchSensor_pin5
        self.touchSensor_pin6 = touchSensor_pin6
        self.proximitySensor_pin1 = proximitySensor_pin1
        self.proximitySensor_pin2 = proximitySensor_pin2

        GPIO.setup(self.lightSensor_pin1, GPIO.OUT)
        GPIO.setup(self.lightSensor_pin2, GPIO.OUT)
        GPIO.setup(self.touchSensor_pin1, GPIO.IN)
        GPIO.setup(self.touchSensor_pin2, GPIO.IN)
        GPIO.setup(self.touchSensor_pin3, GPIO.IN)
        GPIO.setup(self.touchSensor_pin4, GPIO.IN)
        GPIO.setup(self.touchSensor_pin5, GPIO.IN)
        GPIO.setup(self.touchSensor_pin6, GPIO.IN)
        GPIO.setup(self.proximitySensor_pin1, GPIO.IN)
        GPIO.setup(self.proximitySensor_pin2, GPIO.IN)

	self.light1_value = 1 #self.read_light(self.lightSensor_pin1)
        self.light2_value = 1 #self.read_light(self.lightSensor_pin2)
        self.touch1_value = GPIO.input(self.touchSensor_pin1)
        self.touch2_value = GPIO.input(self.touchSensor_pin2)
        self.touch3_value = GPIO.input(self.touchSensor_pin3)
        self.touch4_value = GPIO.input(self.touchSensor_pin4)
        self.touch5_value = GPIO.input(self.touchSensor_pin5)
        self.touch6_value = GPIO.input(self.touchSensor_pin6)
        self.prox1_value = GPIO.input(self.proximitySensor_pin1)
        self.prox2_value = GPIO.input(self.proximitySensor_pin2)

#        try:
#            thread.start_new_thread(self.poll_sensors, (500,))
#        except:
#            print "Error: unable to start thread"

    def readSensor(self,sensor_type,pos):
		#print "Sensor Type enumVal"
		#print sensor_type
    		if sensor_type == enums.SensorType.touch:
			#print "We are activating a touch sensor"
		        if pos == 1:
				print GPIO.input(self.touchSensor_pin1)
				return GPIO.input(self.touchSensor_pin1)
		        elif pos == 2:
				print GPIO.input(self.touchSensor_pin2)
				return GPIO.input(self.touchSensor_pin2)
		        elif pos == 3:
				return GPIO.input(self.touchSensor_pin3)
		        elif pos == 4:
				return GPIO.input(self.touchSensor_pin4)
		        elif pos == 5:
				return GPIO.input(self.touchSensor_pin5)
		        elif pos == 6:
				return GPIO.input(self.touchSensor_pin6)
		if sensor_type == enums.SensorType.light:
			#print "We are activating a light sensor"
		        if pos == 1:
			    #print "Pos1"
		            return self.read_light(self.lightSensor_pin1)
		        elif pos == 2:
			    #print "Pos2"
		            return self.read_light(self.lightSensor_pin2)
		if sensor_type == enums. SensorType.proximity:
			#print "We are activating a proximity sensor"
		        if pos == 1:
		            return GPIO.input(self.proximitySensor_pin1)
		        elif pos == 2:
		            return GPIO.input(self.proximitySensor_pin2)

#    def poll_sensors(self,delay):
#        while True:
#            self.busy = True
#            #self.light1_value = self.read_light(self.lightSensor_pin1)
#            #print self.light1_value
#            #self.light2_value = self.read_light(self.lightSensor_pin2)
#            #print self.light2_value
#            self.touch1_value = GPIO.input(self.touchSensor_pin1)
#	    #print self.touch1_value
#            self.touch2_value = GPIO.input(self.touchSensor_pin2)
#            #print self.touch2_value
#	    	self.touch3_value = GPIO.input(self.touchSensor_pin3)
#            #print self.touch3_value
#	   	self.touch4_value = GPIO.input(self.touchSensor_pin4)
#            #print self.touch4_value
#            self.touch5_value = GPIO.input(self.touchSensor_pin5)
#            #print self.touch5_value
#            self.touch6_value = GPIO.input(self.touchSensor_pin6)
#            #print self.touch6_value
#            self.prox1_value = GPIO.input(self.proximitySensor_pin1)
#            #print self.prox1_value
#            self.prox2_value = GPIO.input(self.proximitySensor_pin2)
#            #print self.prox2_value
#            self.busy = False
#            time.sleep(delay/1000.0)

    def read_light(self,lspin):
        reading = 0
        GPIO.setup(lspin, GPIO.OUT)
        GPIO.output(lspin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(lspin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
	#print "Entering loop"
        while (GPIO.input(lspin) == GPIO.LOW):
            reading += 1
	#print "Leaving loop"	
	#print "read light"
        return reading

