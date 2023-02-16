import can

from lib.errors import SubsystemException
import lib.constants as constants

CAN_VERBOSE = True

class SubsystemsListener: 
	def __init__(self, client): 
		self.handlers = { }  # id: handler
		self.client = client

	def __call__(self, message): self.on_message_received(message)

	def on_message_received(self, message): 
		id = message.arbitration_id
		# NOTE: Calling socket.recvfrom causes a CAN frame of ID=4 to be detected. 
		# Does not occur in candump, only in python-can with socketcan
		if id == 4: return

		if id not in constants.CAN_ID_TO_NAME: print(f"  Unrecognized ID")
		else: 
			name = constants.CAN_ID_TO_NAME[id]
			print(f"  Message recognized as a {name} object")
			self.client.send_raw(name, bytes(message.data), constants.DASHBOARD_IP, constants.DASHBOARD_DATA_PORT)

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
