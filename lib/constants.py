def get_id(node, command): 
	return (node << 5) | command

# Data comes from this spreadsheet. Must be standardized across the firmware code
# https://docs.google.com/spreadsheets/d/1beRk89HpqvpsFLITcuTHR4fR-6Inla7YWBR8VH2ndbg/edit?pli=1#gid=0
NAME_TO_CAN_ID = {
	"DriveCommand": get_id(node=0x5, command=0x3),
	"ArmCommand": get_id(node=0x2, command=0x3),
	"GripperCommand": get_id(node=0x3, command=0x3),
	"ElectricalCommand": get_id(node=0x6, command=0x3),
	"ScienceCommand": get_id(node=0x4, command=0x3),
}

CAN_ID_TO_NAME = {
	get_id(node=0x1, command=0x3): "ElectricalData",
	get_id(node=0x1, command=0x4): "DriveData",
	get_id(node=0x1, command=0x5): "ArmData",
	get_id(node=0x1, command=0x6): "GripperData",
	get_id(node=0x1, command=0x7): "ScienceData",
	get_id(node=0x1, command=0x8): "AutonomyData",
}

# These must match the IPs and ports found in the following Google Doc: 

DASHBOARD_IP = "192.168.1.10"
DASHBOARD_DATA_PORT = 8008
SUBSYSTEMS_DATA_PORT = 8002
