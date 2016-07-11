import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Motor:

    def __init__(self, cA1p, cA2p, cB1p, cB2p):

        self.coil_A_1_pin = cA1p
        self.coil_A_2_pin = cA2p
        self.coil_B_1_pin = cB1p
        self.coil_B_2_pin = cB2p

        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)



    #if everything OK, return 0. If delay or steps < 0, return -1
    def forwards(self,delay, steps):

        if delay < 0:

            raise RuntimeError('Motor delay can only be a positive number!')
            return -1

        elif steps < 0:

            raise RuntimeError('Motor steps can only be a positive number!')
            return -1

        else:

            for i in range(0, steps):

                self.setStep(0,0,1,1)
                time.sleep(delay)
                self.setStep(1,0,0,1)
                time.sleep(delay)
                self.setStep(1,1,0,0)
                time.sleep(delay)
                self.setStep(0,1,1,0)
                time.sleep(delay)

            return 0


    #if everything OK, return 0. If delay or steps < 0, return -1
    def backwards(self,delay, steps):

        if delay < 0:

            raise RuntimeError('Motor delay can only be a positive number!')
            return -1

        elif steps < 0:

            raise RuntimeError('Motor steps can only be a positive number!')
            return -1

        else:

            for i in range(0, steps):

                self.setStep(0,1,1,0)
                time.sleep(delay)
                self.setStep(1,1,0,0)
                time.sleep(delay)
                self.setStep(1,0,0,1)
                time.sleep(delay)
                self.setStep(0,0,1,1)
                time.sleep(delay)

            return 0


    def setStep(self, w1,w2,w3,w4):

        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def stopMotors(self):

        self.setStep(0, 0, 0 ,0)
