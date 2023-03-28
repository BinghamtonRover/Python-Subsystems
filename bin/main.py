import os
os.system("sudo ip link set can0 up type can bitrate 500000")

import lib.constants as constants
from network import ProtoSocket
from lib.can_to_udp import CanToUdp
from lib.udp_to_can import UdpToCan

class Subsystems: 
	def __init__(self): 
		udp = UdpToCan(8001, self)
		can = CanToUdp(self, test=True)
		udp.listen()

	def close(self): 
		self.can.stop_driving()
		self.udp.close()

Subsystems()
