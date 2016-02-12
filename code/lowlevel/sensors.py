import thread
import RPi.GPIO as GPIO
import time

class Sensor:

    def __init__(self,ls_1,ls_2,sw_1,sw_2,sw_3,sw_4,sw_5,sw_6,pr_1,pr_2):

        self.busy = False
        self.touch = 0
        self.light = 1
        self.proximity = 2

        self.ls1 = ls_1
        self.ls2 = ls_2
        self.sw1 = sw_1
        self.sw2 = sw_2
        self.sw3 = sw_3
        self.sw4 = sw_4
        self.sw5 = sw_5
        self.sw6 = sw_6
        self.pr1 = pr_1
        self.pr2 = pr_2

        GPIO.setup(self.ls1, GPIO.OUT)
        GPIO.setup(self.ls2, GPIO.OUT)
        GPIO.setup(self.sw1, GPIO.IN)
        GPIO.setup(self.sw2, GPIO.IN)
        GPIO.setup(self.sw3, GPIO.IN)
        GPIO.setup(self.sw4, GPIO.IN)
        GPIO.setup(self.sw5, GPIO.IN)
        GPIO.setup(self.sw6, GPIO.IN)
        GPIO.setup(self.pr1, GPIO.IN)
        GPIO.setup(self.pr2, GPIO.IN)

        try:
            thread.start_new_thread(self.poll_sensors, (500,))
        except:
            print "Error: unable to start thread"

    def readSensor(self,sensor_type,pos):
        while self.busy == true:
            pass
        if sensor_type == self.touch:
            if pos == 1:
                return self.touch1
            elif pos == 2:
                return self.touch2
            elif pos == 3:
                return self.touch3
            elif pos == 4:
                return self.touch4
            elif pos == 5:
                return self.touch5
            elif pos == 6:
                return self.touch6
        elif sensor_type == self.light:
            if pos == 1:
                return self.light1
            elif pos == 2:
                return self.light2
        else:
            if pos == 1:
                return self.proximity1
            elif pos == 2:
                return self.proximity2

    def poll_sensors(self,delay):
        while 1:
            self.busy = True
            self.light1 = self.read_light(self.ls1)
            self.light2 = self.read_light(self.ls2)
            self.touch1 = GPIO.input(self.sw1)
            self.touch2 = GPIO.input(self.sw2)
            self.touch3 = GPIO.input(self.sw3)
            self.touch4 = GPIO.input(self.sw4)
            self.touch5 = GPIO.input(self.sw5)
            self.touch6 = GPIO.input(self.sw6)
            self.proximity1 = GPIO.input(self.pr1)
            self.proximity2 = GPIO.input(self.pr2)
            self.busy = False
            time.sleep(delay)

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

