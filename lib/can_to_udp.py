import can
import sys
import logging
logging.basicConfig(level=logging.CRITICAL)

import lib.constants as constants
from lib.errors import SubsystemException
from network.generated import DriveCommand, DriveData, WrappedMessage

logging.disable(logging.CRITICAL)
CAN_VERBOSE = True

class SubsystemsListener: 
	def __init__(self, subsystems): 
		self.handlers = { }  # id: handler
		self.subsystems = subsystems

	def __call__(self, message): self.on_message_received(message)

	def on_message_received(self, message): 
		id = message.arbitration_id
		# NOTE: Calling socket.recvfrom causes a CAN frame of random IDs to be detected. 
		# Does not occur in candump, only in python-can with socketcan
		if id not in constants.CAN_ID_TO_NAME: return 
		name = constants.CAN_ID_TO_NAME[id]
		# print(f"Received {name} message from can ID {hex(id)}: {''.join(hex(x)[2:].zfill(2) for x in message.data)}")
		if self.subsystems.udp.destination is None: return  # dashboard is not connected
		message = WrappedMessage(name=name, data=bytes(message.data))
		self.subsystems.udp.send(message.SerializeToString())
		if name == "DriveData":  # needs to be forwarded to the autonomy Pi
			print(f"Got ultrasonic: {bytes(message.data)}")
			self.subsystems.udp.send(message.SerializeToString(), address="192.168.1.30", port=8003)

class CanToUdp: 
	def __init__(self, subsystems, test=False): 
		if sys.platform != "linux": 
			print("[Warning]: Switching] to virtual CAN on non-Linux platform")
			test = True
		if (test): 
			self.bus = can.interface.Bus('test_receive', bustype="virtual")
		else: 
			self.bus = can.interface.Bus(interface="socketcan", channel="can0", fd=False)

		self.udp_socket = None
		self.listener = SubsystemsListener(subsystems)
		self.notifier = can.Notifier(self.bus, [self.listener])

	def send(self, id, data): 
		message = can.Message(arbitration_id=id, data=data, is_fd=False, is_extended_id=False)
		try: 
			# print(f"  Sent:{''.join(hex(x)[2:].zfill(2) for x in data)}")
			self.bus.send(message)
		except can.exceptions.CanOperationError as error: 
			print(f"  Error sending data to id={id}")

	def mock_send(self):  # sends without using the bus
		data = DriveData(left=0.75).SerializeToString()
		message = can.Message(arbitration_id=0x14, data=data)
		self.listener.on_message_received(message)

	def stop_driving(self): 
		command1 = DriveCommand(set_left=True, left=0)
		command2 = DriveCommand(set_right=True, right=0)
		command3 = DriveCommand(set_throttle=True, throttle=0)
		self.send(0x53, command1.SerializeToString())
		self.send(0x53, command2.SerializeToString())
		self.send(0x53, command3.SerializeToString())
