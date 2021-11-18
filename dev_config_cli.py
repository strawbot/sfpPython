import serial
import time


CONTROL_COMMAND = [0xbd, 0xf2, 0x13, 0x00, 0x00, 0x00, 0x04, 0xce, 0x84, 0xbd]
CONTROL_TERMINAL = [0xbd, 0xf2, 0x13, 0x82, 0x00, 0x00, 0x02, 0x09, 0x68, 0xbd, 0x0d]


def cmd_to_bytes(cmd):
    return bytes(cmd, 'utf-8')


class DeviceConfigCLI:
    def __init__(self, port_num):
        self.__port_num = port_num
        self.__port = None
        self.init_cli()  # will open port and send commands via dev config protocol to go to terminal mode

    def __open_port(self):
        return serial.Serial(self.__port_num, 57600, timeout=0.5, stopbits=1, parity='N', bytesize=8)

    def init_cli(self):
        open_port = self.__open_port()
        open_port.write(bytearray(CONTROL_COMMAND))
        resp = open_port.readlines()
        open_port.write(bytearray(CONTROL_TERMINAL))
        resp2 = open_port.readlines()
        self.__port = open_port

    def close_port(self):
        self.__port.close()

    def write_port(self, cmd):
        self.__port.write(cmd_to_bytes(cmd))

    def read_port(self, timeout=0.1):
        end = time.time() + timeout
        collected = b''
        while time.time() < end:
            resp = self.__port.read(self.__port.in_waiting)
            if resp:
                collected += resp
                end = time.time() + timeout
        return collected

    def get_response(self, timeout=0.5):
        end = time.time() + timeout
        while True:
            resp = self.read_port()
            if resp or time.time() > end:
                return resp

    def get_whoami(self):
        self.write_port('whoami\r\n')
        return self.parse_whoami(self.get_response(1.0))

    @staticmethod
    def parse_whoami(whosit):
        who_dict = {}
        if whosit:
            lines = whosit.split(b'\n')
            for line in lines:
                if line.startswith(b'whoami'):
                    continue
                if line.startswith(b'\ral200:'):
                    continue
                if line.startswith(b'Revision'):
                    who_dict['Revision'] = line.decode('utf-8').strip('\r\n')[14:]
                    continue
                if line.startswith(b'UTC'):
                    who_dict['UTC'] = line.decode('utf-8').strip('\r\n')[14:]
                    continue
                spl = line.decode('utf-8').strip('\r\n').split(':')
                who_dict[spl[0].lstrip()] = spl[1].strip()
        return who_dict

    def is_alive(self):
        self.write_port('\r\n')
        resp = self.get_response()
        try:
            if b'al200:' in resp:
                return True
        except IndexError as e:
            pass
        return False

    def restart_device(self):
        self.write_port('restart')
        time.sleep(.5)


if __name__ == '__main__':
    dcc = DeviceConfigCLI('COM33')
    # dcc.init_cli()
    alive = dcc.is_alive()
    if alive:
        whosit = dcc.get_whoami()
        print(whosit)
        whosit = dcc.get_whoami()
        print(whosit)
        whosit = dcc.get_whoami()
        print(whosit)
        whosit = dcc.get_whoami()
        print(whosit)


