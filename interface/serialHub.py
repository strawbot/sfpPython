# pluggable serial port  Robert Chapman  Jul 26, 2018

from .interface import Port, Hub
from . import listports
import traceback
import serial
from .message import warning, error, note, message
from threading import Thread
import sys
from time import sleep

class SerialPort(Port):
    # define signals
    stopbits = serial.STOPBITS_ONE
    noparity, evenparity, oddparity = serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD
    parity = noparity
    bytesize = serial.EIGHTBITS

    def __init__(self, name, hub=None):
        Port.__init__(self, name, name, hub)
        self.port = None
        self.rate = 115200

    def run(self):
        while self.is_open():
            try:
                c = self.port.read(1)
                if len(c):
                    c += self.port.read(self.port.in_waiting)
                    self.output.emit(c)
            # except IOError:
            #     self.closePort()
            #     note('Alert: device removed while open ')
            except Exception as e:
                self.closePort()
                error("run - serial port exception: %s" % e)
                traceback.print_exc(file=sys.stderr)
        print ('serial thread for {} is done'.format(self.name))

    def open(self, rate=None, thread=True, timeout=.01):
        if self.is_open():
            error("Already opened!")
        else:
            if rate:
                self.rate = rate

            try:
                self.port = serial.Serial(self.name,
                                          self.rate,
                                          timeout=timeout,
                                          # time to accumulate characters: 10 ms @ 115200, thats up to 115.2 chars
                                          parity=self.parity,
                                          stopbits=self.stopbits,
                                          xonxoff=0,
                                          rtscts=0,  # hw flow control
                                          bytesize=self.bytesize)
                Port.open(self)
                note('opened %s at %d' % (self.name, self.rate))
                if sys.platform == 'win32':
                    if self.port._GetCommModemStatus() != 0:
                        self.port.close()
                        raise Exception('Unusable port: '+self.port.name)
                if thread:
                    t = Thread(name=self.name, target=self.run)
                    t.setDaemon(True)
                    t.start()  # run serial port in thread
                sleep(.1)
            except Exception as e:
                if self.port:
                    self.port.close()
                print(e, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                raise Exception('open port failed for ' + self.name)

    def closePort(self):
        Port.close(self)
        self.wait(100) # let thread finish
        self.unplug()
        for sig in self.signals:
            sig.disconnect()

        if self.isOpen():
            try:
                self.port.flush()
                self.port.close()
            except:
                pass
            note('closed %s' % self.name)
        self.port = None

    def close(self):
        self.closePort()
        self.wait(100)

    def send_data(self, s):
        if self.isOpen():
            try:
                self.port.write(s)
            except IOError:
                self.ioError.emit('Alert: device closed while writing ')
            except Exception as e:
                if self.port:
                    self.ioException.emit("Error: send_data - serial port exception: %s" % e)

    def setRate(self, rate):
        if self.rate != rate:
            note('Baudrate changed to %d' % rate)
            self.rate = rate
        if self.isOpen():
            self.port.baudrate = rate

    def isOpen(self):
        if self.port:
            return self.port.isOpen()
        return False

    # support for blocking usage
    def openBlocking(self, port, rate=None):
        self.open(port, rate, thread=False, timeout=0)

    def getc(self, n, timeout=1):
        self.port.timeout = timeout
        return self.port.read(n)

    def putc(self, data, timeout=1):
        self.port.timeout = timeout
        self.port.write(data)


class SerialHub(Hub):
    def __init__(self, interval=2):
        self.update_interval = interval*1000 # change to ms
        Hub.__init__(self, "SerialHub")
        self.running = True
        t = Thread(name=self.name, target=self.run)
        t.setDaemon(True)
        t.start()  # run serial hub in thread
        self.wait(100)

    def run(self):
        try:
            while self.running:
                ports = listports.listports()
                portlist = [port.name for port in self.ports()]
                for r in list(set(portlist) - set(ports)):  # items to be removed
                    self.remove_port(self.get_port(r))
                for a in list(set(ports) - set(portlist)):  # items to be added
                    port = SerialPort(a, self)
                    self.add_port(port)
                self.wait(self.update_interval)
        except Exception as e:
            print(e, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def exit(self):
        self.running = False
        self.wait(self.update_interval*1.1)
        self.close()


# test needs serial cable looped back to itself
if __name__ == '__main__':
    from time import sleep

    def redText():
        return '\033[{}m'.format('31')

    def blackText():
        return '\033[{}m'.format('0')

    class Test(object):
        def __init__(self):
            self.sh = SerialHub()
            self.result = False
            sleep(3)
            self.port = self.sh.ports()[0]

        def didopen(self):
            print("port '{}' at address '{}' is open".format(self.port.name, self.port.address))

        def didclose(self):
            print("port '{}' closed".format(self.port.name))

        def seeInput(self, data):
            self.result = True
            print("Rx'd:[{}]".format(data))

        def test(self):
            try:
                s = self.port
                s.report()
                s.opened.connect(self.didopen)
                s.closed.connect(self.didclose)
                s.output.connect(self.seeInput)
                s.open()
                if s.is_open():
                    print("yes its open")
                    s.report()
                else:
                    print("port not found")

                for i in range(20):
                    s.send_data("test string {}\n".format(i))
                sleep(.1)
                if not self.result:
                    print ('{}Error{}: no data received'.format(redText(), blackText()))
                s.close()
                s.report()
            except Exception as e:
                print(e, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    t = Test()
    print ('test 1')
    t.test()
    sleep(1)
    print ('test 2')
    t.test()
    sys.exit(0)
