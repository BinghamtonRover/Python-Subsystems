import os
os.system("sudo ip link set can0 up type can bitrate 500000")

import lib.constants as constants
from network import ProtoSocket
from lib.can_to_udp import CanToUdp
from lib.udp_to_can import UdpToCan

class Subsystems: 
	def __init__(self): 
		self.udp = UdpToCan(8001, self)
		self.can = CanToUdp(self)

	def close(self): 
		self.can.stop_driving()
		self.udp.close()

subsystems = Subsystems()

try: 
	while True: 
		try: subsystems.udp.listen()
		except KeyboardInterrupt: break
		except OSError as error: 
			if error.errno == 10054: continue
			else: raise error
finally: subsystems.close()
