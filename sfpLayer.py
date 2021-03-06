# Layer around sfp protocol

from threading import Lock

from . import pids
from . import sfp
from .interface.interface import Layer
from .interface.message import *

mutex = Lock()

class SfpLayer (Layer, sfp.sfpProtocol):
    def __init__(self):
        Layer.__init__(self, 'sfpLayer')
        sfp.sfpProtocol.__init__(self)
        self.setHandler(pids.TALK_OUT, self.talkPacket)
        def probeDump(packet):
            pass
        self.setHandler(pids.PROBE, probeDump)
        self.connected()

    def connected(self):
        self.input.connect(self.talkOut)
        self.inner.input.connect(self.receive_data)

    def receive_data(self, bytes):
        # self.rxBytes(list(map(ord, bytes)))
        self.rxBytes(bytes)

    def newFrame(self):
        data = self.txBytes()
        self.inner.output.emit(data)

    def newPacket(self):
        self.distributer()

    def error(self, code = 0, string = ""):
        self.result = code
        error(string)

    def warning(self, code = 0, string = ""):
        self.result = code
        warning(string)

    def note(self, code = 0, string = ""):
        self.result = code
        note(string)

    def dump(self, tag, buffer):
        messageDump(tag, buffer)

    def talkPacket(self, packet):  # handle text packets
        data = ''.join(map(chr, packet[2:]))
        self.output.emit(data)


if __name__ == '__main__':
    from protocols.interface.serialHub import SerialHub
    from protocols.interface.interface import Interface
    import sys
    import traceback

    class app(object):
        def didopen(self):
            print("port '{}' at address '{}' is open".format(self.port.name, self.port.address))

        def didclose(self):
            print("port '{}' closed".format(self.port.name))

        def got_data(self, data):
            print("Rx'd:[{}]".format(data))

        def test(self):
            try:
                self.hub = SerialHub()
                self.port = self.hub.ports()[0]
                self.layer = SfpLayer()
                self.app = Interface('test')
                # build comm stack
                self.app.plugin(self.layer)
                self.layer.plugin(self.port)

                self.app.input.connect(self.got_data)
                self.layer.connected()
                self.port.opened.connect(self.didopen)
                self.port.closed.connect(self.didclose)
                self.port.report()

                self.port.open()
                if self.port.is_open():
                    print("yes its open")
                else:
                    print("port not found")

                self.app.output.emit('\r')
                self.port.wait(1000)
                self.hub.close()
            except Exception as e:
                print(e, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
            finally:
                sys.exit(0)

    t = app()
    t.test()
