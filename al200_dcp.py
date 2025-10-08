# add names and return a tuple; can elements be named?

settings = {
1: 'OS Version',
30: 'Battery',
32: 'SE1 Scaled Reading',
33: 'P1 Total',
34: 'C1 Scaled Reading',
35: 'SE1 Raw Reading',
36: 'C1 Raw Reading',
45: 'Operation Mode',
46: 'Port Protocols',
47: 'Test Mode',
50: 'RS-232 Baud Rate',
55: 'RS-232 Parity',
60: 'RS-232 Stop Bits',
61: 'RS-232 HW Flow Control',
75: 'CS I/O SDC Address',
95: 'Station Source Address',
100: 'Destination Address',
105: 'Add Path Service Enabled',
110: 'Add Destination Address',
130: 'Hop Limit',
151: 'TDMA Slot Length',
152: 'TDMA Slot Start Offset',
155: 'TDMA Frame Length',
156: 'FEC Mode',
157: 'Enable TDMA',
158: 'Center Transmission',
159: 'TDMA Slot Overrun Behavior',
160: 'TDMA Slot Length',
162: 'TDMA Slot Padding',
164: 'Encryption Key Rotation Time',
165: 'Encrypt Outgoing Messages',
166: 'Encryption Set Key',
167: 'Active EMID',
168: 'Encryption EMID',
169: 'Encryption Key Status',
170: 'GPS Update Period',
171: 'Encryption Source Address To Configure',
172: 'Encryption Remove Key',
174: 'New Pending Key',
175: 'GPS Update Timeout',
185: 'Last GPS Fix',
186: 'Tick Lock Loop',
187: 'Leap Seconds',
190: 'Carrier Only time',
195: 'AGC time',
200: 'RF Tail Time',
205: 'Invert Modulation',
210: 'Modulation Voltage',
215: 'Radio Power Up Mode',
220: 'Radio Warm Up',
255: 'Multi-Sensor Report',
257: 'Self Report Interval',
260: 'Sensor Scan Interval',
262: 'Configuration Sensor Scan Interval',
265: 'SW12 Warm Up Time',
267: 'Clock Status in Self Report',
268: 'Clock Status Sensor ID',
270: 'P1 Enable',
280: 'TDMA Bytes Remaining',
310: 'SE1 Mode',
312: 'SE1 Sensor ID',
315: 'SE1 Transmitted',
316: 'Include Temperature',
314: 'Health',
317: 'C1 Transmitted',
325: 'SE1 Multiplier',
330: 'SE1 Offset',
340: 'SE1 Tx Change',
345: 'SDI-12 Command',
346: 'SDI-12 Value to Send',
347: 'C1 Sensor ID',
348: 'SDI-12 Multiplier',
349: 'SDI-12 Offset',
350: 'SDI-12 Tx Change',
355: 'C1 Mode',
356: 'C1 Status',
357: 'Load Peripherals',
358: 'TBR Accumulator',
359: 'DCU Peripheral Enable',
360: 'DCU Peripheral Definitions',
361: 'Peripheral Activity',
362: 'SDI-12 Sensors Mappin',
}

class dcu_setting:
    def __init__(self, id, length):
        self.id = id; self.length = length
        if id not in settings:
            settings[id] = '<unknown>%i'%id
        self.name = settings[id]

OS_Version = dcu_setting(1, 40)
Battery = dcu_setting(30, 4)
SE1_Scaled_Reading = dcu_setting(32, 4)
P1_Total = dcu_setting(33, 2)
SE1_Raw_Reading = dcu_setting(35, 4)
Operation_Mode = dcu_setting(45, 1)
Port_Protocols = dcu_setting(46, 40)
RS232_Baud_Rate = dcu_setting(50, 1)
RS232_Parity = dcu_setting(55, 1)
RS232_Stop_Bits = dcu_setting(60, 1)
RS232_HW_Flow_Control = dcu_setting(61, 1)
CS_IO_SDC_Address = dcu_setting(75, 1)
Station_Source_Address = dcu_setting(95, 2)
Destination_Address = dcu_setting(100, 2)
Add_Path_Service_Enabled = dcu_setting(105, 1)
Add_Destination_Address = dcu_setting(110, 1)
Hop_Limit = dcu_setting(130, 1)
TDMA_Slot_Start_Offset = dcu_setting(152, 4)
TDMA_Frame_Length = dcu_setting(155, 4)
FEC_Mode = dcu_setting(156, 1)
Enable_TDMA = dcu_setting(157, 1)
Center_Transmission = dcu_setting(158, 1)
TDMA_Slot_Overrun_Behavior = dcu_setting(159, 1)
TDMA_Slot_Length = dcu_setting(160, 2)
TDMA_Slot_Padding = dcu_setting(162, 2)
Encryption_New_Pending_Key_Rotation_Time = dcu_setting(164, 4)
Encrypt_Outgoing_Messages = dcu_setting(165, 1)
Encryption_New_Active_Key = dcu_setting(166, 33)
Encryption_Active_EMID = dcu_setting(167, 4)
Encryption_New_EMID = dcu_setting(168, 4)
Encryption_Key_Status = dcu_setting(169, 10)
GPS_Update_Period = dcu_setting(170, 2)
# Encryption_Source_Address_To_Configure = dcu_setting(171, 2)
Encryption_Remove_Keys = dcu_setting(172, 1)
Encryption_New_Pending_Key = dcu_setting(174, 33)
GPS_Update_Timeout = dcu_setting(175, 2)
Last_GPS_Fix = dcu_setting(185, 30)
Tick_Lock_Loop = dcu_setting(186, 40)
Carrier_Only_time = dcu_setting(190, 2)
AGC_time = dcu_setting(195, 2)
RF_Tail_Time = dcu_setting(200, 2)
Invert_Modulation = dcu_setting(205, 1)
Modulation_Voltage = dcu_setting(210, 2)
Radio_Power_Up_Mode = dcu_setting(215, 1)
Radio_Warm_Up = dcu_setting(220, 4)
Alert_Message_Format = dcu_setting(225, 1)
Alert_Hold_Off_Time = dcu_setting(228, 1)
Alert_Preamble_Time = dcu_setting(226, 2)
Alert_Packet_Spacing = dcu_setting(227, 1)
Alert_Tone_Frequency = dcu_setting(229, 1)
Alert_Carrier_Only_Time = dcu_setting(261, 2)
Alert_Tail_Time = dcu_setting(262, 2)
MultiSensor_Report = dcu_setting(255, 1)
Self_Report_Interval = dcu_setting(257, 4)
Sensor_Scan_Interval = dcu_setting(260, 2)
Configuration_Sensor_Scan_Interval = dcu_setting(262, 2)
SW12_Warm_Up_Time = dcu_setting(265, 1)
Clock_Status_in_Self_Report = dcu_setting(267, 1)
Clock_Status_Sensor_ID = dcu_setting(268, 1)
P1_Enable = dcu_setting(270, 1)
TDMA_Bytes_Remaining = dcu_setting(280, 2)
SE1_Mode = dcu_setting(310, 1)
SE1_Sensor_ID = dcu_setting(312, 1)
SE1_Transmitted = dcu_setting(315, 4)
C1_Transmitted = dcu_setting(317, 4)
SE1_Multiplier = dcu_setting(325, 4)
SE1_Offset = dcu_setting(330, 4)
SE1_Tx_Change = dcu_setting(340, 4)
C1_Sensor_ID = dcu_setting(347, 1)
C1_Mode = dcu_setting(355, 1)
C1_Status = dcu_setting(356, 4)
P1_Transmitted = dcu_setting(357, 2)
TBR_Accumulator = dcu_setting(358, 2)
SDI12_Sensor_Monitor = dcu_setting(361, 2)
ALERT2_to_SDI12_Sensors_Mapping = dcu_setting(362, 8)
Health = dcu_setting(314, 1)
Include_Temperature = dcu_setting(316, 1)