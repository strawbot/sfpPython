# parameter, command and message type definitions
addresslistquery = 0x3B
tdmabytesremaining = 0x52
getgpsleapseconds = 0x71
apiversionnumber = 0x75
clockstatus = 0x7F
lastnvsavestatus = 0x8080
encryptionlistaddresseswithkeys = 0x8088
versionstring = 0x96
currentserialportnumber = 0x900C
currentipaddress = 0x9017
indaddress = 0x18
destinationaddress = 0x19
addpathservice = 0x1A
adddestinationaddress = 0x1B
concentrationtestflag = 0x1E
concentrationpduid = 0x20
applicationpdutimestampservice = 0x28
addresslistselection = 0x31
addresslistenabled = 0x32
addresslistaction = 0x33
addresslisttype = 0x34
addpathoverride = 0x39
reportrejectedmessages = 0x3A
echosuppression = 0x3F
hoplimit = 0x40
eerdsenable = 0x41
eerdsretransmitdelay = 0x42
eerdsmaximumretransmissions = 0x43
tdmaframelength = 0x48
tdmaslotlength = 0x4A
tdmaslotoffset = 0x4B
gpsupdateperiod = 0x4C
gpsupdatetimeout = 0x4D
tdmaslotpadding = 0x4E
tdmacentertransmission = 0x4F
enabletdma = 0x50
tdmaslotoverrunbehavior = 0x51
statusreportintervalhours = 0x56
statusreportoffsetminutes = 0x57
carrieronlytime = 0x60
agctime = 0x61
rftailtime = 0x62
invertmodulation = 0x63
fecmode = 0x64
transmitradioalwayson = 0x65
transmitradiowarmuptime = 0x66
transmitaudiomodulationvoltage = 0x68
agencyidentifier = 0X77
indtimedaymillisecondsformat = 0x7C
indtimeextendedformat = 0x7D
indtimesecondssince2010 = 0x7E
encryptoutgoingmessages = 0x8082
encryptionaddresstoconfigure = 0x8083
encryptionkeyrotationtime = 0x8084
encryptionemid = 0x8087
baudrate = 0x9000
parity = 0x9001
stopbits = 0x9002
flowcontrol = 0x9003
timeout = 0x9006
serialporttoconfigure = 0x9007
serialportinputmode = 0x9008
independentaddressingenabled = 0x9009
portaddress = 0x900A
outputmode = 0x900B
dhcpenabled = 0x9010
iov4addressstatic = 0x9011
ipv4subnetmask = 0x9012
ipv4gateway = 0x9013
ipv4dnsservers = 0x9014
clocksource = 0x9015
ntpservers = 0x9016
ipv6addressstatic = 0x9018
ipv6subnetmask = 0x9019
ipv6gateway = 0x901A
ipv6dnsservers = 0x901B
addresslistaddlist = 0x35
addresslistaddrange = 0x36
addresslistremovelist = 0x37
addresslistremoverange = 0x38
encryptionsetkey = 0x8085
encryptionremovekey = 0x8086
ALERT2_SelfReport = 0x00
ALERT2_Concentration = 0x01
ALERT2_Configuration_Control = 0x02
Set_Parameter = 0x0A
Get_Parameter = 0x0B
Forward_ALERT2_Messages = 0x10
Initiate_GPS_Cycles = 0x70
Save_Configuration = 0x78
Query_Current_Configuration = 0x79
Reset_Configuration_to_Defaults = 0x7A
Load_Configuration = 0x7B
TLV_Exists = 0x8081
ALERT2_Data_Envelope = 0x10
AirLink_PDU_Envelope = 0x14
MANT_PDU_Envelope = 0x15
MANT_Header = 0x8400
MANT_Payload = 0x8401
MANT_Authentic = 0x8404
MANT_Error = 0x8405
MANT_Error_Description = 0x8406
AirLink_Header = 0x844C
AirLink_Payload = 0x844D
AirLink_FEC_Mode = 0x844E
AirLink_Total_Symbol_Errors_Corrected = 0x844F
AirLink_Symbol_Errors_Corrected = 0x8450
AirLink_Frame_Length = 0x8451
AirLink_Noise_Level = 0x8452
Number_MANT_PDUs_Seccessfully_Decoded = 0x8453
AirLink_Error = 0x8454
AirLink_Error_Description = 0x8455



