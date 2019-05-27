# generated file on 2019-05-27 11:12:50.451608. Do not edit!

class _statParam(): # _won't be imported
    def __init__(self, name, num, type, length):
        self.name = name
        self.num = num
        self.type = type
        self.length = length

LONG, CHAR, CELL, BYTE, BOOL = range(5)

# Stats
wdogResetCtr = _statParam("wdogResetCtr", 0, LONG, 1)
faultCtr = _statParam("faultCtr", 1, LONG, 1)
resetByFault = _statParam("resetByFault", 2, LONG, 1)
sdi12Errors = _statParam("sdi12Errors", 3, LONG, 1)
unsuportedSensor = _statParam("unsuportedSensor", 4, LONG, 1)
runNewImage = _statParam("runNewImage", 5, LONG, 1)
badImage = _statParam("badImage", 6, LONG, 1)
succesfulSample1 = _statParam("succesfulSample1", 7, LONG, 1)
succesfulSample2 = _statParam("succesfulSample2", 8, LONG, 1)
succesfulSample3 = _statParam("succesfulSample3", 9, LONG, 1)
failedSample1 = _statParam("failedSample1", 10, LONG, 1)
failedSample2 = _statParam("failedSample2", 11, LONG, 1)
failedSample3 = _statParam("failedSample3", 12, LONG, 1)
badUtcTime = _statParam("badUtcTime", 13, LONG, 1)
goodUtcTime = _statParam("goodUtcTime", 14, LONG, 1)
failGetUtc = _statParam("failGetUtc", 15, LONG, 1)
failedConnect = _statParam("failedConnect", 16, LONG, 1)
succeedConnect = _statParam("succeedConnect", 17, LONG, 1)
iflashWriteFail = _statParam("iflashWriteFail", 18, LONG, 1)
iflashEraseFail = _statParam("iflashEraseFail", 19, LONG, 1)
postHttpGood = _statParam("postHttpGood", 20, LONG, 1)
postHttpFail = _statParam("postHttpFail", 21, LONG, 1)
postHttpDisc = _statParam("postHttpDisc", 22, LONG, 1)
getHttpGood = _statParam("getHttpGood", 23, LONG, 1)
getHttpFail = _statParam("getHttpFail", 24, LONG, 1)
getHttpDisc = _statParam("getHttpDisc", 25, LONG, 1)
sequencerRetry = _statParam("sequencerRetry", 26, LONG, 1)
wifiModemConnect = _statParam("wifiModemConnect", 27, LONG, 1)
cellModemConnect = _statParam("cellModemConnect", 28, LONG, 1)
wifiResponseTimedout = _statParam("wifiResponseTimedout", 29, LONG, 1)
cellResponseTimedout = _statParam("cellResponseTimedout", 30, LONG, 1)
goodTempRhI2c = _statParam("goodTempRhI2c", 31, LONG, 1)
badTempRhI2c = _statParam("badTempRhI2c", 32, LONG, 1)
cellOverflows = _statParam("cellOverflows", 33, LONG, 1)
wifirxqOverflow = _statParam("wifirxqOverflow", 34, LONG, 1)
cellUartRxError = _statParam("cellUartRxError", 35, LONG, 1)
wifiUartRxError = _statParam("wifiUartRxError", 36, LONG, 1)
stackOverflow = _statParam("stackOverflow", 37, LONG, 1)
cellByteqMax = _statParam("cellByteqMax", 38, LONG, 1)
wifiByteqMax = _statParam("wifiByteqMax", 39, LONG, 1)
UnknownEscapes = _statParam("UnknownEscapes", 40, LONG, 1)
WifiErrors = _statParam("WifiErrors", 41, LONG, 1)
WifiDisconnects = _statParam("WifiDisconnects", 42, LONG, 1)
wifiTimeout = _statParam("wifiTimeout", 43, LONG, 1)
communicationDeath = _statParam("communicationDeath", 44, LONG, 1)
etrcWriteFail = _statParam("etrcWriteFail", 45, LONG, 1)
etrcReadFail = _statParam("etrcReadFail", 46, LONG, 1)
startUp = _statParam("startUp", 47, LONG, 1)
httpErrorStatus = _statParam("httpErrorStatus", 48, LONG, 1)
fileWriteSuccess = _statParam("fileWriteSuccess", 49, LONG, 1)
fileWriteFail = _statParam("fileWriteFail", 50, LONG, 1)
doubleActionError = _statParam("doubleActionError", 51, LONG, 1)
udmErase = _statParam("udmErase", 52, LONG, 1)
sensorRxqOverflow = _statParam("sensorRxqOverflow", 53, LONG, 1)
cloudDeath = _statParam("cloudDeath", 54, LONG, 1)
goodGetUtc = _statParam("goodGetUtc", 55, LONG, 1)

stats = [wdogResetCtr, 
	faultCtr, 
	resetByFault, 
	sdi12Errors, 
	unsuportedSensor, 
	runNewImage, 
	badImage, 
	succesfulSample1, 
	succesfulSample2, 
	succesfulSample3, 
	failedSample1, 
	failedSample2, 
	failedSample3, 
	badUtcTime, 
	goodUtcTime, 
	failGetUtc, 
	failedConnect, 
	succeedConnect, 
	iflashWriteFail, 
	iflashEraseFail, 
	postHttpGood, 
	postHttpFail, 
	postHttpDisc, 
	getHttpGood, 
	getHttpFail, 
	getHttpDisc, 
	sequencerRetry, 
	wifiModemConnect, 
	cellModemConnect, 
	wifiResponseTimedout, 
	cellResponseTimedout, 
	goodTempRhI2c, 
	badTempRhI2c, 
	cellOverflows, 
	wifirxqOverflow, 
	cellUartRxError, 
	wifiUartRxError, 
	stackOverflow, 
	cellByteqMax, 
	wifiByteqMax, 
	UnknownEscapes, 
	WifiErrors, 
	WifiDisconnects, 
	wifiTimeout, 
	communicationDeath, 
	etrcWriteFail, 
	etrcReadFail, 
	startUp, 
	httpErrorStatus, 
	fileWriteSuccess, 
	fileWriteFail, 
	doubleActionError, 
	udmErase, 
	sensorRxqOverflow, 
	cloudDeath, 
	goodGetUtc]

# Params
Ssid = _statParam("Ssid", 1, CHAR, 33)
Password = _statParam("Password", 2, CHAR, 65)
SerialNo = _statParam("SerialNo", 3, CHAR, 6)
DataServer = _statParam("DataServer", 4, CHAR, 64)
TimeServer = _statParam("TimeServer", 5, CHAR, 64)
DataPort = _statParam("DataPort", 6, CHAR, 6)
ConnectInterval = _statParam("ConnectInterval", 7, CELL, 1)
CalibrateInterval = _statParam("CalibrateInterval", 8, CELL, 1)
Services = _statParam("Services", 9, BYTE, 1)
WdogDisabled = _statParam("WdogDisabled", 10, BYTE, 1)
FileServer = _statParam("FileServer", 11, CHAR, 64)
FilePort = _statParam("FilePort", 12, CHAR, 6)
TimeSyncInterval = _statParam("TimeSyncInterval", 13, CELL, 1)
FileCheckInterval = _statParam("FileCheckInterval", 14, CELL, 1)
CellModem = _statParam("CellModem", 15, BOOL, 1)
CellWait = _statParam("CellWait", 16, CELL, 1)
TranslatedV1 = _statParam("TranslatedV1", 17, BOOL, 1)
Netid = _statParam("Netid", 18, CHAR, 32)
DeviceName = _statParam("DeviceName", 19, CHAR, 32)
StationName = _statParam("StationName", 20, CHAR, 32)
InitFileSystem = _statParam("InitFileSystem", 21, BOOL, 1)
McuSignature = _statParam("McuSignature", 22, CHAR, 11)
FileSystemVersion = _statParam("FileSystemVersion", 23, LONG, 1)
Uid = _statParam("Uid", 24, CHAR, 7)
Apn = _statParam("Apn", 25, CHAR, 64)
PdpId = _statParam("PdpId", 26, CHAR, 2)
TempRhInterval = _statParam("TempRhInterval", 27, CELL, 1)
HealthReportInterval = _statParam("HealthReportInterval", 28, CELL, 1)
ArchStatsInterval = _statParam("ArchStatsInterval", 29, CELL, 1)
PowerResolution = _statParam("PowerResolution", 30, CELL, 1)
AutoRemote = _statParam("AutoRemote", 31, BOOL, 1)
RemoteServer = _statParam("RemoteServer", 32, CHAR, 64)
RemotePort = _statParam("RemotePort", 33, CHAR, 6)
RemoteIdleTime = _statParam("RemoteIdleTime", 34, CELL, 1)
Gitrev = _statParam("Gitrev", 200, CHAR, 33)
Gitbranch = _statParam("Gitbranch", 201, CHAR, 33)
Gitstate = _statParam("Gitstate", 202, CHAR, 33)
Builddate = _statParam("Builddate", 203, CHAR, 33)
Buildtime = _statParam("Buildtime", 204, CHAR, 33)
IMEI = _statParam("IMEI", 205, CHAR, 16)
SimId = _statParam("SimId", 206, CHAR, 21)

params = [Ssid, 
	Password, 
	SerialNo, 
	DataServer, 
	TimeServer, 
	DataPort, 
	ConnectInterval, 
	CalibrateInterval, 
	Services, 
	WdogDisabled, 
	FileServer, 
	FilePort, 
	TimeSyncInterval, 
	FileCheckInterval, 
	CellModem, 
	CellWait, 
	TranslatedV1, 
	Netid, 
	DeviceName, 
	StationName, 
	InitFileSystem, 
	McuSignature, 
	FileSystemVersion, 
	Uid, 
	Apn, 
	PdpId, 
	TempRhInterval, 
	HealthReportInterval, 
	ArchStatsInterval, 
	PowerResolution, 
	AutoRemote, 
	RemoteServer, 
	RemotePort, 
	RemoteIdleTime, 
	Gitrev, 
	Gitbranch, 
	Gitstate, 
	Builddate, 
	Buildtime, 
	IMEI, 
	SimId]

ADC0_CH6 = _statParam("ADC0_CH6", 0, BYTE, 2)
ADC0_CH7 = _statParam("ADC0_CH7", 1, BYTE, 2)
ADC_SOL = _statParam("ADC_SOL", 2, BYTE, 2)
ADC_VIN_ON = _statParam("ADC_VIN_ON", 3, BYTE, 2)
ADC_VIN = _statParam("ADC_VIN", 4, BYTE, 2)
BU_VIN = _statParam("BU_VIN", 5, BYTE, 2)
C1_SDI12_NRX_TX = _statParam("C1_SDI12_NRX_TX", 6, BYTE, 2)
C2_SDI12_NRX_TX = _statParam("C2_SDI12_NRX_TX", 7, BYTE, 2)
C3_SDI12_NRX_TX = _statParam("C3_SDI12_NRX_TX", 8, BYTE, 2)
CELL_CTS = _statParam("CELL_CTS", 9, BYTE, 2)
CELL_DCD = _statParam("CELL_DCD", 10, BYTE, 2)
CELL_DSR = _statParam("CELL_DSR", 11, BYTE, 2)
CELL_DTR = _statParam("CELL_DTR", 12, BYTE, 2)
CELL_MODEM_RX = _statParam("CELL_MODEM_RX", 13, BYTE, 2)
CELL_MODEM_TX = _statParam("CELL_MODEM_TX", 14, BYTE, 2)
CELL_PWR_ON = _statParam("CELL_PWR_ON", 15, BYTE, 2)
CELL_RESET = _statParam("CELL_RESET", 16, BYTE, 2)
CELL_RTS = _statParam("CELL_RTS", 17, BYTE, 2)
COM1_SEL_SDI12 = _statParam("COM1_SEL_SDI12", 18, BYTE, 2)
COM2_SEL_SDI12 = _statParam("COM2_SEL_SDI12", 19, BYTE, 2)
CTRL_CELL_PWR = _statParam("CTRL_CELL_PWR", 20, BYTE, 2)
DAC0_OUT0 = _statParam("DAC0_OUT0", 21, BYTE, 2)
DAC0_OUT1 = _statParam("DAC0_OUT1", 22, BYTE, 2)
DC_DC_CNTL = _statParam("DC_DC_CNTL", 23, BYTE, 2)
FLASH_SPI_CS = _statParam("FLASH_SPI_CS", 24, BYTE, 2)
FLASH_SPI_WP = _statParam("FLASH_SPI_WP", 25, BYTE, 2)
FRAM_SPI_CLK = _statParam("FRAM_SPI_CLK", 26, BYTE, 2)
FRAM_SPI_CS = _statParam("FRAM_SPI_CS", 27, BYTE, 2)
FRAM_SPI_MISO = _statParam("FRAM_SPI_MISO", 28, BYTE, 2)
FRAM_SPI_MOSI = _statParam("FRAM_SPI_MOSI", 29, BYTE, 2)
FRAM_SPI_WP = _statParam("FRAM_SPI_WP", 30, BYTE, 2)
GPIO_SWO = _statParam("GPIO_SWO", 31, BYTE, 2)
GPIO_TCLK = _statParam("GPIO_TCLK", 32, BYTE, 2)
GPIO_TD0 = _statParam("GPIO_TD0", 33, BYTE, 2)
GPIO_TD1 = _statParam("GPIO_TD1", 34, BYTE, 2)
GPIO_TD2 = _statParam("GPIO_TD2", 35, BYTE, 2)
GPIO_TD3 = _statParam("GPIO_TD3", 36, BYTE, 2)
GS_ASYNC_IRQ = _statParam("GS_ASYNC_IRQ", 37, BYTE, 2)
GS_NEXT_RESET = _statParam("GS_NEXT_RESET", 38, BYTE, 2)
GS_RX = _statParam("GS_RX", 39, BYTE, 2)
GS_TX = _statParam("GS_TX", 40, BYTE, 2)
GS_WAKEUP_STANDBY = _statParam("GS_WAKEUP_STANDBY", 41, BYTE, 2)
I2C0_SCL = _statParam("I2C0_SCL", 42, BYTE, 2)
I2C0_SDA = _statParam("I2C0_SDA", 43, BYTE, 2)
LEUART0_RX = _statParam("LEUART0_RX", 44, BYTE, 2)
LEUART0_TX = _statParam("LEUART0_TX", 45, BYTE, 2)
LEUART1_RX = _statParam("LEUART1_RX", 46, BYTE, 2)
LEUART1_TX = _statParam("LEUART1_TX", 47, BYTE, 2)
LFXO_N = _statParam("LFXO_N", 48, BYTE, 2)
LFXO_P = _statParam("LFXO_P", 49, BYTE, 2)
NRTC_IRQ = _statParam("NRTC_IRQ", 50, BYTE, 2)
OC_OUT = _statParam("OC_OUT", 51, BYTE, 2)
PLUS5V_NOFF = _statParam("PLUS5V_NOFF", 52, BYTE, 2)
PROGRAM_RESTORE = _statParam("PROGRAM_RESTORE", 53, BYTE, 2)
PUSHBUTTON1 = _statParam("PUSHBUTTON1", 54, BYTE, 2)
PWR_COM1 = _statParam("PWR_COM1", 55, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 56, BYTE, 2)
PWR_COM3 = _statParam("PWR_COM3", 57, BYTE, 2)
PWR_DAC1 = _statParam("PWR_DAC1", 58, BYTE, 2)
PWR_DAC2 = _statParam("PWR_DAC2", 59, BYTE, 2)
SENS1 = _statParam("SENS1", 60, BYTE, 2)
SENS2 = _statParam("SENS2", 61, BYTE, 2)
SENS3 = _statParam("SENS3", 62, BYTE, 2)
TP5 = _statParam("TP5", 63, BYTE, 2)
TP6 = _statParam("TP6", 64, BYTE, 2)
TP7 = _statParam("TP7", 65, BYTE, 2)
UART0_RX = _statParam("UART0_RX", 66, BYTE, 2)
UART0_TX = _statParam("UART0_TX", 67, BYTE, 2)
UART1_RX = _statParam("UART1_RX", 68, BYTE, 2)
UART1_TX = _statParam("UART1_TX", 69, BYTE, 2)
UCEXC = _statParam("UCEXC", 70, BYTE, 2)
UC_DEBUG_RX = _statParam("UC_DEBUG_RX", 71, BYTE, 2)
UC_DEBUG_TX = _statParam("UC_DEBUG_TX", 72, BYTE, 2)
UC_EN_485N232_1 = _statParam("UC_EN_485N232_1", 73, BYTE, 2)
UC_EN_485N232_2 = _statParam("UC_EN_485N232_2", 74, BYTE, 2)
UC_EN_RX_485232_1 = _statParam("UC_EN_RX_485232_1", 75, BYTE, 2)
UC_EN_RX_485232_2 = _statParam("UC_EN_RX_485232_2", 76, BYTE, 2)
UC_EN_TX_485232_1 = _statParam("UC_EN_TX_485232_1", 77, BYTE, 2)
UC_EN_TX_485232_2 = _statParam("UC_EN_TX_485232_2", 78, BYTE, 2)
UC_LED1 = _statParam("UC_LED1", 79, BYTE, 2)
UC_LED2 = _statParam("UC_LED2", 80, BYTE, 2)
UC_LED3 = _statParam("UC_LED3", 81, BYTE, 2)
UC_RX_COM1 = _statParam("UC_RX_COM1", 82, BYTE, 2)
UC_RX_COM2 = _statParam("UC_RX_COM2", 83, BYTE, 2)
UC_RX_COM3 = _statParam("UC_RX_COM3", 84, BYTE, 2)
UC_TX_COM1 = _statParam("UC_TX_COM1", 85, BYTE, 2)
UC_TX_COM2 = _statParam("UC_TX_COM2", 86, BYTE, 2)
UC_TX_COM3 = _statParam("UC_TX_COM3", 87, BYTE, 2)
USART0_RX = _statParam("USART0_RX", 88, BYTE, 2)
USART0_TX = _statParam("USART0_TX", 89, BYTE, 2)
USART1_RX = _statParam("USART1_RX", 90, BYTE, 2)
USART1_TX = _statParam("USART1_TX", 91, BYTE, 2)
USART2_CLK = _statParam("USART2_CLK", 92, BYTE, 2)
USART2_RX = _statParam("USART2_RX", 93, BYTE, 2)
USART2_TX = _statParam("USART2_TX", 94, BYTE, 2)
USB_RTS = _statParam("USB_RTS", 95, BYTE, 2)
WIFI_PWR_CTRL = _statParam("WIFI_PWR_CTRL", 96, BYTE, 2)

pins = [ADC0_CH6, 
	ADC0_CH7, 
	ADC_SOL, 
	ADC_VIN_ON, 
	ADC_VIN, 
	BU_VIN, 
	C1_SDI12_NRX_TX, 
	C2_SDI12_NRX_TX, 
	C3_SDI12_NRX_TX, 
	CELL_CTS, 
	CELL_DCD, 
	CELL_DSR, 
	CELL_DTR, 
	CELL_MODEM_RX, 
	CELL_MODEM_TX, 
	CELL_PWR_ON, 
	CELL_RESET, 
	CELL_RTS, 
	COM1_SEL_SDI12, 
	COM2_SEL_SDI12, 
	CTRL_CELL_PWR, 
	DAC0_OUT0, 
	DAC0_OUT1, 
	DC_DC_CNTL, 
	FLASH_SPI_CS, 
	FLASH_SPI_WP, 
	FRAM_SPI_CLK, 
	FRAM_SPI_CS, 
	FRAM_SPI_MISO, 
	FRAM_SPI_MOSI, 
	FRAM_SPI_WP, 
	GPIO_SWO, 
	GPIO_TCLK, 
	GPIO_TD0, 
	GPIO_TD1, 
	GPIO_TD2, 
	GPIO_TD3, 
	GS_ASYNC_IRQ, 
	GS_NEXT_RESET, 
	GS_RX, 
	GS_TX, 
	GS_WAKEUP_STANDBY, 
	I2C0_SCL, 
	I2C0_SDA, 
	LEUART0_RX, 
	LEUART0_TX, 
	LEUART1_RX, 
	LEUART1_TX, 
	LFXO_N, 
	LFXO_P, 
	NRTC_IRQ, 
	OC_OUT, 
	PLUS5V_NOFF, 
	PROGRAM_RESTORE, 
	PUSHBUTTON1, 
	PWR_COM1, 
	PWR_COM2, 
	PWR_COM3, 
	PWR_DAC1, 
	PWR_DAC2, 
	SENS1, 
	SENS2, 
	SENS3, 
	TP5, 
	TP6, 
	TP7, 
	UART0_RX, 
	UART0_TX, 
	UART1_RX, 
	UART1_TX, 
	UCEXC, 
	UC_DEBUG_RX, 
	UC_DEBUG_TX, 
	UC_EN_485N232_1, 
	UC_EN_485N232_2, 
	UC_EN_RX_485232_1, 
	UC_EN_RX_485232_2, 
	UC_EN_TX_485232_1, 
	UC_EN_TX_485232_2, 
	UC_LED1, 
	UC_LED2, 
	UC_LED3, 
	UC_RX_COM1, 
	UC_RX_COM2, 
	UC_RX_COM3, 
	UC_TX_COM1, 
	UC_TX_COM2, 
	UC_TX_COM3, 
	USART0_RX, 
	USART0_TX, 
	USART1_RX, 
	USART1_TX, 
	USART2_CLK, 
	USART2_RX, 
	USART2_TX, 
	USB_RTS, 
	WIFI_PWR_CTRL]
