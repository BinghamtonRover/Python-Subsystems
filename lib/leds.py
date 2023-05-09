import pigpio

class Leds: 
	RED = (1, 0, 0)
	GREEN = (0, 1, 0)
	BLUE = (0, 0, 1)
	WHITE = (1, 1, 1)
	OFF = (0, 0, 0)

	RED_PIN = 13
	GREEN_PIN = 19
	BLUE_PIN = 26
	PWM_PIN = 17

	def __init__(self): 
		self.pi = pigpio.pi()
		self.set_mode(RED_PIN, pigpio.OUTPUT)
		self.set_mode(GREEN_PIN, pigpio.OUTPUT)
		self.set_mode(BLUE_PIN, pigpio.OUTPUT)
		self.set_mode(PWM_PIN, pigpio.INPUT)
		self.set_pull_up_down(PWM_PIN, 2)

	def set(self, color):
		r, g, b = color
		pi.write(RED_PIN, r)
		pi.write(GREEN_PIN, g)
		pi.write(BLUE_PIN, b)
