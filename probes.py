# structure for containing pin information to be sent in packet; each pin is 2 bytes
# typedef struct {
#     Byte port : 4; // A-I
#     Byte pin  : 4; // 0-15
#     Byte mode : 4; // one of 16 modes
#     Byte din  : 1; // for now 0 and 1
# } portpin;

import pids
import time

# SPIDs
GET_STATE, \
GET_RESULT, \
GET_STATS, \
GET_PARAMS, \
READ_SHORT_FILE, \
WRITE_SHORT_FILE = range(0,6)

SDI12_SENSOR_1_SPID, \
SDI12_SENSOR_2_SPID, \
SDI12_SENSOR_3_SPID, \
MCU_PIN = range(11, 11+4)

timestamp = 'timestamp'
pins = {}

class setPin():
    def __init__(self, port, pin, mode, value):
        self.port = port
        self.pin = pin
        self.mode = mode
        self.value = value

def printPins():
    for i in range(len(pinNames)):
        name = pinNames[i]
        port = pins[name].port
        pin = pins[name].pin
        mode = pins[name].mode
        value = pins[name].value

        print("{:<18} [P{}{:<3} {:>2} ({})".\
          format(name, port, str(pin)+']', value, modes[mode]))

def probeHandler(packet):
    spid = packet[2]
    probePins = packet[3:]
    if spid == MCU_PIN:
        pins[timestamp] = time.time()
        for i in range(len(pinNames)):
            name = pinNames[i]
            portpin = probePins[2*i]
            modeval = probePins[2*i+1]
            port, pin = portpin & 0xF, portpin >> 4
            mode, value = modeval & 0xF, modeval >> 4
            pins[name] = setPin("ABCDEFGHI"[port], pin, mode, value)

'''API for pins:
    initialize(sfpPort) will install the handler and setup initial pins 
    refresh() will get the latest pin information
    pins['pinname'] will return a structure for the pin which can be accessed:
        .value for the pin value
        .mode for the mode of the pin (one of 16 values: convert with modeName(n))
        .port for what port the pin is on (A-I)
        .pin for the pin number of the port (0-15)
    pins['timestamp'] will return the utc time of the last update or 0 if never
'''
sfp = None

def initialize(sfplink):
    global sfp
    pins[timestamp] = 0
    sfplink.setHandler(pids.PROBE, probeHandler)
    sfp = sfplink
    refresh()

def refresh():
    sfp.sendText("probepins")

modes = [
    'Input',
    'InputPull',
    'InputPullFilter',
    'PushPull',
    'PushPullDrive',
    'PushPullAlternate',
    'WiredOr',
    'WiredOrPullDown',
    'WiredAnd',
    'WiredAndFilter',
    'WiredAndPullUp',
    'WiredAndPullUpFilter',
    'WiredAndDrive',
    'WiredAndDriveFilter',
    'WiredAndDrivePullUp',
    'WiredAndDrivePullUpFilter']

pinNames = [
	'ADC0_CH6',
	'ADC0_CH7',
	'ADC_SOL',
	'ADC_VIN_ON',
	'ADC_VIN',
	'BU_VIN',
	'C1_SDI12_NRX_TX',
	'C2_SDI12_NRX_TX',
	'C3_SDI12_NRX_TX',
	'CELL_CTS',
	'CELL_DCD',
	'CELL_DSR',
	'CELL_DTR',
	'CELL_MODEM_RX',
	'CELL_MODEM_TX',
	'CELL_PWR_ON',
	'CELL_RESET',
	'CELL_RTS',
	'COM1_SEL_SDI12',
	'COM2_SEL_SDI12',
	'CTRL_CELL_PWR',
	'DAC0_OUT0',
	'DAC0_OUT1',
	'DC_DC_CNTL',
	'FLASH_SPI_CS',
	'FLASH_SPI_WP',
	'FRAM_SPI_CLK',
	'FRAM_SPI_CS',
	'FRAM_SPI_MISO',
	'FRAM_SPI_MOSI',
	'FRAM_SPI_WP',
	'GPIO_SWO',
	'GPIO_TCLK',
	'GPIO_TD0',
	'GPIO_TD1',
	'GPIO_TD2',
	'GPIO_TD3',
	'GS_ASYNC_IRQ',
	'GS_NEXT_RESET',
	'GS_RX',
	'GS_TX',
	'GS_WAKEUP_STANDBY',
	'I2C0_SCL',
	'I2C0_SDA',
	'LEUART0_RX',
	'LEUART0_TX',
	'LEUART1_RX',
	'LEUART1_TX',
	'LFXO_N',
	'LFXO_P',
	'NRTC_IRQ',
	'OC_OUT',
	'PLUS5V_NOFF',
	'PROGRAM_RESTORE',
	'PUSHBUTTON1',
	'PWR_COM1',
	'PWR_COM2',
	'PWR_COM3',
	'PWR_DAC1',
	'PWR_DAC2',
	'SENS1',
	'SENS2',
	'SENS3',
	'TP5',
	'TP6',
	'TP7',
	'UART0_RX',
	'UART0_TX',
	'UART1_RX',
	'UART1_TX',
	'UCEXC',
	'UC_DEBUG_RX',
	'UC_DEBUG_TX',
	'UC_EN_485N232_1',
	'UC_EN_485N232_2',
	'UC_EN_RX_485232_1',
	'UC_EN_RX_485232_2',
	'UC_EN_TX_485232_1',
	'UC_EN_TX_485232_2',
	'UC_LED1',
	'UC_LED2',
	'UC_LED3',
	'UC_RX_COM1',
	'UC_RX_COM2',
	'UC_RX_COM3',
	'UC_TX_COM1',
	'UC_TX_COM2',
	'UC_TX_COM3',
	'USART0_RX',
	'USART0_TX',
	'USART1_RX',
	'USART1_TX',
	'USART2_CLK',
	'USART2_RX',
	'USART2_TX',
	'USB_RTS',
	'WIFI_PWR_CTRL']

if __name__ == "__main__":
    packet = [0x02, 0x01, 0x0E, 0x63, 0x60, 0x73, 0x60, 0x73, 0x60, 0x85, 0x64, 0x63, 0xE0, 0x83, 0x00, 0x14, 0x04, 0xE0, 0x04, 0x10, 0x04, 0x33, 0x11, 0xC0, 0x01, 0x01, 0x11, 0xA2, 0x04, 0xB5, 0x11, 0xA5, 0x14, 0xB2, 0x14, 0x93, 0x04, 0x23, 0x04, 0x04, 0x14, 0xB0, 0x14, 0x95, 0x14, 0xB1, 0x00, 0xC1, 0x00, 0x44, 0x11, 0x51, 0x14, 0x41, 0x14, 0x42, 0x04, 0x52, 0x14, 0x32, 0x11, 0x22, 0x04, 0x61, 0x14, 0x25, 0x00, 0x60, 0x04, 0x20, 0x04, 0x30, 0x04, 0x40, 0x04, 0x50, 0x04, 0x64, 0x01, 0x92, 0x16, 0x13, 0x11, 0x03, 0x14, 0x34, 0x04, 0x12, 0x1B, 0x02, 0x1B, 0xE1, 0x11, 0xD1, 0x04, 0x72, 0x11, 0x62, 0x04, 0x81, 0x00, 0x71, 0x00, 0x21, 0x11, 0xF0, 0x04, 0xC5, 0x14, 0x74, 0x04, 0xF4, 0x01, 0x24, 0x04, 0xD0, 0x04, 0x11, 0x04, 0xB1, 0x00, 0xC1, 0x00, 0x91, 0x01, 0x70, 0x01, 0x00, 0x01, 0xC4, 0x04, 0xD4, 0x04, 0xE4, 0x04, 0x75, 0x01, 0x65, 0x04, 0xB5, 0x11, 0xA5, 0x14, 0x31, 0x04, 0xB4, 0x11, 0xA4, 0x14, 0x53, 0x04, 0xA0, 0x04, 0xA1, 0x04, 0x90, 0x04, 0x43, 0x04, 0x80, 0x04, 0xC3, 0x04, 0xB3, 0x04, 0xA3, 0x04, 0x72, 0x11, 0xE1, 0x11, 0x75, 0x01, 0x62, 0x04, 0xD1, 0x04, 0x65, 0x04, 0xB4, 0x11, 0xA4, 0x14, 0x13, 0x11, 0x03, 0x14, 0x42, 0x04, 0x32, 0x11, 0x22, 0x04, 0x54, 0x01, 0x82, 0x14, 0x0B, 0x49, 0x0B, 0xF4, 0x08, 0x02, 0x01, 0x73, 0x6C, 0x64, 0x3A, 0x20]
    probeHandler(packet)
    printPins()
