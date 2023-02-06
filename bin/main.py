import lib.constants as constants
from lib.can_to_udp import CanToUdp
from lib.udp_to_can import UdpToCan

can = CanToUdp()
server = UdpToCan(constants.SUBSYSTEMS_DATA_PORT, can)
server.start()
