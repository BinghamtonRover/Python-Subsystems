from lib.leds import *
import time

leds = Leds()
leds.set(RED)
time.sleep(1)
leds.set(GREEN)
time.sleep(1)
leds.set(BLUE)
time.sleep(1)
leds.set( (0.75, 0, 0.25) )
time.sleep(1)
leds.set(WHITE)
time.sleep(1)
leds.set(OFF)
time.sleep(1)
