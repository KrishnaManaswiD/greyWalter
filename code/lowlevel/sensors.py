import RPi.GPIO as GPIO
import time
import enums

GPIO.setmode(GPIO.BCM)

class Sensors:

    def __init__(self):

        self.busy = False
        self.touch = 0
        self.light = 1
        self.proximity = 2
        self.emergencySwitch = 3

        self.touchPressed = 0

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
        self.proximitySensor_pin3 = -1
        self.proximitySensor_pin4 = -1
        self.emergencySwitch_pin1 = -1

        self.light1_value = -1 #self.read_light(self.lightSensor_pin1)
        self.light2_value = -1 #self.read_light(self.lightSensor_pin2)
        self.touch1_timesPressed = 0
        self.touch2_timesPressed = 0
        self.touch3_timesPressed = 0
        self.touch4_timesPressed = 0
        self.touch5_timesPressed = 0
        self.touch6_timesPressed = 0
        self.proximity1_state = -1 
        self.proximity2_state = -1
        self.proximity3_state = -1
        self.proximity4_state = -1
        self.emergency1_timesPressed = 0

#        try:
#            thread.start_new_thread(self.poll_sensors, (500,))
#        except:
#            print "Error: unable to start thread"

    #if everything OK, return 0. If sensor type unknown or position > limit, return -1
    def setSensor(self, sensor_type, pos, pin):
        if sensor_type == enums.SensorType.touch:
            if pos == 1:
                self.touchSensor_pin1 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            elif pos == 2:
                self.touchSensor_pin2 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            elif pos == 3:
                self.touchSensor_pin3 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            elif pos == 4:
                self.touchSensor_pin4 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            elif pos == 5:
                self.touchSensor_pin5 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            elif pos == 6:
                self.touchSensor_pin6 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-6')
                return -1

        elif sensor_type == enums.SensorType.light:
            if pos == 1:
                self.lightSensor_pin1 = pin
                GPIO.setup(pin, GPIO.OUT)
                return 0
            elif pos == 2:
                self.lightSensor_pin2 = pin
                GPIO.setup(pin, GPIO.OUT)
                return 0
            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-2')
                return -1

        elif sensor_type == enums.SensorType.proximity:
            if pos == 1:
                self.proximitySensor_pin1 = pin
                
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                self.proximity1_state = GPIO.input(pin)
                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 300)
                return 0
            elif pos == 2:
                self.proximitySensor_pin2 = pin
                
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                self.proximity2_state = GPIO.input(pin)
                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 300)
                return 0
            elif pos == 3:
                self.proximitySensor_pin3 = pin
                
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                self.proximity3_state = GPIO.input(pin)
                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 300)
                return 0
            elif pos == 4:
                self.proximitySensor_pin4 = pin
                
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                self.proximity4_state = GPIO.input(pin)
                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 300)
                return 0
            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-4')
                return -1

        elif sensor_type == enums.SensorType.emergencySwitch:
            if pos == 1:
                self.emergencySwitch_pin1 = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            else:
                raise RuntimeError('Emergency switch can only be assigned to position 1')
                return -1

        else:
            raise RuntimeError('Unknown sensor type!')
            return -1


    def callback_touch(self, channel):
        if channel == self.touchSensor_pin1:
            self.touch1_timesPressed = self.touch1_timesPressed + 1
        elif channel == self.touchSensor_pin2:
            self.touch2_timesPressed = self.touch2_timesPressed + 1
        elif channel == self.touchSensor_pin3:
            self.touch3_timesPressed = self.touch3_timesPressed + 1
        elif channel == self.touchSensor_pin4:
            self.touch4_timesPressed = self.touch4_timesPressed + 1
        elif channel == self.touchSensor_pin5:
            self.touch5_timesPressed = self.touch5_timesPressed + 1
        elif channel == self.touchSensor_pin6:
            self.touch6_timesPressed = self.touch6_timesPressed + 1
        elif channel == self.emergencySwitch_pin1:
            self.emergency1_timesPressed = self.emergency1_timesPressed + 1

    def callback_proximity(self,channel):
        time.sleep(0.01)
        if channel == self.proximitySensor_pin1:
            self.proximity1_state =  GPIO.input(channel)
        elif channel == self.proximitySensor_pin2:
            self.proximity2_state =  GPIO.input(channel)
        elif channel == self.proximitySensor_pin3:
            self.proximity3_state =  GPIO.input(channel)
        elif channel == self.proximitySensor_pin4:
            self.proximity4_state =  GPIO.input(channel)

    #if everything OK, return sensor value. If sensor type unknown or position > limit, return -1
    def readSensor(self,sensor_type,pos):

        if sensor_type == enums.SensorType.touch:
            if pos == 1:
                if(self.touchSensor_pin1 == -1) :
                    raise RuntimeError('Pin for touch sensor in position 1 is not assigned')
                    return -1
                else:
                    return self.touch1_timesPressed

            elif pos == 2:
                if(self.touchSensor_pin2 == -1) :
                    raise RuntimeError('Pin for touch sensor in position 2 is not assigned')
                    return -1
                else:
                    return self.touch2_timesPressed

            elif pos == 3:
                if(self.touchSensor_pin3 == -1):
                    raise RuntimeError('Pin for touch sensor in position 3 is not assigned')
                    return -1
                else:
                    return self.touch3_timesPressed

            elif pos == 4:
                if(self.touchSensor_pin4 == -1):
                    raise RuntimeError('Pin for touch sensor in position 4 is not assigned')
                    return -1
                else:
                    return self.touch4_timesPressed

            elif pos == 5:
                if(self.touchSensor_pin5 == -1):
                    raise RuntimeError('Pin for touch sensor in position 5 is not assigned')
                    return -1
                else:
                    return self.touch5_timesPressed

            elif pos == 6:
                if(self.touchSensor_pin6 == -1):
                    raise RuntimeError('Pin for touch sensor in position 6 is not assigned')
                    return -1
                else:
                    return self.touch6_timesPressed
            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-6')
                return -1

        elif sensor_type == enums.SensorType.light:

            if pos == 1:
                if(self.lightSensor_pin1 == -1):
                    raise RuntimeError('Pin for light sensor in position 1 is not assigned')
                    return -1
                else:
                    return self.read_light(self.lightSensor_pin1)

            elif pos == 2:
                if(self.lightSensor_pin2 == -1):
                    raise RuntimeError('Pin for light sensor in position 2 is not assigned')
                    return -1
                else:
                    return self.read_light(self.lightSensor_pin2)
            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-2')
                return -1

        elif sensor_type == enums.SensorType.proximity:

            if pos == 1:
                if(self.proximitySensor_pin1 == -1):
                    raise RuntimeError('Pin for proximity sensor in position 1 is not assigned')
                    return -1
                else:
                    return self.proximity1_state
            elif pos == 2:
                if(self.proximitySensor_pin2 == -1):
                    raise RuntimeError('Pin for proximity sensor in position 2 is not assigned')
                    return -1
                else:
                    return self.proximity2_state
            elif pos == 3:
                if(self.proximitySensor_pin3 == -1):
                    raise RuntimeError('Pin for proximity sensor in position 3 is not assigned')
                    return -1
                else:
                    return self.proximity3_state
            elif pos == 4:
                if(self.proximitySensor_pin4 == -1):
                    raise RuntimeError('Pin for proximity sensor in position 4 is not assigned')
                    return -1
                else:
                    return self.proximity4_state
            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-4')
                return -1

        elif sensor_type == enums.SensorType.emergencySwitch:

            if pos == 1:
                if(self.emergencySwitch_pin1 == -1):
                    raise RuntimeError('Pin for emergency switch in position 1 is not assigned')
                    return -1
                else:
                    return self.emergency1_timesPressed
            else:
                raise RuntimeError('Emergency switch can only be assigned to position 1')
                return -1

        else:
            raise RuntimeError('Unknown sensor type!')
            return -1

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

