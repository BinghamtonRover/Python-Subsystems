import pigpio
import time
from os import system

RED_PIN = 19
GREEN_PIN = 13
BLUE_PIN = 26
PWM_PIN = 17

class Leds: 
	"""A helper class that manages the LED strip.

	This class uses PiGPIO to manage the GPIO pins on the Pi, which requires the pigpiod daemon.
	"""
	def __init__(self): 
		self.init_pigpiod()
		self.gpio.set_mode(RED_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(GREEN_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(BLUE_PIN, pigpio.OUTPUT)
		self.gpio.set_mode(PWM_PIN, pigpio.INPUT)
		self.gpio.set_pull_up_down(PWM_PIN, 2)
		print("Initialized LED strip")

	def init_pigpiod(self): 
		self.gpio = pigpio.pi()
		if self.gpio.connected: return
		print("[Error] Could not initialize pigpiod")
		quit()

	def set(self, color):
		"""Sets the LED strip to [color], a Protobuf [Color] message."""
		self.gpio.set_PWM_dutycycle(RED_PIN, color.red*255)
		self.gpio.set_PWM_dutycycle(GREEN_PIN, color.green*255)
		self.gpio.set_PWM_dutycycle(BLUE_PIN, color.blue*255)
