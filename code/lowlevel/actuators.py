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

    def initActuator(self, actuator_type, pos, pin):

        if actuator_type == enums.ActuatorType.led:

            if pos == 1:
                self.led_pin1 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            elif pos == 2:
                self.led_pin2 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            elif pos == 3:
                self.led_pin3 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            elif pos == 4:
                self.led_pin4 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            elif pos == 5:
                self.led_pin5 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            elif pos == 6:
                self.led_pin6 = pin
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)    


    def setActuator(self,actuator_type,pos,value):

        if actuator_type == enums.ActuatorType.led:
            if pos == 1:

                if(self.led_pin1 == -1) :           
                    raise RuntimeError('Pin for led in position 1 not assigned')
                else:
                    return GPIO.output(self.led_pin1,value)

            elif pos == 2:

                if(self.led_pin2 == -1) :           
                    raise RuntimeError('Pin for led in position 2 not assigned')
                else:
                    return GPIO.output(self.led_pin2,value)

            elif pos == 3:

                if(self.led_pin3 == -1) :           
                    raise RuntimeError('Pin for led in position 3 not assigned')
                else:
                    return GPIO.output(self.led_pin3,value)

            elif pos == 4:

                if(self.led_pin4 == -1) :           
                    raise RuntimeError('Pin for led in position 4 not assigned')
                else:
                    return GPIO.output(self.led_pin4,value)

            elif pos == 5:

                if(self.led_pin5 == -1) :           
                    raise RuntimeError('Pin for led in position 5 not assigned')
                else:
                    return GPIO.output(self.led_pin5,value)

            elif pos == 6:

                if(self.led_pin6 == -1) :           
                    raise RuntimeError('Pin for led in position 6 not assigned')
                else:
                    return GPIO.output(self.led_pin6,value)

