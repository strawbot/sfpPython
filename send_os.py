import os, sys
import time
import serial
# from Pylibs.sfpPort import SfpPort
# from Pylibs.protocols.interface.serialHub import SerialPort

FW_FILE = '../Alert2Encoder/Alert2Encoder/Debug/Alert2Encoder_os.hex'

# "main" method to use for AL200 programming
def send_firmware(port_num):
    return send_os(port_num)


def build_preamble():  # Will build lines needed for srecord preamble and return as a list of 2 items
    ret = []
    l1 = bytearray()
    l1.append(0xbd)
    l1.append(0xf2)
    l1.append(0x13)
    l1.append(0x00)
    l1.append(0x00)
    l1.append(0x00)
    l1.append(0x05)
    l1.append(0xcc)
    l1.append(0x83)
    l1.append(0xbd)
    ret.append(l1)
    l2 = bytearray()
    l2.append(0x41)
    l2.append(0x4c)
    l2.append(0x32)
    l2.append(0x30)
    l2.append(0x30)
    ret.append(l2)
    return ret


def write_line(port, data):
    return port.write(data)


def check_response(port, expected):
    res = port.read_until()
    if res == expected:
        print(res)
        return True
    return False


def get_hex_file():
    # Read hex file in binary mode
    with open(FW_FILE, 'rb') as f:
        lines = f.readlines()

    # Need to change from Linux line endings or the device will not receive the OS
    newlines = []
    for l in lines:
        l = l.strip(b'\r\n') + b'\r\n'
        newlines.append(l)
    return newlines


def send_control_command(port, preamble):
    start = time.time()
    while True:
        port.write(preamble[0])
        ctrl = check_response(port, b'\xbd\xf2\x93\x00\x04\xc2\x7a\xbd')
        if ctrl:
            print("Received control response")
            return True
        if time.time() > start + 10:
            print("Timed out waiting for control response")
            break
        time.sleep(.5)
    return False


def send_device_type(port, preamble):
    start = time.time()
    while True:
        port.write(preamble[1])
        echo = check_response(port, b'AL200\x06')
        if echo:
            print("Device type echo received")
            return True
        if time.time() > start + 10:
            print("Timed out waiting for device type echo")
            break
        time.sleep(.5)
    return False


def send_os(port_num, notifier):
    file = get_hex_file()
    port = serial.Serial(port_num, 57600, timeout=0.8, stopbits=1, parity='N')
    pre = build_preamble()

    if not send_control_command(port, pre):
        port.close()
        return False

    if not send_device_type(port, pre):
        port.close()
        return False

    count = 0
    for l in file[:-1]:  # Write all lines except the last
        port.write(l)
        port.read()
        count += 1
        notifier(count, len(file))
    port.write(file[-1])  # Write last line
    count += 1
    fin = port.read(2)
    print("Lines written: ", count)
    print("Length of hex file: ", len(file))
    port.close()
    if count != len(file):
        return False
    # check final response from device
    if b'\x04\x00' in fin:
        return True
    else:
        return False


if __name__ == '__main__':
    result = send_firmware('/dev/cu.usbserial-1442440')
    print("Send OS result: {}".format(result))
