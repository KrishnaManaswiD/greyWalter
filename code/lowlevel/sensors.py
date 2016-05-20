import RPi.GPIO as GPIO
import time
import enums

GPIO.setmode(GPIO.BCM)

class Sensor:

    def __init__(self):

        self.busy = False
        self.touch = 0
        self.light = 1
        self.proximity = 2
        self.emergencySwitch = 3

        self.lightSensor_pin1 = -1
        self.lightSensor_pin2 = -1
        self.touchSensor_pin1 = -1
        self.touchSensor_pin2 = -1
        self.touchSensor_pin3 = -1
        self.touchSensor_pin4 = -1
        self.touchSensor_pin5 = -1
        self.touchSensor_pin6 = -1
        self.proximitySensor_pin1 = -1
        self.proximitySensor_pin2 = -1
        self.emergencySwitch_pin1 = -1


        self.light1_value = -1 #self.read_light(self.lightSensor_pin1)
        self.light2_value = -1 #self.read_light(self.lightSensor_pin2)
        self.touch1_value = -1
        self.touch2_value = -1
        self.touch3_value = -1
        self.touch4_value = -1
        self.touch5_value = -1
        self.touch6_value = -1
        self.prox1_value = -1
        self.prox2_value = -1
        self.emergency1_value = -1

#        try:
#            thread.start_new_thread(self.poll_sensors, (500,))
#        except:
#            print "Error: unable to start thread"



    def setSensor(self, sensor_type, pos, pin):

        if sensor_type == enums.SensorType.touch:

            if pos == 1:
                self.touchSensor_pin1 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 2:
                self.touchSensor_pin2 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 3:
                self.touchSensor_pin3 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 4:
                self.touchSensor_pin4 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 5:
                self.touchSensor_pin5 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 6:
                self.touchSensor_pin6 = pin
                GPIO.setup(pin, GPIO.IN)

        elif sensor_type == enums.SensorType.light:

            if pos == 1:
                self.lightSensor_pin1 = pin
                GPIO.setup(pin, GPIO.OUT)
            elif pos == 2:
                self.lightSensor_pin2 = pin
                GPIO.setup(pin, GPIO.OUT)

        elif sensor_type == enums.SensorType.proximity:

            if pos == 1:
                self.proximitySensor_pin1 = pin
                GPIO.setup(pin, GPIO.IN)
            elif pos == 2:
                self.proximitySensor_pin2 = pin
                GPIO.setup(pin, GPIO.IN)

        elif sensor_type == enums.SensorType.emergencySwitch:
        
            if pos == 1:
            
                self.emergencySwitch_pin1 = pin
                GPIO.setup(pin, GPIO.IN)
    


    def readSensor(self,sensor_type,pos):

        if sensor_type == enums.SensorType.touch:
            if pos == 1:

                if(self.touchSensor_pin1 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 1 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin1)
                    return GPIO.input(self.touchSensor_pin1) == GPIO.HIGH

            elif pos == 2:

                if(self.touchSensor_pin2 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 2 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin2)
                    return GPIO.input(self.touchSensor_pin2) == GPIO.HIGH


            elif pos == 3:

                if(self.touchSensor_pin3 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 3 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin3)
                    return GPIO.input(self.touchSensor_pin3) == GPIO.HIGH

            elif pos == 4:

                if(self.touchSensor_pin4 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 4 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin4)
                    return GPIO.input(self.touchSensor_pin4) == GPIO.HIGH

            elif pos == 5:

                if(self.touchSensor_pin5 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 5 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin5)
                    return GPIO.input(self.touchSensor_pin5) == GPIO.HIGH

            elif pos == 6:

                if(self.touchSensor_pin6 == -1)            
                    raise RuntimeError('Pin for touch sensor in position 6 not assigned')
                else
                    print GPIO.input(self.touchSensor_pin6)
                    return GPIO.input(self.touchSensor_pin6) == GPIO.HIGH


        elif sensor_type == enums.SensorType.light:

            if pos == 1:

                if(self.lightSensor_pin1 == -1)            
                    raise RuntimeError('Pin for light sensor in position 1 not assigned')
                else
                    print GPIO.input(self.lightSensor_pin1)
                    return GPIO.input(self.lightSensor_pin1)

            elif pos == 2:

                if(self.lightSensor_pin2 == -1)            
                    raise RuntimeError('Pin for light sensor in position 2 not assigned')
                else
                    print GPIO.input(self.lightSensor_pin2)
                    return GPIO.input(self.lightSensor_pin2)

        elif sensor_type == enums. SensorType.proximity:

            if pos == 1:

                if(self.proximitySensor_pin1 == -1)            
                    raise RuntimeError('Pin for proximity sensor in position 1 not assigned')
                else
                    print GPIO.input(self.proximitySensor_pin1)
                    return GPIO.input(self.proximitySensor_pin1)

            elif pos == 2:

                if(self.proximitySensor_pin2 == -1)            
                    raise RuntimeError('Pin for proximity sensor in position 2 not assigned')
                else
                    print GPIO.input(self.proximitySensor_pin2)
                    return GPIO.input(self.proximitySensor_pin2)

        elif sensor_type == enums.SensorType.emergencySwitch:
        
            if pos == 1:
            
                if(self.emergencySwitch_pin1 == -1)            
                    raise RuntimeError('Pin for emergency switch in position 1 not assigned')
                else
                    print GPIO.input(self.emergencySwitch_pin1)
                    return GPIO.input(self.emergencySwitch_pin1) == GPIO.HIGH



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

