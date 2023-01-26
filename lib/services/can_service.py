from lib.errors import SubsystemException

import can

class SubsystemsListener: 
	def __init__(self): 
		self.handlers = { }  # id: handler

	def register_handler(self, id, handler): 
		self.handlers[id] = handler

	def on_message_received(self, message): 
		id = message.arbitration_id
		if id not in self.handlers: raise SubsystemException(f"No handler found for ID: {id}")
		self.handlers[id](message)

	def __call__(self, message): self.on_message_received(message)

class CanService: 
	def __init__(self, test=False): 
		if (test): 
			self.bus = can.interface.Bus('test_receive', bustype="virtual")
		else: 
			self.bus = can.interface.Bus(interface="socketcan", channel="can0", fd=False)

		self.listener = SubsystemsListener()
		self.notifier = can.Notifier(self.bus, [self.listener])

	def send(self, id, data): 
		message = can.Message(arbitration_id=id, data=data, is_fd=False)
		self.bus.send(message)

	def register_handler(self, id, handler): 
		self.listener.register_handler(id, handler)

	def mock_send(self, id, data):  # sends without using the bus
		message = can.Message(arbitration_id=id, data=data)
		self.listener.on_message_received(message)
