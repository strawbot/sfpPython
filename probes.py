# generated file on 2020-02-07 15:25:12.332507. Do not edit!

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
readingOverlap = _statParam("readingOverlap", 56, LONG, 1)
outOfAggregators = _statParam("outOfAggregators", 57, LONG, 1)
badDataTimestampWrite = _statParam("badDataTimestampWrite", 58, LONG, 1)
badDatafileSize = _statParam("badDatafileSize", 59, LONG, 1)
outOfRangeTimestamp = _statParam("outOfRangeTimestamp", 60, LONG, 1)
badClientListener = _statParam("badClientListener", 61, LONG, 1)
overDueTea = _statParam("overDueTea", 62, LONG, 1)

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
	goodGetUtc, 
	readingOverlap, 
	outOfAggregators, 
	badDataTimestampWrite, 
	badDatafileSize, 
	outOfRangeTimestamp, 
	badClientListener, 
	overDueTea]

# Params
Gitrev = _statParam("Gitrev", 200, CHAR, 33)
Gitbranch = _statParam("Gitbranch", 201, CHAR, 33)
Gitstate = _statParam("Gitstate", 202, CHAR, 33)
Builddate = _statParam("Builddate", 203, CHAR, 33)
Buildtime = _statParam("Buildtime", 204, CHAR, 33)
IMEI = _statParam("IMEI", 205, CHAR, 16)
SimId = _statParam("SimId", 206, CHAR, 21)

params = [Gitrev, 
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
C2_SDI12_NRX_TX = _statParam("C2_SDI12_NRX_TX", 8, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 9, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 10, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 11, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 12, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 13, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 14, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 15, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 16, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 17, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 18, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 19, BYTE, 2)
CTRL_IRD_PWR = _statParam("CTRL_IRD_PWR", 20, BYTE, 2)
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
ADC0_CH6 = _statParam("ADC0_CH6", 32, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 33, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 34, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 35, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 36, BYTE, 2)
GS_ASYNC_IRQ = _statParam("GS_ASYNC_IRQ", 37, BYTE, 2)
GS_NEXT_RESET = _statParam("GS_NEXT_RESET", 38, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 39, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 40, BYTE, 2)
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
ADC0_CH6 = _statParam("ADC0_CH6", 51, BYTE, 2)
PLUS5V_NOFF = _statParam("PLUS5V_NOFF", 52, BYTE, 2)
PROGRAM_RESTORE = _statParam("PROGRAM_RESTORE", 53, BYTE, 2)
PUSHBUTTON1 = _statParam("PUSHBUTTON1", 54, BYTE, 2)
PWR_COM1 = _statParam("PWR_COM1", 55, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 56, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 57, BYTE, 2)
PWR_DAC1 = _statParam("PWR_DAC1", 58, BYTE, 2)
PWR_DAC2 = _statParam("PWR_DAC2", 59, BYTE, 2)
SENS1 = _statParam("SENS1", 60, BYTE, 2)
SENS2 = _statParam("SENS2", 61, BYTE, 2)
SENS2 = _statParam("SENS2", 62, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 63, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 64, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 65, BYTE, 2)
UART0_RX = _statParam("UART0_RX", 66, BYTE, 2)
UART0_TX = _statParam("UART0_TX", 67, BYTE, 2)
UART1_RX = _statParam("UART1_RX", 68, BYTE, 2)
UART1_TX = _statParam("UART1_TX", 69, BYTE, 2)
UCEXC = _statParam("UCEXC", 70, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 71, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 72, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 73, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 74, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 75, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 76, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 77, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 78, BYTE, 2)
UC_LED1 = _statParam("UC_LED1", 79, BYTE, 2)
UC_LED2 = _statParam("UC_LED2", 80, BYTE, 2)
UC_LED3 = _statParam("UC_LED3", 81, BYTE, 2)
UC_RX_COM1 = _statParam("UC_RX_COM1", 82, BYTE, 2)
UC_RX_COM2 = _statParam("UC_RX_COM2", 83, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 84, BYTE, 2)
UC_TX_COM1 = _statParam("UC_TX_COM1", 85, BYTE, 2)
UC_TX_COM2 = _statParam("UC_TX_COM2", 86, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 87, BYTE, 2)
USART0_RX = _statParam("USART0_RX", 88, BYTE, 2)
USART0_TX = _statParam("USART0_TX", 89, BYTE, 2)
USART1_RX = _statParam("USART1_RX", 90, BYTE, 2)
USART1_TX = _statParam("USART1_TX", 91, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 92, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 93, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 94, BYTE, 2)
USB_RTS = _statParam("USB_RTS", 95, BYTE, 2)
WIFI_PWR_CTRL = _statParam("WIFI_PWR_CTRL", 96, BYTE, 2)
ADC0_CH6 = _statParam("ADC0_CH6", 97, BYTE, 2)
ADC0_CH7 = _statParam("ADC0_CH7", 98, BYTE, 2)
ADC_SOL = _statParam("ADC_SOL", 99, BYTE, 2)
ADC_VIN_ON = _statParam("ADC_VIN_ON", 100, BYTE, 2)
ADC_VIN = _statParam("ADC_VIN", 101, BYTE, 2)
BU_VIN = _statParam("BU_VIN", 102, BYTE, 2)
C1_SDI12_NRX_TX = _statParam("C1_SDI12_NRX_TX", 103, BYTE, 2)
C2_SDI12_NRX_TX = _statParam("C2_SDI12_NRX_TX", 104, BYTE, 2)
C3_SDI12_NRX_TX = _statParam("C3_SDI12_NRX_TX", 105, BYTE, 2)
CELL_CTS = _statParam("CELL_CTS", 106, BYTE, 2)
CELL_DCD = _statParam("CELL_DCD", 107, BYTE, 2)
CELL_DSR = _statParam("CELL_DSR", 108, BYTE, 2)
CELL_DTR = _statParam("CELL_DTR", 109, BYTE, 2)
CELL_MODEM_RX = _statParam("CELL_MODEM_RX", 110, BYTE, 2)
CELL_MODEM_TX = _statParam("CELL_MODEM_TX", 111, BYTE, 2)
CELL_PWR_ON = _statParam("CELL_PWR_ON", 112, BYTE, 2)
CELL_RESET = _statParam("CELL_RESET", 113, BYTE, 2)
CELL_RTS = _statParam("CELL_RTS", 114, BYTE, 2)
COM1_SEL_SDI12 = _statParam("COM1_SEL_SDI12", 115, BYTE, 2)
COM2_SEL_SDI12 = _statParam("COM2_SEL_SDI12", 116, BYTE, 2)
CTRL_CELL_PWR = _statParam("CTRL_CELL_PWR", 117, BYTE, 2)
DAC0_OUT0 = _statParam("DAC0_OUT0", 118, BYTE, 2)
DAC0_OUT1 = _statParam("DAC0_OUT1", 119, BYTE, 2)
DC_DC_CNTL = _statParam("DC_DC_CNTL", 120, BYTE, 2)
FLASH_SPI_CS = _statParam("FLASH_SPI_CS", 121, BYTE, 2)
FLASH_SPI_WP = _statParam("FLASH_SPI_WP", 122, BYTE, 2)
FRAM_SPI_CLK = _statParam("FRAM_SPI_CLK", 123, BYTE, 2)
FRAM_SPI_CS = _statParam("FRAM_SPI_CS", 124, BYTE, 2)
FRAM_SPI_MISO = _statParam("FRAM_SPI_MISO", 125, BYTE, 2)
FRAM_SPI_MOSI = _statParam("FRAM_SPI_MOSI", 126, BYTE, 2)
FRAM_SPI_WP = _statParam("FRAM_SPI_WP", 127, BYTE, 2)
GPIO_SWO = _statParam("GPIO_SWO", 128, BYTE, 2)
GPIO_TCLK = _statParam("GPIO_TCLK", 129, BYTE, 2)
GPIO_TD0 = _statParam("GPIO_TD0", 130, BYTE, 2)
GPIO_TD1 = _statParam("GPIO_TD1", 131, BYTE, 2)
GPIO_TD2 = _statParam("GPIO_TD2", 132, BYTE, 2)
GPIO_TD3 = _statParam("GPIO_TD3", 133, BYTE, 2)
GS_ASYNC_IRQ = _statParam("GS_ASYNC_IRQ", 134, BYTE, 2)
GS_NEXT_RESET = _statParam("GS_NEXT_RESET", 135, BYTE, 2)
GS_RX = _statParam("GS_RX", 136, BYTE, 2)
GS_TX = _statParam("GS_TX", 137, BYTE, 2)
GS_WAKEUP_STANDBY = _statParam("GS_WAKEUP_STANDBY", 138, BYTE, 2)
I2C0_SCL = _statParam("I2C0_SCL", 139, BYTE, 2)
I2C0_SDA = _statParam("I2C0_SDA", 140, BYTE, 2)
LEUART0_RX = _statParam("LEUART0_RX", 141, BYTE, 2)
LEUART0_TX = _statParam("LEUART0_TX", 142, BYTE, 2)
LEUART1_RX = _statParam("LEUART1_RX", 143, BYTE, 2)
LEUART1_TX = _statParam("LEUART1_TX", 144, BYTE, 2)
LFXO_N = _statParam("LFXO_N", 145, BYTE, 2)
LFXO_P = _statParam("LFXO_P", 146, BYTE, 2)
NRTC_IRQ = _statParam("NRTC_IRQ", 147, BYTE, 2)
OC_OUT = _statParam("OC_OUT", 148, BYTE, 2)
PLUS5V_NOFF = _statParam("PLUS5V_NOFF", 149, BYTE, 2)
PROGRAM_RESTORE = _statParam("PROGRAM_RESTORE", 150, BYTE, 2)
PUSHBUTTON1 = _statParam("PUSHBUTTON1", 151, BYTE, 2)
PWR_COM1 = _statParam("PWR_COM1", 152, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 153, BYTE, 2)
PWR_COM3 = _statParam("PWR_COM3", 154, BYTE, 2)
PWR_DAC1 = _statParam("PWR_DAC1", 155, BYTE, 2)
PWR_DAC2 = _statParam("PWR_DAC2", 156, BYTE, 2)
SENS1 = _statParam("SENS1", 157, BYTE, 2)
SENS2 = _statParam("SENS2", 158, BYTE, 2)
SENS3 = _statParam("SENS3", 159, BYTE, 2)
TP5 = _statParam("TP5", 160, BYTE, 2)
TP6 = _statParam("TP6", 161, BYTE, 2)
TP7 = _statParam("TP7", 162, BYTE, 2)
UART0_RX = _statParam("UART0_RX", 163, BYTE, 2)
UART0_TX = _statParam("UART0_TX", 164, BYTE, 2)
UART1_RX = _statParam("UART1_RX", 165, BYTE, 2)
UART1_TX = _statParam("UART1_TX", 166, BYTE, 2)
UCEXC = _statParam("UCEXC", 167, BYTE, 2)
UC_DEBUG_RX = _statParam("UC_DEBUG_RX", 168, BYTE, 2)
UC_DEBUG_TX = _statParam("UC_DEBUG_TX", 169, BYTE, 2)
UC_EN_485N232_1 = _statParam("UC_EN_485N232_1", 170, BYTE, 2)
UC_EN_485N232_2 = _statParam("UC_EN_485N232_2", 171, BYTE, 2)
UC_EN_RX_485232_1 = _statParam("UC_EN_RX_485232_1", 172, BYTE, 2)
UC_EN_RX_485232_2 = _statParam("UC_EN_RX_485232_2", 173, BYTE, 2)
UC_EN_TX_485232_1 = _statParam("UC_EN_TX_485232_1", 174, BYTE, 2)
UC_EN_TX_485232_2 = _statParam("UC_EN_TX_485232_2", 175, BYTE, 2)
UC_LED1 = _statParam("UC_LED1", 176, BYTE, 2)
UC_LED2 = _statParam("UC_LED2", 177, BYTE, 2)
UC_LED3 = _statParam("UC_LED3", 178, BYTE, 2)
UC_RX_COM1 = _statParam("UC_RX_COM1", 179, BYTE, 2)
UC_RX_COM2 = _statParam("UC_RX_COM2", 180, BYTE, 2)
UC_RX_COM3 = _statParam("UC_RX_COM3", 181, BYTE, 2)
UC_TX_COM1 = _statParam("UC_TX_COM1", 182, BYTE, 2)
UC_TX_COM2 = _statParam("UC_TX_COM2", 183, BYTE, 2)
UC_TX_COM3 = _statParam("UC_TX_COM3", 184, BYTE, 2)
USART0_RX = _statParam("USART0_RX", 185, BYTE, 2)
USART0_TX = _statParam("USART0_TX", 186, BYTE, 2)
USART1_RX = _statParam("USART1_RX", 187, BYTE, 2)
USART1_TX = _statParam("USART1_TX", 188, BYTE, 2)
USART2_CLK = _statParam("USART2_CLK", 189, BYTE, 2)
USART2_RX = _statParam("USART2_RX", 190, BYTE, 2)
USART2_TX = _statParam("USART2_TX", 191, BYTE, 2)
USB_RTS = _statParam("USB_RTS", 192, BYTE, 2)
WIFI_PWR_CTRL = _statParam("WIFI_PWR_CTRL", 193, BYTE, 2)
ADC_SOL = _statParam("ADC_SOL", 194, BYTE, 2)
ADC_VIN_ON = _statParam("ADC_VIN_ON", 195, BYTE, 2)
ADC_VIN = _statParam("ADC_VIN", 196, BYTE, 2)
BU_VIN = _statParam("BU_VIN", 197, BYTE, 2)
C1_SDI12_NRX_TX = _statParam("C1_SDI12_NRX_TX", 198, BYTE, 2)
C2_SDI12_NRX_TX = _statParam("C2_SDI12_NRX_TX", 199, BYTE, 2)
COM1_SDI12_3V = _statParam("COM1_SDI12_3V", 200, BYTE, 2)
COM1_SEL_A0 = _statParam("COM1_SEL_A0", 201, BYTE, 2)
COM1_SEL_A1 = _statParam("COM1_SEL_A1", 202, BYTE, 2)
COM1_SEL_B0 = _statParam("COM1_SEL_B0", 203, BYTE, 2)
COM1_SEL_B1 = _statParam("COM1_SEL_B1", 204, BYTE, 2)
COM2_SDI12_3V = _statParam("COM2_SDI12_3V", 205, BYTE, 2)
COM2_SEL_A0 = _statParam("COM2_SEL_A0", 206, BYTE, 2)
COM2_SEL_A1 = _statParam("COM2_SEL_A1", 207, BYTE, 2)
COM2_SEL_B0 = _statParam("COM2_SEL_B0", 208, BYTE, 2)
COM2_SEL_B1 = _statParam("COM2_SEL_B1", 209, BYTE, 2)
CONFIG0 = _statParam("CONFIG0", 210, BYTE, 2)
CONFIG1 = _statParam("CONFIG1", 211, BYTE, 2)
CTRL_IRD_PWR = _statParam("CTRL_IRD_PWR", 212, BYTE, 2)
DC_DC_CNTL = _statParam("DC_DC_CNTL", 213, BYTE, 2)
EN_SW_COM1 = _statParam("EN_SW_COM1", 214, BYTE, 2)
EN_SW_COM2 = _statParam("EN_SW_COM2", 215, BYTE, 2)
FLASH_SPI_CS = _statParam("FLASH_SPI_CS", 216, BYTE, 2)
FLASH_SPI_WP = _statParam("FLASH_SPI_WP", 217, BYTE, 2)
FRAM_SPI_CLK = _statParam("FRAM_SPI_CLK", 218, BYTE, 2)
FRAM_SPI_CS = _statParam("FRAM_SPI_CS", 219, BYTE, 2)
FRAM_SPI_MISO = _statParam("FRAM_SPI_MISO", 220, BYTE, 2)
FRAM_SPI_MOSI = _statParam("FRAM_SPI_MOSI", 221, BYTE, 2)
FRAM_SPI_WP = _statParam("FRAM_SPI_WP", 222, BYTE, 2)
FRC_ON1 = _statParam("FRC_ON1", 223, BYTE, 2)
FRC_ON2 = _statParam("FRC_ON2", 224, BYTE, 2)
GPIO_SWO = _statParam("GPIO_SWO", 225, BYTE, 2)
GS_ASYNC_IRQ = _statParam("GS_ASYNC_IRQ", 226, BYTE, 2)
GS_NEXT_RESET = _statParam("GS_NEXT_RESET", 227, BYTE, 2)
GS_SDIO_DAT1_INT = _statParam("GS_SDIO_DAT1_INT", 228, BYTE, 2)
GS_SPI_CLK = _statParam("GS_SPI_CLK", 229, BYTE, 2)
GS_SPI_CS = _statParam("GS_SPI_CS", 230, BYTE, 2)
GS_SPI_MISO = _statParam("GS_SPI_MISO", 231, BYTE, 2)
GS_SPI_MOSI = _statParam("GS_SPI_MOSI", 232, BYTE, 2)
GS_WAKEUP_STANDBY = _statParam("GS_WAKEUP_STANDBY", 233, BYTE, 2)
I2C0_SCL = _statParam("I2C0_SCL", 234, BYTE, 2)
I2C0_SDA = _statParam("I2C0_SDA", 235, BYTE, 2)
IRD_TTL_RX = _statParam("IRD_TTL_RX", 236, BYTE, 2)
IRD_TTL_TX = _statParam("IRD_TTL_TX", 237, BYTE, 2)
LEUART0_RX = _statParam("LEUART0_RX", 238, BYTE, 2)
LEUART1_RX = _statParam("LEUART1_RX", 239, BYTE, 2)
LFXO_N = _statParam("LFXO_N", 240, BYTE, 2)
LFXO_P = _statParam("LFXO_P", 241, BYTE, 2)
NETWORK_AVAIL = _statParam("NETWORK_AVAIL", 242, BYTE, 2)
NFRC_OFF1 = _statParam("NFRC_OFF1", 243, BYTE, 2)
NFRC_OFF2 = _statParam("NFRC_OFF2", 244, BYTE, 2)
NRTC_IRQ = _statParam("NRTC_IRQ", 245, BYTE, 2)
PLUS5V_NOFF = _statParam("PLUS5V_NOFF", 246, BYTE, 2)
PROGRAM_RESTORE = _statParam("PROGRAM_RESTORE", 247, BYTE, 2)
PUSHBUTTON1 = _statParam("PUSHBUTTON1", 248, BYTE, 2)
PUSHBUTTON2 = _statParam("PUSHBUTTON2", 249, BYTE, 2)
PWR_COM1 = _statParam("PWR_COM1", 250, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 251, BYTE, 2)
PWR_DAC1 = _statParam("PWR_DAC1", 252, BYTE, 2)
PWR_DAC2 = _statParam("PWR_DAC2", 253, BYTE, 2)
SENS1 = _statParam("SENS1", 254, BYTE, 2)
SENS2 = _statParam("SENS2", 255, BYTE, 2)
UCEXC = _statParam("UCEXC", 256, BYTE, 2)
UC_LED1 = _statParam("UC_LED1", 257, BYTE, 2)
UC_LED2 = _statParam("UC_LED2", 258, BYTE, 2)
UC_LED3 = _statParam("UC_LED3", 259, BYTE, 2)
UC_NEN_RX_485_1 = _statParam("UC_NEN_RX_485_1", 260, BYTE, 2)
UC_NEN_RX_485_2 = _statParam("UC_NEN_RX_485_2", 261, BYTE, 2)
UC_NEN_RX_COM1 = _statParam("UC_NEN_RX_COM1", 262, BYTE, 2)
UC_NEN_RX_COM2 = _statParam("UC_NEN_RX_COM2", 263, BYTE, 2)
UC_NEN_TX_485_1 = _statParam("UC_NEN_TX_485_1", 264, BYTE, 2)
UC_NEN_TX_485_2 = _statParam("UC_NEN_TX_485_2", 265, BYTE, 2)
UC_RX_COM1 = _statParam("UC_RX_COM1", 266, BYTE, 2)
UC_RX_COM2 = _statParam("UC_RX_COM2", 267, BYTE, 2)
UC_TX_COM1 = _statParam("UC_TX_COM1", 268, BYTE, 2)
UC_TX_COM2 = _statParam("UC_TX_COM2", 269, BYTE, 2)
USB_RTS = _statParam("USB_RTS", 270, BYTE, 2)
WIFI_PWR_CTRL = _statParam("WIFI_PWR_CTRL", 271, BYTE, 2)
ADC_SOL = _statParam("ADC_SOL", 272, BYTE, 2)
ADC_VIN_ON = _statParam("ADC_VIN_ON", 273, BYTE, 2)
ADC_VIN = _statParam("ADC_VIN", 274, BYTE, 2)
BU_VIN = _statParam("BU_VIN", 275, BYTE, 2)
C1_SDI12_NRX_TX = _statParam("C1_SDI12_NRX_TX", 276, BYTE, 2)
C2_SDI12_NRX_TX = _statParam("C2_SDI12_NRX_TX", 277, BYTE, 2)
C3_SDI12_NRX_TX = _statParam("C3_SDI12_NRX_TX", 278, BYTE, 2)
CELL_CTS = _statParam("CELL_CTS", 279, BYTE, 2)
CELL_DCD = _statParam("CELL_DCD", 280, BYTE, 2)
CELL_DSR = _statParam("CELL_DSR", 281, BYTE, 2)
CELL_DTR = _statParam("CELL_DTR", 282, BYTE, 2)
CELL_MODEM_RX = _statParam("CELL_MODEM_RX", 283, BYTE, 2)
CELL_MODEM_TX = _statParam("CELL_MODEM_TX", 284, BYTE, 2)
CELL_PWR_ON = _statParam("CELL_PWR_ON", 285, BYTE, 2)
CELL_RESET = _statParam("CELL_RESET", 286, BYTE, 2)
CELL_RTS = _statParam("CELL_RTS", 287, BYTE, 2)
COM1_SEL_SDI12 = _statParam("COM1_SEL_SDI12", 288, BYTE, 2)
COM2_SEL_SDI12 = _statParam("COM2_SEL_SDI12", 289, BYTE, 2)
CTRL_CELL_PWR = _statParam("CTRL_CELL_PWR", 290, BYTE, 2)
DC_DC_CNTL = _statParam("DC_DC_CNTL", 291, BYTE, 2)
FLASH_SPI_CS = _statParam("FLASH_SPI_CS", 292, BYTE, 2)
FLASH_SPI_WP = _statParam("FLASH_SPI_WP", 293, BYTE, 2)
FRAM_SPI_CLK = _statParam("FRAM_SPI_CLK", 294, BYTE, 2)
FRAM_SPI_CS = _statParam("FRAM_SPI_CS", 295, BYTE, 2)
FRAM_SPI_MISO = _statParam("FRAM_SPI_MISO", 296, BYTE, 2)
FRAM_SPI_MOSI = _statParam("FRAM_SPI_MOSI", 297, BYTE, 2)
FRAM_SPI_WP = _statParam("FRAM_SPI_WP", 298, BYTE, 2)
GPIO_SWO = _statParam("GPIO_SWO", 299, BYTE, 2)
GPIO_TCLK = _statParam("GPIO_TCLK", 300, BYTE, 2)
GPIO_TD0 = _statParam("GPIO_TD0", 301, BYTE, 2)
GPIO_TD1 = _statParam("GPIO_TD1", 302, BYTE, 2)
GPIO_TD2 = _statParam("GPIO_TD2", 303, BYTE, 2)
GPIO_TD3 = _statParam("GPIO_TD3", 304, BYTE, 2)
GS_ASYNC_IRQ = _statParam("GS_ASYNC_IRQ", 305, BYTE, 2)
GS_NEXT_RESET = _statParam("GS_NEXT_RESET", 306, BYTE, 2)
GS_RX = _statParam("GS_RX", 307, BYTE, 2)
GS_TX = _statParam("GS_TX", 308, BYTE, 2)
GS_WAKEUP_STANDBY = _statParam("GS_WAKEUP_STANDBY", 309, BYTE, 2)
I2C0_SCL = _statParam("I2C0_SCL", 310, BYTE, 2)
I2C0_SDA = _statParam("I2C0_SDA", 311, BYTE, 2)
LFXO_N = _statParam("LFXO_N", 312, BYTE, 2)
LFXO_P = _statParam("LFXO_P", 313, BYTE, 2)
NRTC_IRQ = _statParam("NRTC_IRQ", 314, BYTE, 2)
OC_OUT = _statParam("OC_OUT", 315, BYTE, 2)
PLUS5V_NOFF = _statParam("PLUS5V_NOFF", 316, BYTE, 2)
PROGRAM_RESTORE = _statParam("PROGRAM_RESTORE", 317, BYTE, 2)
PUSHBUTTON1 = _statParam("PUSHBUTTON1", 318, BYTE, 2)
PWR_COM1 = _statParam("PWR_COM1", 319, BYTE, 2)
PWR_COM2 = _statParam("PWR_COM2", 320, BYTE, 2)
PWR_COM3 = _statParam("PWR_COM3", 321, BYTE, 2)
PWR_DAC1 = _statParam("PWR_DAC1", 322, BYTE, 2)
PWR_DAC2 = _statParam("PWR_DAC2", 323, BYTE, 2)
SENS1 = _statParam("SENS1", 324, BYTE, 2)
SENS2 = _statParam("SENS2", 325, BYTE, 2)
SENS3 = _statParam("SENS3", 326, BYTE, 2)
TP5 = _statParam("TP5", 327, BYTE, 2)
TP6 = _statParam("TP6", 328, BYTE, 2)
TP7 = _statParam("TP7", 329, BYTE, 2)
UCEXC = _statParam("UCEXC", 330, BYTE, 2)
UC_DEBUG_RX = _statParam("UC_DEBUG_RX", 331, BYTE, 2)
UC_DEBUG_TX = _statParam("UC_DEBUG_TX", 332, BYTE, 2)
UC_EN_485N232_1 = _statParam("UC_EN_485N232_1", 333, BYTE, 2)
UC_EN_485N232_2 = _statParam("UC_EN_485N232_2", 334, BYTE, 2)
UC_EN_RX_485232_1 = _statParam("UC_EN_RX_485232_1", 335, BYTE, 2)
UC_EN_RX_485232_2 = _statParam("UC_EN_RX_485232_2", 336, BYTE, 2)
UC_EN_TX_485232_1 = _statParam("UC_EN_TX_485232_1", 337, BYTE, 2)
UC_EN_TX_485232_2 = _statParam("UC_EN_TX_485232_2", 338, BYTE, 2)
UC_LED1 = _statParam("UC_LED1", 339, BYTE, 2)
UC_LED2 = _statParam("UC_LED2", 340, BYTE, 2)
UC_LED3 = _statParam("UC_LED3", 341, BYTE, 2)
UC_RX_COM1 = _statParam("UC_RX_COM1", 342, BYTE, 2)
UC_RX_COM2 = _statParam("UC_RX_COM2", 343, BYTE, 2)
UC_RX_COM3 = _statParam("UC_RX_COM3", 344, BYTE, 2)
UC_TX_COM1 = _statParam("UC_TX_COM1", 345, BYTE, 2)
UC_TX_COM2 = _statParam("UC_TX_COM2", 346, BYTE, 2)
UC_TX_COM3 = _statParam("UC_TX_COM3", 347, BYTE, 2)
USB_RTS = _statParam("USB_RTS", 348, BYTE, 2)
WIFI_PWR_CTRL = _statParam("WIFI_PWR_CTRL", 349, BYTE, 2)

pins = [ADC0_CH6, 
	ADC0_CH7, 
	ADC_SOL, 
	ADC_VIN_ON, 
	ADC_VIN, 
	BU_VIN, 
	C1_SDI12_NRX_TX, 
	C2_SDI12_NRX_TX, 
	C2_SDI12_NRX_TX, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	CTRL_IRD_PWR, 
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
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	GS_ASYNC_IRQ, 
	GS_NEXT_RESET, 
	ADC0_CH6, 
	ADC0_CH6, 
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
	ADC0_CH6, 
	PLUS5V_NOFF, 
	PROGRAM_RESTORE, 
	PUSHBUTTON1, 
	PWR_COM1, 
	PWR_COM2, 
	PWR_COM2, 
	PWR_DAC1, 
	PWR_DAC2, 
	SENS1, 
	SENS2, 
	SENS2, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	UART0_RX, 
	UART0_TX, 
	UART1_RX, 
	UART1_TX, 
	UCEXC, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	UC_LED1, 
	UC_LED2, 
	UC_LED3, 
	UC_RX_COM1, 
	UC_RX_COM2, 
	ADC0_CH6, 
	UC_TX_COM1, 
	UC_TX_COM2, 
	ADC0_CH6, 
	USART0_RX, 
	USART0_TX, 
	USART1_RX, 
	USART1_TX, 
	ADC0_CH6, 
	ADC0_CH6, 
	ADC0_CH6, 
	USB_RTS, 
	WIFI_PWR_CTRL, 
	ADC0_CH6, 
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
	WIFI_PWR_CTRL, 
	ADC_SOL, 
	ADC_VIN_ON, 
	ADC_VIN, 
	BU_VIN, 
	C1_SDI12_NRX_TX, 
	C2_SDI12_NRX_TX, 
	COM1_SDI12_3V, 
	COM1_SEL_A0, 
	COM1_SEL_A1, 
	COM1_SEL_B0, 
	COM1_SEL_B1, 
	COM2_SDI12_3V, 
	COM2_SEL_A0, 
	COM2_SEL_A1, 
	COM2_SEL_B0, 
	COM2_SEL_B1, 
	CONFIG0, 
	CONFIG1, 
	CTRL_IRD_PWR, 
	DC_DC_CNTL, 
	EN_SW_COM1, 
	EN_SW_COM2, 
	FLASH_SPI_CS, 
	FLASH_SPI_WP, 
	FRAM_SPI_CLK, 
	FRAM_SPI_CS, 
	FRAM_SPI_MISO, 
	FRAM_SPI_MOSI, 
	FRAM_SPI_WP, 
	FRC_ON1, 
	FRC_ON2, 
	GPIO_SWO, 
	GS_ASYNC_IRQ, 
	GS_NEXT_RESET, 
	GS_SDIO_DAT1_INT, 
	GS_SPI_CLK, 
	GS_SPI_CS, 
	GS_SPI_MISO, 
	GS_SPI_MOSI, 
	GS_WAKEUP_STANDBY, 
	I2C0_SCL, 
	I2C0_SDA, 
	IRD_TTL_RX, 
	IRD_TTL_TX, 
	LEUART0_RX, 
	LEUART1_RX, 
	LFXO_N, 
	LFXO_P, 
	NETWORK_AVAIL, 
	NFRC_OFF1, 
	NFRC_OFF2, 
	NRTC_IRQ, 
	PLUS5V_NOFF, 
	PROGRAM_RESTORE, 
	PUSHBUTTON1, 
	PUSHBUTTON2, 
	PWR_COM1, 
	PWR_COM2, 
	PWR_DAC1, 
	PWR_DAC2, 
	SENS1, 
	SENS2, 
	UCEXC, 
	UC_LED1, 
	UC_LED2, 
	UC_LED3, 
	UC_NEN_RX_485_1, 
	UC_NEN_RX_485_2, 
	UC_NEN_RX_COM1, 
	UC_NEN_RX_COM2, 
	UC_NEN_TX_485_1, 
	UC_NEN_TX_485_2, 
	UC_RX_COM1, 
	UC_RX_COM2, 
	UC_TX_COM1, 
	UC_TX_COM2, 
	USB_RTS, 
	WIFI_PWR_CTRL, 
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
	USB_RTS, 
	WIFI_PWR_CTRL]
