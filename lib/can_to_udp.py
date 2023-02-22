import can
import logging
logging.basicConfig(level=logging.CRITICAL)

import lib.constants as constants
from lib.network.generated.Protobuf.drive_pb2 import *
from lib.errors import SubsystemException

logging.disable(logging.CRITICAL)
CAN_VERBOSE = True

class SubsystemsListener: 
	def __init__(self, client): 
		self.handlers = { }  # id: handler
		self.client = client

	def __call__(self, message): self.on_message_received(message)

	def on_message_received(self, message): 
		id = message.arbitration_id
		# NOTE: Calling socket.recvfrom causes a CAN frame of random IDs to be detected. 
		# Does not occur in candump, only in python-can with socketcan
		if id not in constants.CAN_ID_TO_NAME: return 
		else: 
			name = constants.CAN_ID_TO_NAME[id]
			if self.client.address is None: return  # dashboard is not connected
			self.client.send_raw(name, bytes(message.data))

class CanToUdp: 
	def __init__(self, client, test=False): 
		if (test): 
			self.bus = can.interface.Bus('test_receive', bustype="virtual")
		else: 
			self.bus = can.interface.Bus(interface="socketcan", channel="can0", fd=False)

		self.listener = SubsystemsListener(client)
		self.notifier = can.Notifier(self.bus, [self.listener])

	def send(self, id, data): 
		message = can.Message(arbitration_id=id, data=data, is_fd=False, is_extended_id=False)
		print(f"Sending {message}")
		self.bus.send(message)

	def mock_send(self, id, data):  # sends without using the bus
		message = can.Message(arbitration_id=id, data=data)
		self.listener.on_message_received(message)

	def stop_driving(self): 
		command1 = DriveCommand(set_left=True, left=0)
		command2 = DriveCommand(set_right=True, right=0)
		command3 = DriveCommand(set_throttle=True, throttle=0)
		self.send(0x53, command1.SerializeToString())
		self.send(0x53, command2.SerializeToString())
		self.send(0x53, command3.SerializeToString())
