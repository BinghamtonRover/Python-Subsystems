import pigpio
import time
from os import system

RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
WHITE = (1, 1, 1)
OFF = (0, 0, 0)

RED_PIN = 19
GREEN_PIN = 13
BLUE_PIN = 26
PWM_PIN = 17

class Leds: 
	def init_pigpiod(self): 
		self.gpio = pigpio.pi()
		if self.gpio.connected: return
		system("sudo pigpiod")
		time.sleep(1)
		if not self.gpio.connected: 
			print("[Error] Could not initialize pigpiod")
			quit()		

	def __init__(self): 
		self.init_pigpiod()
		self.gpio.set_mode(RED_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(GREEN_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(BLUE_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(PWM_PIN, pigpio.INPUT)
		self.gpio.set_pull_up_down(PWM_PIN, 2)
		print("Initialized LED strip")

	def set(self, color):
		r, g, b = color
		self.gpio.write(RED_PIN, r)
		self.gpio.write(GREEN_PIN, g)
		self.gpio.write(BLUE_PIN, b)
