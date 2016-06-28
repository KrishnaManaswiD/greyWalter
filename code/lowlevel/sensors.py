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
        self.emergencyStop = 3

        self.lightSensor_pin = [-1,-1,-1]

        self.touchSensor_pin = [-1,-1,-1,-1]

        self.proximitySensor_pin = [-1,-1,-1,-1,-1]

        self.emergencyStop_pin = [-1,-1]

        self.light_value = [-1,-1,-1]
        self.touch_timesPressed = [0,0,0,0]
        self.proximity_state = [-1,-1,-1,-1,-1]

        self.emergency_timesPressed = [0,0]

#        try:
#            thread.start_new_thread(self.poll_sensors, (500,))
#        except:
#            print "Error: unable to start thread"

    #if everything OK, return 0. If sensor type unknown or position > limit, return -1
    def setSensor(self, sensor_type, pos, pin):
        if sensor_type == enums.SensorType.touch:
            if pos < len(self.touchSensor_pin) and pos > 0:
                self.touchSensor_pin[pos] = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0
            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-' + str(len(self.touchSensor_pin)-1))
                return -1

        elif sensor_type == enums.SensorType.light:
            if pos < len(self.lightSensor_pin) and pos > 0:
                self.lightSensor_pin[pos] = pin
                GPIO.setup(pin, GPIO.OUT)
                return 0
            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-' + str(len(self.lightSensor_pin)-1))
                return -1

        elif sensor_type == enums.SensorType.proximity:
            if pos < len(self.proximitySensor_pin) and pos > 0:
                self.proximitySensor_pin[pos] = pin
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                if GPIO.input(pin) == GPIO.HIGH:
                        self.proximity1_state = 0
                else:
                        self.proximity1_state = 1
                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 100)
                return 0
            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-' + str(len(self.proximitySensor_pin)-1))
                return -1

        elif sensor_type == enums.SensorType.emergencyStop:
            if pos < len(self.emergencyStop_pin) and pos > 0:
                self.emergencyStop_pin[pos] = pin
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
        for pos in range(1,len(self.touchSensor_pin)-1):
            if channel == self.touchSensor_pin[pos]:
                self.touch_timesPressed[pos] = self.touch_timesPressed[pos] + 1
                break
        for pos in range(1,len(self.emergencyStop_pin)-1):
            if channel == self.emergencyStop_pin[pos]:
                self.emergency_timesPressed[pos] = self.emergency1_timesPressed[pos] + 1
                break

    def callback_proximity(self,channel):
        time.sleep(0.1)
        for pos in range(1,len(self.proximitySensor_pin)-1):
            if channel == self.proximitySensor_pin[pos]:
                if GPIO.input(channel) == GPIO.HIGH:
                        self.proximity_state[pos] = 0
                else:
                        self.proximity_state[pos] = 1
                break

    #if everything OK, return sensor value. If sensor type unknown or position > limit, return -1
    def readSensor(self,sensor_type,pos):
        if sensor_type == enums.SensorType.touch:
            if pos < len(self.touchSensor_pin) and pos > 0:
                if(self.touchSensor_pin[pos] == -1) :
                    raise RuntimeError('Pin for touch sensor in position ' + str(pos) + ' is not assigned')
                    return -1
                else:
                    return self.touch_timesPressed[pos]
            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-' + str(len(self.touchSensor_pin)-1))
                return -1

        elif sensor_type == enums.SensorType.light:
            if pos < len(self.lightSensor_pin) and pos > 0:
                if(self.lightSensor_pin[pos] == -1):
                    raise RuntimeError('Pin for light sensor in position ' + str(pos) + ' is not assigned')
                    return -1
                else:
                    return self.read_light(self.lightSensor_pin[pos])
            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-' + str(len(self.lightSensor_pin)-1))
                return -1

        elif sensor_type == enums. SensorType.proximity:
            if pos < len(self.proximitySensor_pin) and pos > 0:
                if(self.proximitySensor_pin[pos] == -1):
                    raise RuntimeError('Pin for proximity sensor in position ' + str(pos) + ' is not assigned')
                    return -1
                else:
                    return self.proximity_state[pos]
            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-' + str(len(self.proximitySensor_pin)-1))
                return -1

        elif sensor_type == enums.SensorType.emergencyStop:
            if pos < len(self.emergencyStop_pin) and pos > 0:
                if(self.emergencyStop_pin[pos] == -1):
                    raise RuntimeError('Pin for emergency switch in position ' + str(pos) + ' is not assigned')
                    return -1
                else:
                    return self.emergency_timesPressed[pos]
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
        while (GPIO.input(lspin) == GPIO.LOW):
            reading += 1

        return reading

