import time 

from lib.network import ProtoServer
from lib.network.generated.Protobuf.core_pb2 import *
from lib.constants import NAME_TO_CAN_ID

heartbeat_interval = 1  # in seconds

class UdpToCan(ProtoServer):
	def __init__(self, port, can, client): 
		self.can = can
		self.client = client
		self.received_handshake = False
		self.dashboard_ip = None
		self.last_handshake_check = time.time()
		super().__init__(port)

	def is_connected(self): return self.dashboard_ip is not None

	# Overriden from UdpServer
	def on_loop(self):
		now = time.time()
		if (now - self.last_handshake_check < heartbeat_interval): return
		if not self.received_handshake: 
			if self.is_connected(): self.on_disconnect()
		else: self.received_handshake = False
		self.last_handshake_check = time.time()

	def on_disconnect(self): 
		print("Handshake not received. Assuming Dashboard has disconnected")
		self.dashboard_ip = None
		self.client.address = None
		self.can.stop_driving()

	def handle_handshake(self): 
		if handshake.receiver != Device.SUBSYSTEMS: 
			print(f"Received a misaddressed handshake intended for {handshake.receiver}, sent by {handshake.sender}")
		self.received_handshake = True
		self.dashboard_ip = source[0]
		self.client.address = self.dashboard_ip
		self.client.send_message(Connect(sender=Device.SUBSYSTEMS, receiver=Device.DASHBOARD))

	# This function comes from ProtoServer -- do not rename
	def on_message(self, wrapper, source): 
		if wrapper.name == Connect.DESCRIPTOR.name: 
			handshake = Connect.FromString(wrapper.data)
			self.handle_handshake(handshake)
		elif wrapper.name == UpdateSetting.DESCRIPTOR.name: 
			settings = UpdateSetting.FromString(wrapper.data)
			print(f"Received a request to update status={settings.status}")
		elif len(wrapper.data) > 8: 
			print(f"{wrapper.name} is {len(wrapper.data)} bytes long, but CAN only supports 8")
		elif wrapper.name not in NAME_TO_CAN_ID: 
			print(f"No handler for {wrapper.name}")
		else: 
			id = NAME_TO_CAN_ID[wrapper.name]
			# print(f"Received UDP message {wrapper.name}, sending CAN message to {id}")
			self.can.send(id, wrapper.data)
