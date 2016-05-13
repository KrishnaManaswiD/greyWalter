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

		GPIO.setwarnings(False)

	def forward(self,delay, steps):
		for i in range(0, steps):
			self.setStep(0,0,1,1)
			time.sleep(delay)
			self.setStep(1,0,0,1)
			time.sleep(delay)
			self.setStep(1,1,0,0)
			time.sleep(delay)
			self.setStep(0,1,1,0)
			time.sleep(delay)

	def backwards(self,delay, steps):
		for i in range(0, steps):
			self.setStep(0,1,1,0)
			time.sleep(delay)
			self.setStep(1,1,0,0)
			time.sleep(delay)
			self.setStep(1,0,0,1)
			time.sleep(delay)
			self.setStep(0,0,1,1)
			time.sleep(delay)

	def setStep(self, w1,w2,w3,w4):
		GPIO.output(self.coil_A_1_pin, w1)
		GPIO.output(self.coil_A_2_pin, w2)
		GPIO.output(self.coil_B_1_pin, w3)
		GPIO.output(self.coil_B_2_pin, w4)

	def stopMotors(self):
		self.setStep(0, 0, 0 ,0)

