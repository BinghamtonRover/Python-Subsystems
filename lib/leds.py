import pigpio
from os import system

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
		system("sudo pigpiod")
		self.gpio = pigpio.pi()
		if not self.gpio.connected:
			print("[Error] PiGPIO is not running")
			quit()
		print("Tank successfully initialized")
		self.gpio.set_mode(RED_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(GREEN_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(BLUE_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(PWM_PIN, pigpio.INPUT)
		self.gpio.set_pull_up_down(PWM_PIN, 2)

	def set(self, color):
		r, g, b = color
		self.gpio.write(RED_PIN, r)
		self.gpio.write(GREEN_PIN, g)
		self.gpio.write(BLUE_PIN, b)
