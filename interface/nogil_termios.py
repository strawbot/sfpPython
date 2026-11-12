# termios calls that release the GIL, for pyserial on macOS.
#
# CPython's termios module makes its libc calls with the GIL held. When a USB
# serial device stops answering (jammed firmware, wedged driver), tcsetattr()
# and friends block in the kernel, and with the GIL held that freezes every
# thread in the process: GUI, other ports, the debugger. ctypes releases the
# GIL around foreign calls, so a wedged device then only blocks the one
# thread that touched it.
#
# Only installed on macOS, where the struct layout below is known.

import ctypes
import ctypes.util
import os
import sys
import termios as _termios

_NCCS = 20


class _Termios(ctypes.Structure):
    _fields_ = [('c_iflag', ctypes.c_ulong),
                ('c_oflag', ctypes.c_ulong),
                ('c_cflag', ctypes.c_ulong),
                ('c_lflag', ctypes.c_ulong),
                ('c_cc', ctypes.c_ubyte * _NCCS),
                ('c_ispeed', ctypes.c_ulong),
                ('c_ospeed', ctypes.c_ulong)]


_libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
_libc.tcgetattr.argtypes = [ctypes.c_int, ctypes.POINTER(_Termios)]
_libc.tcsetattr.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(_Termios)]
_libc.tcflush.argtypes = [ctypes.c_int, ctypes.c_int]
_libc.tcdrain.argtypes = [ctypes.c_int]
_libc.tcsendbreak.argtypes = [ctypes.c_int, ctypes.c_int]
_libc.tcflow.argtypes = [ctypes.c_int, ctypes.c_int]


def _check(result):
    if result != 0:
        err = ctypes.get_errno()
        raise _termios.error(err, os.strerror(err))


def tcgetattr(fd):
    t = _Termios()
    _check(_libc.tcgetattr(fd, ctypes.byref(t)))
    cc = []
    for i in range(_NCCS):
        # same shapes as the stock module: bytes, except VMIN/VTIME as ints
        # when not in canonical mode
        if not (t.c_lflag & _termios.ICANON) and i in (_termios.VMIN, _termios.VTIME):
            cc.append(t.c_cc[i])
        else:
            cc.append(bytes([t.c_cc[i]]))
    return [t.c_iflag, t.c_oflag, t.c_cflag, t.c_lflag, t.c_ispeed, t.c_ospeed, cc]


def tcsetattr(fd, when, attributes):
    if not isinstance(attributes, list) or len(attributes) != 7:
        raise TypeError('tcsetattr, arg 3: must be 7 element list')
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = attributes
    if not isinstance(cc, list) or len(cc) != _NCCS:
        raise TypeError('tcsetattr: attributes[6] must be %d element list' % _NCCS)
    t = _Termios()
    t.c_iflag, t.c_oflag, t.c_cflag, t.c_lflag = iflag, oflag, cflag, lflag
    t.c_ispeed, t.c_ospeed = ispeed, ospeed
    for i, v in enumerate(cc):
        if isinstance(v, bytes) and len(v) == 1:
            t.c_cc[i] = v[0]
        elif isinstance(v, int):
            t.c_cc[i] = v
        else:
            raise TypeError('tcsetattr: elements of attributes must be characters or integers')
    _check(_libc.tcsetattr(fd, when, ctypes.byref(t)))


def tcflush(fd, queue):
    _check(_libc.tcflush(fd, queue))


def tcdrain(fd):
    _check(_libc.tcdrain(fd))


def tcsendbreak(fd, duration):
    _check(_libc.tcsendbreak(fd, duration))


def tcflow(fd, action):
    _check(_libc.tcflow(fd, action))


class _GilFreeTermios(object):
    """Stands in for the termios module inside pyserial."""
    tcgetattr = staticmethod(tcgetattr)
    tcsetattr = staticmethod(tcsetattr)
    tcflush = staticmethod(tcflush)
    tcdrain = staticmethod(tcdrain)
    tcsendbreak = staticmethod(tcsendbreak)
    tcflow = staticmethod(tcflow)

    def __getattr__(self, name):        # constants, error class, ...
        return getattr(_termios, name)


def install():
    """Make pyserial use the GIL-releasing calls. No-op off macOS."""
    if sys.platform != 'darwin':
        return False
    from serial import serialposix
    serialposix.termios = _GilFreeTermios()
    return True
