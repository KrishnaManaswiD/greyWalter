import RPi.GPIO as GPIO
import time
import enums

GPIO.setmode(GPIO.BCM)

class Actuators:

    def __init__(self):

        self.busy = False
        self.led = 0

        self.led_pin1 = -1
        self.led_pin2 = -1
        self.led_pin3 = -1
        self.led_pin4 = -1
        self.led_pin5 = -1
        self.led_pin6 = -1

    #if everything OK, return 0. If actuator type unknown or position > limit, return -1
    def initActuator(self, actuator_type, pos, pin):

        if actuator_type == enums.ActuatorType.led:

            if pos == 1:
                self.led_pin1 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            elif pos == 2:
                self.led_pin2 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            elif pos == 3:
                self.led_pin3 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            elif pos == 4:
                self.led_pin4 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            elif pos == 5:
                self.led_pin5 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            elif pos == 6:
                self.led_pin6 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
                return 0
            else:
                raise RuntimeError('LED can only be assigned to position 1-6')
                return -1

        else:
            raise RuntimeError('Unknown actuator type!')
            return -1

    #if everything OK, return 0. If actuator type unknown or position > limit or value is not (0 or 1), return -1
    def setActuator(self,actuator_type,pos,value):
        if actuator_type == enums.ActuatorType.led:
            if not (value==1 or value==0):
                raise RuntimeError('LED value can only be 1 or 0!')
                return -1
            if pos == 1:
                if(self.led_pin1 == -1) :
                    raise RuntimeError('Pin for LED in position 1 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin1,value)
                    return 0
            elif pos == 2:
                if(self.led_pin2 == -1) :
                    raise RuntimeError('Pin for LED in position 2 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin2,value)
                    return 0
            elif pos == 3:
                if(self.led_pin3 == -1) :
                    raise RuntimeError('Pin for LED in position 3 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin3,value)
                    return 0
            elif pos == 4:
                if(self.led_pin4 == -1) :
                    raise RuntimeError('Pin for LED in position 4 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin4,value)
                    return 0
            elif pos == 5:
                if(self.led_pin5 == -1) :
                    raise RuntimeError('Pin for LED in position 5 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin5,value)
                    return 0
            elif pos == 6:
                if(self.led_pin6 == -1) :
                    raise RuntimeError('Pin for LED in position 6 is not assigned')
                    return -1
                else:
                    GPIO.output(self.led_pin6,value)
                    return 0
            else:
                raise RuntimeError('LED can only be assigned to position 1-6')
                return -1

        else:
            raise RuntimeError('Unknown actuator type!')
            return -1
