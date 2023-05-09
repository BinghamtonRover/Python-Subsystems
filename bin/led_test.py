import time

from network import ProtoSocket, Device
from network.generated import UpdateSettings, Color
from lib.leds import *

socket = ProtoSocket(port=8000, device=Device.DASHBOARD, destination=("127.0.0.1", 8001))
red = Color(red=1, green=0, blue=0)
green = Color(red=0, green=1, blue=0)
blue = Color(red=0, green=0, blue=1)
custom = Color(red=0.75, green=0, blue=0.25)

if __name__ == '__main__':
	socket.send_message(UpdateSettings(color=red))
	time.sleep(1)
	socket.send_message(UpdateSettings(color=red))
	time.sleep(1)
	socket.send_message(UpdateSettings(color=red))
	time.sleep(1)
	socket.send_message(UpdateSettings(color=custom))
