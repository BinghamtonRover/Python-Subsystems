import os
os.system("sudo ip link set can0 up type can bitrate 500000")

import lib.constants as constants
from network import ProtoSocket
from lib.can_to_udp import CanToUdp
from lib.udp_to_can import UdpToCan

class Subsystems: 
	def __init__(self): 
		self.udp = UdpToCan(8001, self)
		self.can = CanToUdp(self, test=True)

	def close(self): 
		self.can.stop_driving()
		self.udp.close()

subsystems = Subsystems()
subsystems.can.mock_send()
try: subsystems.udp.listen()
finally: subsystems.close()
