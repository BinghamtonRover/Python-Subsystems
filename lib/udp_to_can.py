from lib.network import ProtoServer
from lib.network.generated.Protobuf.core_pb2 import *
from lib.constants import NAME_TO_CAN_ID

heartbeat_interval = 5  # in seconds

class UdpToCan(ProtoServer):
	def __init__(self, port, can, client): 
		self.can = can
		self.client = client
		self.received_handshake = False
		self.dashboard_ip = None
		self.server_loop_count = 0
		super().__init__(port)

	def is_connected(self): return self.dashboard_ip is not None

	# Overriden from UdpServer
	def on_loop(self):
		# Every 10 server checks is about a second
		self.server_loop_count += 1
		if self.server_loop_count != (heartbeat_interval * 10): return
		self.server_loop_count = 0

		print("Checking for heartbeat")

		if not self.received_handshake: 
			if self.is_connected(): self.on_disconnect()
		else: self.received_handshake = False

	def on_disconnect(self): 
		print("Handshake not received. Assuming Dashboard has disconnected")
		self.dashboard_ip = None
		self.client.address = None
		self.can.stop_driving()

	# This function comes from ProtoServer -- do not rename
	def on_message(self, wrapper, source): 
		if wrapper.name == Connect.DESCRIPTOR.name: 
			handshake = Connect.FromString(wrapper.data)
			if handshake.receiver != Device.SUBSYSTEMS: 
				print(f"Received a misaddressed handshake intended for {handshake.receiver}, sent by {handshake.sender}")
			self.received_handshake = True
			self.dashboard_ip = source[0]
			self.client.address = self.dashboard_ip
			self.client.send_message(Connect(sender=Device.SUBSYSTEMS, receiver=Device.DASHBOARD))
		elif len(wrapper.data) > 8: 
			print(f"{wrapper.name} is {len(wrapper.data)} bytes long, but CAN only supports 8")
		elif wrapper.name not in NAME_TO_CAN_ID: 
			print(f"No handler for {wrapper.name}")
		else: 
			id = NAME_TO_CAN_ID[wrapper.name]
			print(f"Received UDP message {wrapper.name}, sending CAN message to {id}")
			self.can.send(id, wrapper.data)
