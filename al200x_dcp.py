# AL200X DCU settings
# add names and return a tuple; can elements be named?
class dcu_setting:
    def __init__(self, id, length, name):
        self.id = id; self.length = length
        self.name = name

Active_Emid = dcu_setting(167, 4, 'Active Emid')
Add_Destination_Address = dcu_setting(110, 1, 'Add Destination Address')
Add_Path_Service_Enabled = dcu_setting(105, 1, 'Add Path Service Enabled')
AGC_time = dcu_setting(195, 2, 'AGC time')
Alert_Carrier = dcu_setting(261, 2, 'Alert Carrier')
Alert_Tail = dcu_setting(262, 2, 'Alert Tail')
ALERT_Transmit_Message_Format = dcu_setting(225, 1, 'ALERT Transmit Message Format')
Basic_Advanced = dcu_setting(363, 1, 'Basic Advanced')
Basic_Peripherals = dcu_setting(350, 2, 'Basic Peripherals')
Carrier_Only_time = dcu_setting(190, 2, 'Carrier Only time')
Center_Transmission = dcu_setting(158, 1, 'Center Transmission')
Destination_Address = dcu_setting(100, 2, 'Destination Address')
Enable_TDMA = dcu_setting(157, 1, 'Enable TDMA')
Encrypt_Outgoing_Messages = dcu_setting(165, 1, 'Encrypt Outgoing Messages')
Encryption_Key_Rotation_Time = dcu_setting(164, 4, 'Encryption Key Rotation Time')
Encryption_Key_Status = dcu_setting(169, 50, 'Encryption Key Status')
Encryption_Remove_Key = dcu_setting(172, 1, 'Encryption Remove Key')
FEC_Mode = dcu_setting(156, 1, 'FEC Mode')
GPS_Update_Period = dcu_setting(170, 2, 'GPS Update Period')
GPS_Update_Timeout = dcu_setting(175, 2, 'GPS Update Timeout')
Hold_off_Time = dcu_setting(228, 1, 'Hold off Time')
Hop_Limit = dcu_setting(130, 1, 'Hop Limit')
Inter_packet_Spacing = dcu_setting(227, 1, 'Inter packet Spacing')
Invert_Modulation = dcu_setting(205, 1, 'Invert Modulation')
Last_GPS_Fix = dcu_setting(185, 30, 'Last GPS Fix')
Leap_Seconds = dcu_setting(187, 1, 'Leap Seconds')
Load_Peripherals = dcu_setting(357, 1, 'Load Peripherals')
Mark_Space = dcu_setting(229, 1, 'Mark Space')
Modulation_Voltage = dcu_setting(210, 2, 'Modulation Voltage')
MSR_IND = dcu_setting(355, 1, 'MSR IND')
Multi_Sensor_Report = dcu_setting(356, 1, 'Multi Sensor Report')
New_Active_Key = dcu_setting(166, 48, 'New Active Key')
New_EMID = dcu_setting(168, 4, 'New EMID')
New_Pending_Key = dcu_setting(174, 50, 'New Pending Key')
Operation_Mode = dcu_setting(45, 1, 'Operation Mode')
OS_Version = dcu_setting(1, 48, 'OS Version')
P1_Report = dcu_setting(354, 1, 'P1 Report')
Peripheral_List = dcu_setting(351, 2, 'Peripheral List')
Peripheral_Monitor = dcu_setting(361, 2, 'Peripheral Monitor')
Preamble_Time = dcu_setting(226, 2, 'Preamble Time')
Radio_Power_Up_Mode = dcu_setting(215, 1, 'Radio Power Up Mode')
Radio_Warm_Up = dcu_setting(220, 4, 'Radio Warm Up')
RF_Tail_Time = dcu_setting(200, 2, 'RF Tail Time')
RS232_Baud_Rate = dcu_setting(50, 1, 'RS232 Baud Rate')
RS232_HW_Flow_Control = dcu_setting(61, 1, 'RS232 HW Flow Control')
RS232_Parity = dcu_setting(55, 1, 'RS232 Parity')
RS232_Stop_Bits = dcu_setting(60, 1, 'RS232 Stop Bits')
Sensor_Scan_Interval = dcu_setting(260, 2, 'Sensor Scan Interval')
Sensor_Scan_Offset = dcu_setting(265, 4, 'Sensor Scan Offset')
Station_Source_Address = dcu_setting(95, 2, 'Station Source Address')
TBR_Accumulator = dcu_setting(358, 2, 'TBR Accumulator')
TBR_Maximum = dcu_setting(300, 4, 'TBR Maximum')
TBR_ZeroDate = dcu_setting(301, 4, 'TBR ZeroDate')
TBR_ZeroSchedule = dcu_setting(302, 1, 'TBR ZeroSchedule')
TDMA_Bytes_Remaining = dcu_setting(280, 2, 'TDMA Bytes Remaining')
TDMA_Frame_Length = dcu_setting(155, 4, 'TDMA Frame Length')
TDMA_Slot_Length = dcu_setting(160, 2, 'TDMA Slot Length')
TDMA_Slot_Overrun_Behavior = dcu_setting(159, 1, 'TDMA Slot Overrun Behavior')
TDMA_Slot_Padding = dcu_setting(162, 2, 'TDMA Slot Padding')
TDMA_Slot_Start_Offset = dcu_setting(152, 4, 'TDMA Slot Start Offset')
Test_Mode = dcu_setting(47, 1, 'Test Mode')
Timestamp_Service_Request_Enabled = dcu_setting(115, 1, 'Timestamp Service Request Enabled')

settings = {
1:  'OS Version',
45:  'Operation Mode',
47:  'Test Mode',
50:  'RS232 Baud Rate',
55:  'RS232 Parity',
60:  'RS232 Stop Bits',
61:  'RS232 HW Flow Control',
95:  'Station Source Address',
100:  'Destination Address',
105:  'Add Path Service Enabled',
110:  'Add Destination Address',
115:  'Timestamp Service Request Enabled',
130:  'Hop Limit',
152:  'TDMA Slot Start Offset',
155:  'TDMA Frame Length',
156:  'FEC Mode',
157:  'Enable TDMA',
158:  'Center Transmission',
159:  'TDMA Slot Overrun Behavior',
160:  'TDMA Slot Length',
162:  'TDMA Slot Padding',
164:  'Encryption Key Rotation Time',
165:  'Encrypt Outgoing Messages',
166:  'New Active Key',
167:  'Active Emid',
168:  'New EMID',
169:  'Encryption Key Status',
170:  'GPS Update Period',
172:  'Encryption Remove Key',
174:  'New Pending Key',
175:  'GPS Update Timeout',
185:  'Last GPS Fix',
187:  'Leap Seconds',
190:  'Carrier Only time',
195:  'AGC time',
200:  'RF Tail Time',
205:  'Invert Modulation',
210:  'Modulation Voltage',
215:  'Radio Power Up Mode',
220:  'Radio Warm Up',
225:  'ALERT Transmit Message Format',
226:  'Preamble Time',
227:  'Inter packet Spacing',
228:  'Hold off Time',
229:  'Mark Space',
260:  'Sensor Scan Interval',
261:  'Alert Carrier',
262:  'Alert Tail',
265:  'Sensor Scan Offset',
280:  'TDMA Bytes Remaining',
300:  'TBR Maximum',
301:  'TBR ZeroDate',
302:  'TBR ZeroSchedule',
350:  'Basic Peripherals',
351:  'Peripheral List',
354:  'P1 Report',
355:  'MSR IND',
356:  'Multi Sensor Report',
357:  'Load Peripherals',
358:  'TBR Accumulator',
361:  'Peripheral Monitor',
363:  'Basic Advanced',
}