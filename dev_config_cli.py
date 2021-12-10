import serial
import time


CONTROL_COMMAND = [0xbd, 0xf2, 0x13, 0x00, 0x00, 0x00, 0x04, 0xce, 0x84, 0xbd]
CONTROL_TERMINAL = [0xbd, 0xf2, 0x13, 0x82, 0x00, 0x00, 0x02, 0x09, 0x68, 0xbd, 0x0d]


def cmd_to_bytes(cmd):
    return bytes(cmd + '\r\n', 'utf-8')


class DeviceConfigCLI:
    def __init__(self, port_num):
        self.port_num = port_num
        self.__port = None
        self.init_cli()  # will open port and send commands via dev config protocol to go to terminal mode

    def __open_port(self):
        return serial.Serial(self.port_num, 57600, timeout=0.5, stopbits=1, parity='N', bytesize=8)

    def init_cli(self):
        if self.__port:
            if not self.__port.isOpen():
                self.__port = self.__open_port()
        else:
            self.__port = self.__open_port()
        self.__port.write(bytearray(CONTROL_COMMAND))
        resp = self.__port.readlines()
        self.__port.write(bytearray(CONTROL_TERMINAL))
        resp2 = self.__port.readlines()


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
                try:
                    return resp.decode('utf-8')
                except UnicodeDecodeError as e:
                    return ''

    def get_whoami(self):
        if not self.is_alive():
            self.init_cli()
        self.write_port('whoami')
        return self.parse_whoami(self.get_response(1.0))

    @staticmethod
    def parse_whoami(whosit):
        who_dict = {}
        if whosit:
            lines = whosit.split('\n')
            for line in lines:
                if line.startswith('whoami'):
                    continue
                if line.startswith('\ral200:'):
                    continue
                if line.startswith('Revision'):
                    who_dict['Revision'] = line.strip('\r\n')[14:]
                    continue
                if line.startswith('UTC'):
                    who_dict['UTC'] = line.strip('\r\n')[14:]
                    continue
                spl = line.strip('\r\n').split(':')
                who_dict[spl[0].lstrip()] = spl[1].strip()
        return who_dict

    def is_alive(self):
        self.write_port('\r\n')
        try:
            resp = self.get_response()
            if 'al200:' in resp:
                return True
        except IndexError as e:
            pass
        return False

    def send_cmd_get_resp(self, cmd):
        # Use this method for commands that generate a single line response, i.e. getting settings
        if not self.is_alive():
            self.init_cli()
        self.write_port(cmd)
        resp = self.get_response()
        if resp:
            idx = resp.find(cmd)
            if idx >= 0:
                actual = resp[idx + len(cmd):].split('\n')[0].strip()
                return actual
        return ''

    def send_command(self, cmd):
        # Use this to send commands that don't need a response, i.e. setting settings
        if not self.is_alive():
            self.init_cli()
        self.write_port(cmd)
        self.get_response()

    def restart_device(self):
        self.send_command('restart')
        time.sleep(.5)


if __name__ == '__main__':
    dcc = DeviceConfigCLI('COM33')
    alive = dcc.is_alive()
    if alive:
        whosit = dcc.get_whoami()
        print(whosit)
        dcc.send_command('800 agctime s!')
        agc = dcc.send_cmd_get_resp('agctime s@ .')
        dcc.send_command('1 invertmodulation c!')
        inv = dcc.send_cmd_get_resp('invertmodulation c@ .')
        print(agc)
