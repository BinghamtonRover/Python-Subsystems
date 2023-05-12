import time

from network import ProtoSocket, Device
from network.generated import UpdateSetting, Color, Connect
from lib.leds import *

socket = ProtoSocket(port=8000, device=Device.DASHBOARD, destination=("127.0.0.1", 8001))
socket.send_message(Connect(sender=Device.DASHBOARD, receiver=Device.SUBSYSTEMS))
red = Color(red=1, green=0, blue=0)
green = Color(red=0, green=1, blue=0)
blue = Color(red=0, green=0, blue=1)
custom = Color(red=0.75, green=0, blue=0.25)

if __name__ == '__main__':
# 	while True: socket.send_message(UpdateSetting(color=None))
	socket.send_message(UpdateSetting(color=red))
	time.sleep(0.2)
	socket.send_message(UpdateSetting(color=blue))
	time.sleep(0.2)
	socket.send_message(UpdateSetting(color=green))
	time.sleep(0.2)
	socket.send_message(UpdateSetting(color=custom))
	time.sleep(0.2)
	socket.send_message(UpdateSetting(color=None))
