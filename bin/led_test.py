from lib.leds import Leds
import time

leds = Leds()
leds.set(Leds.RED)
time.sleep(1)
leds.set(Leds.BLUE)
time.sleep(1)
leds.set(Leds.GREEN)
time.sleep(1)
leds.set(Leds.WHITE)
time.sleep(1)
leds.set(Leds.OFF)
time.sleep(1)
