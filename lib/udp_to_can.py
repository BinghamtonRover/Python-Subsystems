import time 

from lib.network import ProtoServer
from lib.network.generated.Protobuf.core_pb2 import *
from lib.network.generated.Protobuf.autonomy_pb2 import *
from lib.constants import NAME_TO_CAN_ID

heartbeat_interval = 1  # in seconds

class UdpToCan(ProtoServer):
	def __init__(self, port, can, client): 
		self.can = can
		self.client = client
		self.received_handshake = False
		self.last_handshake_check = time.time()
		self.status = RoverStatus.MANUAL
		super().__init__(port)

	def is_connected(self): return self.client.address is not None

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
		self.client.address = None
		self.can.stop_driving()

	def send_heartbeat(self): 
		response = Connect(sender=Device.SUBSYSTEMS, receiver=Device.DASHBOARD)
		self.client.send_message(response)
		self.received_handshake = True


	def on_handshake(self, handshake, source): 
		"""Decides what to do when a heartbeat message has been received

		- If the heartbeat was meant for another device, log it and ignore it
		- If we are not connected to any dashboard, connect to it and respond
		- If we are already connected to another dashboard, ignore it
		- If it is our dashboard, respond to it
		"""
		if handshake.receiver != Device.SUBSYSTEMS:  # not meant for us
			print(f"Received a misaddressed handshake intended for {handshake.receiever}, sent by {handshake.sender}")
		elif not self.is_connected():  # new dashboard, let's connect
			self.client.address = source[0]
			self.client.port = source[1]
			self.send_heartbeat()
		elif self.client.address != source[0]:
			# We're already connected to a dashboard, and a new one tried connecting -- ignore
			return
		else:  # heartbeat from the already-connected dashboard -- respond with a heartbeat back
			self.send_heartbeat()

	# This function comes from ProtoServer -- do not rename
	def on_message(self, wrapper, source): 
		if wrapper.name == Connect.DESCRIPTOR.name: 
			handshake = Connect.FromString(wrapper.data)
			self.on_handshake(handshake, source)
		elif wrapper.name == UpdateSetting.DESCRIPTOR.name: 
			settings = UpdateSetting.FromString(wrapper.data)
			print(f"Received a request to update status={settings.status}")
			self.client.send_message(settings)  # must send in return
			self.status = settings.status
			if settings.status == RoverStatus.AUTONOMOUS:
				self.client.send_message(AutonomyCommand(enable=True), address="192.168.1.30", port=8006)
			elif settings.status == RoverStatus.MANUAL:
				self.client.send_message(AutonomyCommand(enable=False), address="192.168.1.30", port=8006)

		elif len(wrapper.data) > 8: 
			print(f"{wrapper.name} is {len(wrapper.data)} bytes long, but CAN only supports 8")
		elif wrapper.name not in NAME_TO_CAN_ID: 
			print(f"No handler for {wrapper.name}")
		else: 
			id = NAME_TO_CAN_ID[wrapper.name]
			# print(f"Received UDP message {wrapper.name}, sending CAN message to {id}")
			self.can.send(id, wrapper.data)
