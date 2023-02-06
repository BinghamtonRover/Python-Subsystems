from lib.network import ProtoServer
from lib.constants import NAME_TO_CAN_ID

class UdpToCan(ProtoServer):
	def __init__(self, port, can): 
		self.can = can
		super().__init__(port)

	# This function comes from ProtoServer -- do not rename
	def on_message(self, wrapper, source): 
		print("Received UDP message")
		if len(wrapper.data) > 8: 
			print(f"{wrapper.name} is {len(wrapper.data)} bytes long, but CAN only supports 8")
		elif wrapper.name not in NAME_TO_CAN_ID: 
			print(f"No handler for {wrapper.name}")
		else: 
			id = NAME_TO_CAN_ID[wrapper.name]
			print(f"Received UDP message {wrapper.name}, sending CAN message to {id}")
			self.can.send(id, wrapper.data)
