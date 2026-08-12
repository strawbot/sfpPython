# telnetPort.py — TCP/Telnet connection as a Port  Robert Chapman
#
# TelnetPort wraps a TCP socket in the Port interface so it can be
# plugged into the protocol stack exactly like a SerialPort.
#
# Telnet option negotiation: the server sends IAC DO/WILL sequences and
# expects responses before it will send any data.  We respond to every
# option with WONT/DONT (refuse all options), which is the standard way
# for a minimal Telnet client to get past the negotiation phase quickly.
# IAC SB … SE subnegotiation blocks are consumed and discarded.
# An escaped IAC IAC pair is decoded to a literal 0xFF data byte.

import socket
import sys
import traceback
from threading import Thread
from time import sleep

from .interface import Port
from .message import note, error

# Telnet command bytes (RFC 854)
IAC  = 0xFF   # Interpret As Command
SB   = 0xFA   # Begin subnegotiation parameters
SE   = 0xF0   # End subnegotiation parameters
WILL = 0xFB   # I will use option
WONT = 0xFC   # I will not use option
DO   = 0xFD   # Please use option
DONT = 0xFE   # Please stop using option

RECV_SZ = 4096


class TelnetPort(Port):
    """A Port backed by a TCP socket (Telnet-style client connection).

    Usage:
        p = TelnetPort('192.168.1.1', 23)
        p.ioError.connect(handle_error)
        p.open()                        # connects and starts reader thread
        p.send_data(b'hello\\r\\n')
        p.close()
    """

    def __init__(self, host, tcp_port):
        name = '%s:%d' % (host, tcp_port)
        Port.__init__(self, address=(host, tcp_port), name=name, hub=None)
        self._host     = host
        self._tcp_port = tcp_port
        self._sock     = None

    # ------------------------------------------------------------------ open

    def open(self, rate=None, **kwargs):
        """Connect to host:tcp_port and start the reader thread.
        ``rate`` is accepted but ignored (no baud rate for TCP).
        Raises ConnectionError on failure.
        """
        if self.is_open():
            error('TelnetPort: already open')
            return
        try:
            # Resolve the address first so we can log what we're trying.
            # getaddrinfo returns all address families (IPv4 + IPv6), so the
            # user can see exactly what was resolved if the connect fails.
            infos = socket.getaddrinfo(self._host, self._tcp_port,
                                       type=socket.SOCK_STREAM)
            addrs = ['%s:%s' % (ai[4][0], ai[4][1]) for ai in infos]
            note('telnet resolving %s → %s' % (self._host, ', '.join(addrs)))

            # create_connection() tries every resolved address in order
            # (IPv6 then IPv4 on most systems), matching what the system
            # telnet command does.
            sock = socket.create_connection((self._host, self._tcp_port),
                                            timeout=5.0)
            sock.settimeout(None)       # switch to blocking recv after connect
            self._sock = sock
            peer = sock.getpeername()
            Port.open(self)
            note('telnet connected to %s (peer %s:%s)' % (self._host, peer[0], peer[1]))
            t = Thread(name=self.name, target=self.run, daemon=True)
            t.start()
            sleep(0.05)                 # give reader thread a moment to start
        except Exception as e:
            if self._sock:
                try:
                    self._sock.close()
                except Exception:
                    pass
                self._sock = None
            traceback.print_exc(file=sys.stderr)
            msg = '%s (port %d): %s' % (self._host, self._tcp_port, e)
            import errno as _errno
            if getattr(e, 'errno', None) == _errno.EHOSTUNREACH:
                msg += '\n  Hint: macOS may be blocking local-network access for this Python process.\n' \
                       '  Check System Settings → Privacy & Security → Local Network.'
            raise ConnectionError(msg)

    # ----------------------------------------------------------------- reader

    def run(self):
        """Reader thread — pumps incoming bytes into the protocol stack.

        For each received chunk, IAC option sequences are parsed: options
        are refused with WONT/DONT so the server doesn't stall waiting for
        a response.  Clean data is forwarded via output.emit().
        """
        while self.is_open():
            try:
                chunk = self._sock.recv(RECV_SZ)
                if not chunk:
                    # Remote closed the connection cleanly
                    if self.is_open():
                        self.ioError.emit('telnet: remote closed connection')
                    break
                data, responses = self._process_iac(chunk)
                if responses:
                    try:
                        self._sock.sendall(responses)
                    except Exception:
                        pass
                if data:
                    self.output.emit(data)
            except Exception as e:
                if self.is_open():
                    self.ioError.emit('telnet rx: %s' % str(e))
                break
        if self.is_open():
            self.closePort()
        print('telnet thread for %s done' % self.name)

    # ------------------------------------------------------ IAC negotiation

    @staticmethod
    def _process_iac(data):
        """Parse Telnet IAC sequences from a received chunk.

        Returns:
            (clean_data, responses)
            clean_data  — bytes with all IAC sequences removed/decoded
            responses   — bytes to send back to the server
                          (WONT for DO/DONT, DONT for WILL/WONT options)
        """
        out      = bytearray()
        response = bytearray()
        i        = 0
        while i < len(data):
            b = data[i]
            if b != IAC:
                out.append(b)
                i += 1
                continue
            # We have IAC — need at least one more byte
            if i + 1 >= len(data):
                i += 1          # lone IAC at end of buffer; skip
                continue
            cmd = data[i + 1]
            if cmd == IAC:
                # IAC IAC → literal 0xFF data byte
                out.append(IAC)
                i += 2
            elif cmd == SB:
                # Subnegotiation block: consume until IAC SE
                j = i + 2
                while j < len(data) - 1:
                    if data[j] == IAC and data[j + 1] == SE:
                        j += 2
                        break
                    j += 1
                i = j
            elif cmd in (WILL, WONT, DO, DONT):
                if i + 2 < len(data):
                    opt = data[i + 2]
                    # Refuse every option:
                    #   DO X   → WONT X   (we won't comply)
                    #   DONT X → WONT X   (acknowledge)
                    #   WILL X → DONT X   (we don't want it)
                    #   WONT X → DONT X   (acknowledge)
                    if cmd in (DO, DONT):
                        response += bytes([IAC, WONT, opt])
                    else:
                        response += bytes([IAC, DONT, opt])
                    i += 3
                else:
                    i += 1      # incomplete triple at end of buffer
            else:
                # Single-byte command (GA, NOP, EOR …)
                i += 2
        return bytes(out), bytes(response)

    # ------------------------------------------------------------- send / close

    def send_data(self, data):
        if self._sock and self.is_open():
            try:
                if isinstance(data, str):
                    # The serial protocol stack terminates commands with \x00
                    # (a null sentinel).  Telnet requires \r\n per RFC 854.
                    # Replace the trailing null with CRLF before sending.
                    if data.endswith('\x00'):
                        data = data[:-1] + '\r\n'
                    data = data.encode()
                elif isinstance(data, list):
                    data = bytes(data)
                self._sock.sendall(data)
            except IOError:
                self.ioError.emit('telnet: send failed (connection lost)')
            except Exception as e:
                if self._sock:
                    self.ioException.emit('telnet: send error: %s' % str(e))

    def closePort(self):
        Port.close(self)
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
        self.unplug()
        for sig in self.signals:
            sig.disconnect()
        note('telnet closed %s' % self.name)

    def close(self):
        self.closePort()
        sleep(0.05)

    def isOpen(self):
        """True if the TCP socket is present (mirrors SerialPort.isOpen())."""
        return self._sock is not None
