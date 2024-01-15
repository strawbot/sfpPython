import serial
import time


CONTROL_COMMAND = [0xbd, 0xf2, 0x13, 0x00, 0x00, 0x00, 0x04, 0xce, 0x84, 0xbd]
CONTROL_TERMINAL = [0xbd, 0xf2, 0x13, 0x82, 0x00, 0x00, 0x02, 0x09, 0x68, 0xbd]
CONTROL_PROMPT = [0x20, 0x0d]


def cmd_to_bytes(cmd):
    # Will turn plain strings into byte strings for sending over serial + carriage return and line feed
    return bytes(cmd + '\r', 'utf-8')


class DeviceConfigCLI:
    def __init__(self, port_num):
        self.port_num = port_num
        self.__port = None
        self.init_cli()  # will initialize port when the class is instantiated

    def __open_port(self):
        return serial.Serial(self.port_num, 57600, timeout=0.5, stopbits=1, parity='N', bytesize=8)

    def is_open(self):
        if self.__port.isOpen():
            return True
        else:
            return False

    def init_cli(self):
        # Checks if port is open
        if self.__port:
            if not self.__port.isOpen():
                self.__port = self.__open_port()
        else:
            self.__port = self.__open_port()
        # Send dev config commands to put unit into terminal mode
        self.__port.write(bytearray(CONTROL_COMMAND))
        resp = self.__port.readlines()
        self.__port.write(bytearray(CONTROL_TERMINAL))
        resp2 = self.__port.readlines()

    def close_port(self):
        self.__port.close()

    def write_port(self, cmd):
        self.__port.write(cmd_to_bytes(cmd))

    def read_port(self, timeout=1):
        # Reads the response from the serial port with a settable timeout
        end = time.time() + timeout
        collected = b''
        while time.time() < end:
            resp = self.__port.read(self.__port.in_waiting)
            if resp:
                collected += resp
                end = time.time() + timeout
        return collected

    def get_response(self, timeout=0.5):
        # Same as read_port but adds a layer for decoding and error handling
        end = time.time() + timeout
        collected = ''
        while time.time() < end:
            resp = self.read_port()
            if resp:
                end = time.time() + timeout
                try:
                    collected += resp.decode('utf-8')
                except UnicodeDecodeError as e:
                    continue
        return collected

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
                if line:
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
                    if ':' in line:
                        spl = line.strip('\r\n').split(':')
                        who_dict[spl[0].lstrip()] = spl[1].strip()
        return who_dict

    def is_alive(self):
        self.write_port(' \r')
        try:
            resp = self.get_response()
            if 'al200:' in resp:
                return True
        except IndexError as e:
            pass
        return False

    def send_cmd_get_resp(self, cmd):
        # Use this method for commands that generate a single line response, i.e. getting settings
        resp = self.send_command(cmd)
        if resp:
            # Parsing response
            idx = resp.find(cmd)
            if idx >= 0:
                actual = resp[idx + len(cmd):]
                actual = actual.split('\n')[1].strip()
                return actual
        return ''

    def send_command(self, cmd):
        # Use this to send commands that don't need a response, i.e. setting settings
        # if not self.is_alive():  # Check if dev config has timed out before sending
        #     self.init_cli()
        self.write_port(cmd)
        return self.get_response()

    def sdi12_command(self, cmd):
        sdi_12 = []
        resp = self.send_command('z ' + cmd)
        if resp.find(cmd) >= 0:
            print("Raw cmd response: {}".format(resp))
            # time.sleep(1)
            # resp = self.get_response(timeout=1.0)
            # print("Raw response: {}".format(resp))
            if not resp:
                resp = self.get_response()
                print("Retry raw resp: {}".format(resp))
            for r in resp.split('\n'):
                if r:
                    if r.startswith('\r'):
                        continue
                    if r.startswith('z'):
                        continue
                    if r.startswith('al200:'):
                        continue
                    if r.startswith('No'):
                        sdi_12.append(r)
                        return sdi_12
                    sdi_12.append((r.split('  ')[0], r.split('  ')[1]))
        return sdi_12

    def restart_device(self):
        self.send_command('restart')
        time.sleep(.5)

    def get_gps_status(self, full=False):
        gps = self.send_command('gps')
        if full:
            return gps[5:]
        else:
            gps = gps.split('\n')
            for g in gps:
                if 'baud:' in g:
                    try:
                        return g.split('  ')[1]
                    except IndexError:
                        return ''

    def get_clock_status(self):
        status = self.get_whoami()['status']
        return status[0]


if __name__ == '__main__':
    dcc = DeviceConfigCLI('COM34')
    alive = dcc.is_alive()
    if alive:
        whosit = dcc.get_whoami()
        print(whosit)
        dcc.send_command('800 agctime s!')
        agc = dcc.send_cmd_get_resp('agctime s@ .')
        dcc.send_command('1 invertmodulation c!')
        inv = dcc.send_cmd_get_resp('invertmodulation c@ .')
        print(agc)
