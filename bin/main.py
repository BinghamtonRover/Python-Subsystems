import os
os.system("sudo ip link set can0 up type can bitrate 500000")

import lib.constants as constants
from lib.network import ProtoClient
from lib.can_to_udp import CanToUdp
from lib.udp_to_can import UdpToCan

client = ProtoClient(address=constants.DASHBOARD_IP, port=constants.DASHBOARD_DATA_PORT)
can = CanToUdp(client)
server = UdpToCan(constants.SUBSYSTEMS_DATA_PORT, can, client)
server.start()
