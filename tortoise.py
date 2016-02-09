from motors import Motor

class Tortoise:

	def __init__(self):
		self.A = Motor(4, 17, 23, 24)
		self.B = Motor(14, 15, 18, 27)


	def main(self):
		while True:
			delay = raw_input("Delay between steps (milliseconds)?")	
			steps = raw_input("How many steps forward? ")
			self.A.forward(int(delay) / 1000.00, int(steps))
			steps = raw_input("How many steps backwards? ")
			self.A.backwards(int(delay) / 1000.00, int(steps))

