def get_id(node, command): 
	return (node << 5) | command

# Data comes from this spreadsheet. Must be standardized across the firmware code
# https://docs.google.com/spreadsheets/d/1beRk89HpqvpsFLITcuTHR4fR-6Inla7YWBR8VH2ndbg/edit?pli=1#gid=0
NAME_TO_CAN_ID = {
	"DriveCommand": 0x53,
	"ArmCommand": 0x23,
	"GripperCommand": 0x33,
	"ElectricalCommand": 0x63,
	"ScienceCommand": 0x43,
}

CAN_ID_TO_NAME = {
	0x13: "ElectricalData",
	0x14: "DriveData",
	0x15: "ArmData",
	0x16: "GripperData",
	0x17: "ScienceData",
	0x18: "AutonomyData",
}

# These must match the IPs and ports found in the following Google Doc: 

DASHBOARD_DATA_PORT = 8008
SUBSYSTEMS_DATA_PORT = 8002
