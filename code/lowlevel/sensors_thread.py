import thread
import RPi.GPIO as GPIO
import time

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

        try:
            thread.start_new_thread(self.poll_sensors, (500,))
        except:
            print "Error: unable to start thread"

    def readSensor(self,sensor_type,pos):
		while self.busy == True:
			pass
		    if sensor_type == self.touch:
		        if pos == 1:
					print self.touch1_value
		            return self.touch1_value
		        elif pos == 2:
					print self.touch2_value
		            return self.touch2_value
		        elif pos == 3:
		            return self.touch3_value
		        elif pos == 4:
		            return self.touch4_value
		        elif pos == 5:
		            return self.touch5_value
		        elif pos == 6:
		            return self.touch6_value
		    elif sensor_type == self.light:
		        if pos == 1:
		            return self.light1_value
		        elif pos == 2:
		            return self.light2_value
		    else:
		        if pos == 1:
		            return self.prox1_value
		        elif pos == 2:
		            return self.prox2_value

    def poll_sensors(self,delay):
        while True:
            self.busy = True
            #self.light1_value = self.read_light(self.lightSensor_pin1)
            #print self.light1_value
            #self.light2_value = self.read_light(self.lightSensor_pin2)
            #print self.light2_value
            self.touch1_value = GPIO.input(self.touchSensor_pin1)
	    #print self.touch1_value
            self.touch2_value = GPIO.input(self.touchSensor_pin2)
            #print self.touch2_value
	    	self.touch3_value = GPIO.input(self.touchSensor_pin3)
            #print self.touch3_value
	   		self.touch4_value = GPIO.input(self.touchSensor_pin4)
            #print self.touch4_value
            self.touch5_value = GPIO.input(self.touchSensor_pin5)
            #print self.touch5_value
            self.touch6_value = GPIO.input(self.touchSensor_pin6)
            #print self.touch6_value
            self.prox1_value = GPIO.input(self.proximitySensor_pin1)
            #print self.prox1_value
            self.prox2_value = GPIO.input(self.proximitySensor_pin2)
            #print self.prox2_value
            self.busy = False
            time.sleep(delay/1000.0)

    def read_light(self,lspin):
        reading = 0
        GPIO.setup(lspin, GPIO.OUT)
        GPIO.output(lspin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(lspin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(lspin) == GPIO.LOW):
            reading += 1
        return reading

