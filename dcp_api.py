import io, traceback, sys, time, serial
import binascii, struct
from Pylibs.protocols.airlink import bit_fields
from Pylibs.protocols.decode_peri import decode_settings

# if __name__ == "__main__":
#     from airlink import bit_fields
# else:
#     from .airlink import bit_fields

# string formatting for text output
def toHex(c):
    if type(c) == type('0'):
        c = ord(c)

    if c < 0x100:
        return '<{:02X}>'.format(c)
    if c < 0x10000:
        return '<{:04X}>'.format(c)
    if c < 0x1000000:
        return '<{:06X}>'.format(c)
    return '<{:X}>'.format(c)

def hexify(s):
    return ''.join(map(lambda x: ' ' + toHex(x)[1:3], s))

def hx(s,n):
    return '{} {}'.format(s,toHex(n)[1:-1])

def hx4(s,n):
    return '{} {:04X}'.format(s,n)

def hb(s,n):
    return '{} {}'.format(s,n)

msg_types = {0x0F: 'Get Settings',
             0x10: 'Set Settings',
             0x11: 'Get Fragment',
             0x12: 'Set Fragment',
             0x13: 'Control',
             0x14: 'File Send',
             0x17: 'Discovery'}

def msgType(msgname):
    for id,name in msg_types.items():
        if name == msgname:
            return id
    return 0

def typify(s,n):
    index = 0x7F & n
    type = msg_types.get(index, '<unknown:%X>'%index)
    dir = 'Cmd:' if n < 0x7F else 'Rsp:'
    return '{} {} {} {}'.format(s,toHex(n)[1:-1],dir,type)

def to_n(msg):
    n = 0
    for m in msg:
        n = n << 8 | m
    return n

# invokes extras() when built
class packet(bytearray):
    def __init__(self, *args, **kwargs):
        bytearray.__init__(self, *args, **kwargs)
        self.extras()

# decoded structures
h = bit_fields([ #(name, span)
        ("Sync", 8),
        ("Class", 8),
        ("Type", 8),
        ("Tranno", 8),
    ])

t = bit_fields([
        ("Checksum", 16),
        ("Sync", 8),
    ])

se = bit_fields([ # settings - setting
    ("settingid", 16),
    ("largevalue", 1),
    ("settinglen", 15),
])

ser = bit_fields([ # settings - setting read only
    ("settingid", 16),
    ("largevalue", 1),
    ("readonly", 1,),
    ("valuelength", 14),
])

sf = bit_fields([ # settings - setting
    ("settingid", 16),
    ("fragmentoffset", 32),
    ("morefragments", 1),
    ("fragmentlen", 15),
])

so = bit_fields([ # setting outcome
    ("settingid", 16),
    ("settingoutcome", 8),
])

gs = bit_fields([ # get settings command
    ("securitycode", 16),
    ("startafter", 1),
    ("beginsettingid", 15),
    ("reserved", 1),
    ("endsettingid", 15),
])

gf = bit_fields([ # get settings command
    ("securitycode", 16),
    ("settingid", 16),
    ("offset", 32),
])

gfr = bit_fields([
    ("outcome", 8),
    ("morefragments", 1),
    ("fragmentlen", 15),
])

ghr = bit_fields([ # get settings response header
    ("outcome", 8),
    ("devicetype", 16),
    ("majorversion", 8),
    ("minorversion", 8),
    ("moresettings", 8)
])

# make a choice on which settings to use: AL200 or AL200X
from al200x_dcp import *
# from al200_dcp import *

# message decoding
RESP = 0x80
Control = 0x13
Response = Control + RESP
GetSettings = 0x0F
SetSettings = 0x10
GetFragment = 0x11
SetFragment = 0x12
GetSettingsResponse = GetSettings + RESP
SetSettingsResponse = SetSettings + RESP
GetFragmentResponse = GetFragment + RESP
SetFragmentResponse = SetFragment + RESP

def id_name(msg):
    id = ser.settingid(msg)[1]
    name = settings.get(id, '<unknown>')
    if id == 1:
        length = ser.valuelength(msg)[1]
        name += ': ' + str(msg[4:4 + length], 'utf-8')
    return id,name

def gs_msg(msg):
    out = ' ' + hx4(*gs.securitycode(msg)) + '\n'
    if len(msg) > 2:
        out += ' ' + hx(*gs.startafter(msg)) + '\n'
        out += ' ' + hb(*gs.beginsettingid(msg)) + '\n'
    if len(msg) > 4:
        out += ' ' + hx(*gs.reserved(msg)) + '\n'
        out += ' ' + hb(*gs.endsettingid(msg)) + '\n'
    return out[:-1]

newsettings = bytearray()

def gsr_msg(msg):
    out = ' ' + hb(*ghr.outcome(msg)) + '\n'
    if len(msg) > 1:
        out += ' ' + hx(*ghr.devicetype(msg)) + '\n'
        out += ' ' + hb(*ghr.majorversion(msg)) + '\n'
        out += ' ' + hb(*ghr.minorversion(msg)) + '\n'
        out += ' ' + hb(*ghr.moresettings(msg)) + '\n'
        del (msg[:6])
        while msg:
            id, name = id_name(msg)
            out += '  ' + hx(*ser.settingid(msg)) + '(%i) %s\n' % (id, name)
            out += '   ' + hb(*ser.largevalue(msg)) + '\n'
            out += '   ' + hb(*ser.readonly(msg)) + '\n'
            out += '   ' + hb(*ser.valuelength(msg)) + '\n'
            length = ser.valuelength(msg)[1]
            del (msg[:4])
            decimal = ' (%i)\n'%to_n(msg[:length]) if length < 20 else '\n'
            out += '    value:' + hexify(msg[:length]) + decimal
            if id == 360:
                newsettings[:] = msg[:length]
            del (msg[:length])
    return out[:-1]

def gf_msg(msg):
    out = ' ' + hx4(*gf.securitycode(msg)) + '\n'
    out += ' ' + hb(*gf.settingid(msg)) + '\n'
    out += ' ' + hb(*gf.offset(msg)) + '\n'
    return out[:-1]

def gfr_msg(msg):
    out = ' ' + hb(*gfr.outcome(msg)) + '\n'
    out += '   ' + hb(*gfr.morefragments(msg)) + '\n'
    out += '   ' + hb(*gfr.fragmentlen(msg)) + '\n'
    length = ser.valuelength(msg)[1]
    del (msg[:3])
    decimal = ' (%i)\n'%to_n(msg[:length]) if length < 20 else '\n'
    out += '    value:' + hexify(msg[:length]) + decimal
    out += decode_settings(newsettings + msg[:length]) + '\n'
    del (msg[:length])
    return out[:-1]

def ss_msg(msg):
    out = ' ' + hx4(*gs.securitycode(msg)) + '\n'
    del(msg[:2])
    while msg:
        id, name = id_name(msg)
        out += '  ' + hx(*so.settingid(msg)) + '(%i) %s\n' % (id, name)
        out += '   ' + hb(*se.largevalue(msg)) + '\n'
        out += '   ' + hb(*se.settinglen(msg)) + '\n'
        length = se.settinglen(msg)[1]
        lv = se.largevalue(msg)
        del(msg[:4])
        out += '    value:' + hexify(msg[:length]) + '\n'
        if lv:
            newsettings[:] = msg[:length]
        else:
            out += decode_settings(msg[:length]) + '\n'
        del (msg[:length])
    return out[:-1]

def ssr_msg(msg):
    out = ' ' + hb(*ghr.outcome(msg)) + '\n'
    del(msg[0])
    # while msg:
    #     id, name = id_name(msg)
    #     out += '  ' + hx(*so.settingid(msg)) + '(%i) %s\n' % (id, name)
    #     out += '   ' + hx(*so.settingoutcome(msg)) + '\n'
    #     del(msg[:3])
    return out[:-1]

def sf_msg(msg):
    out = ' ' + hx4(*gs.securitycode(msg)) + '\n'
    del(msg[:2])
    id, name = id_name(msg)
    out += '  ' + hx(*so.settingid(msg)) + '(%i) %s\n' % (id, name)
    del(msg[:2])
    out += '   ' + hb(*sf.fragmentoffset(msg)) + '\n'
    out += '   ' + hb(*sf.morefragments(msg)) + '\n'
    out += '   ' + hb(*sf.fragmentlen(msg)) + '\n'
    del(msg[:4])
    length = sf.fragmentlen(msg)[1]
    del(msg[:2])
    out += '    value:' + hexify(msg[:length]) + '\n'
    out += decode_settings(newsettings + msg[:length]) + '\n'
    del (msg[:length])
    return out[:-1]

def sfr_msg(msg):
    out = ' ' + hb(*ghr.outcome(msg)) + '\n'
    del(msg[0])
    return out[:-1]

def decode_msg(typ, msg):
    if typ == Control:
        cmds = ['','Commit, Exit','Cancel, Exit', 'Default settings', 'Refresh only', 'Load OS', 'Scan Wifi']
        return ' securitycode: {:04X}\n command: {}'.format((msg[0]<<8) + msg[1], cmds[msg[2]])
    if typ == Response:
        res = ['', 'Commit and reboot', 'security fail', 'session ending', 'load os', 'semi defaults', 'be calm', 'settings busy', 'system error', 'bad action', 'scanning wifi']
        return 'Status: ' + res[msg[0]]
    if typ == GetSettings:
        return gs_msg(msg)
    if typ == GetSettingsResponse:
        return gsr_msg(msg)
    if typ == SetSettings:
        return ss_msg(msg)
    if typ == SetSettingsResponse:
        return ssr_msg(msg)
    if typ == SetFragment:
        return sf_msg(msg)
    if typ == SetFragmentResponse:
        return sfr_msg(msg)
    if typ == GetFragment:
        return gf_msg(msg)
    if typ == GetFragmentResponse:
        return gfr_msg(msg)
    return 'Msg:%s'%hexify(msg)

SYNC = 0xBD
QUOTED = 0xBC
MASKER = 0x20
START_SIG = 0xAAAA

def decode_frame(frame):
    f = io.StringIO()
    try:
        print("Frame length: %i"%len(frame), end="")
        print(hx(*h.Sync(frame)), file=f)
        print(hx(*h.Class(frame)), file=f)
        print(typify(*h.Type(frame)), file=f)
        print(hx(*h.Tranno(frame)), file=f)

        head, rest = h.behead(frame)
        msg, tail = t.betail(rest)

        print(decode_msg(h.Type(frame)[1], msg), file=f)
        print(hx(*t.Checksum(tail)), get_signature(frame[1:-1]), file=f)
        print(hx(*t.Sync(tail)), file=f)
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stderr)
        print("Decode error", file=f)

    a = f.getvalue()
    f.close()
    return a

def dequote(frame):
    out = bytearray()
    quote = False
    for b in frame:
        if b is QUOTED:
            quote = True
        elif quote:
            quote = False
            newb = b - MASKER
            if newb not in [SYNC, QUOTED]:
                print("Error: not a quoted byte %02X"%newb)
                newb = b
            out.append(newb)
        else:
            out.append(b)
    return out

def decode_dcp(input):
    # need to treat as a stream and parse it that way
    # bytes need to accumulate in bunches and then frames parsed out
    # then dequoted
    # then decode
    if input[0] == SYNC and len(input) > 1:
        if input[1] == SYNC:
            if type(input) == type(bytearray()):
                del(input[0])
            return ''
        end = input[1:].find(bytes([SYNC]))
        if end != -1:
            end += 2
            raw = bytearray(input[:end])
            frame = dequote(raw)
            if type(input) == type(bytearray()):
                del(input[:end])
            return '\n' + hexify(raw) + '\n' + decode_frame(frame)
    else:
        start = input.find(bytes([SYNC]))
        if start > 0:
            out = '\nUnframed data: ' + hexify(input[:start])
            if type(input) == type(bytearray()):
                del(input[:start])
            return out
    return ''

def deframe(frame):
    if frame and frame[0] is SYNC  and  frame[-1] is SYNC:
        return frame[1:-1]
    return frame

# encoding; quote SYNC or QUOTED and then wrap in SYNCs
DCP_CLASS = 0xF2

def encode(frame):
    encoded = sum([[x] if x not in [SYNC, QUOTED] else [QUOTED, x + MASKER]  for x in frame], start=[])
    return bytes([SYNC] + encoded + [SYNC])

def print_dcp(dcp):
    for c in dcp.split(bytes.fromhex(hex(SYNC)[2:])):
        if c:
            print(decode_dcp(encode(c)))

class dcp_msg(bytearray):
    tranno = 0x8E

    def add_tranno(msg):
        msg.append(dcp_msg.tranno)
        dcp_msg.tranno += 1
        dcp_msg.tranno %= 256

    def add_short(msg, value):
        msg.append(0xFF&(value>>8))
        msg.append(0xFF&value)

    def add_value(msg, value, length):
        if type(value) == type(1.0):
            msg.extend(struct.pack('!f', value))
        else:
            while length:
                length -= 1
                msg.append(0xFF & (value >> (8 * length)))

'''
/***********************************************************************
 *
 * Signature nullifier functions
 * Used for PakBus protocol
 ***********************************************************************/
static U16 do_sig(U16 old_sig, U8 val) {
    volatile U16 new_sig;
    new_sig = (old_sig << 1) & 0x1FF;
    if (new_sig >= 0x100)
        new_sig++;
    new_sig = ((new_sig + ((old_sig >> 8)) + val) & 0xff) | (old_sig << 8);
    return (new_sig);
}

Short signature(Byte *msg, Short length) {
    Short sig = START_SIG;
    while (length--)
        sig = do_sig(sig, *msg++);
    return sig;
}

U16 end_signature(U16 checksum) {
    // calculate the value for the most significant byte.
    // Then run this value through the signature
    // algorithm using the specified signature as seed.
    // The calculation is designed to cause the
    // least significant byte in the signature to become zero.
    volatile U16 new_seed = (checksum << 1) & 0x1FF;
    volatile U16 new_sig = checksum;
    volatile U8 null1, null2;

    if (new_seed >= 0x0100)
        new_seed++;
    null1 = (U8)(0x0100 - (new_seed + (checksum >> 8)));
    new_sig = do_sig(checksum, null1);

    // now perform the same calculation for the most significant byte
    // in the signature. This time we
    // will use the signature that was calculated using the first null byte
    new_seed = (new_sig << 1) & 0x01FF;
    if (new_seed >= 0x0100)
        new_seed++;
    null2 = (U8)(0x0100 - (new_seed + (new_sig >> 8)));

    // now form the return value placing null1 in the most significant byte
    return null1<<8|null2;
}

'''
def get_signature(msg):
    def do_sig(old_sig, val):
        new_sig = (old_sig << 1) & 0x1FF
        if new_sig >= 0x100:
            new_sig += 1
        new_sig = ((new_sig + ((old_sig >> 8)) + val) & 0xFF) | (old_sig << 8)
        return new_sig & 0xFFFF

    def end_sig(checksum):
        new_seed = (checksum << 1) & 0x1FF
        new_sig = checksum

        if new_seed >= 0x0100:
            new_seed += 1
        null1 = 0xFF & (0x0100 - (new_seed + (checksum >> 8)))
        new_sig = do_sig(checksum, null1)

        new_seed = (new_sig << 1) & 0x01FF
        if new_seed >= 0x0100:
            new_seed += 1
        null2 = 0xFF & (0x0100 - (new_seed + (new_sig >> 8)))

        return null1<<8|null2

    sig = START_SIG
    for byte in msg:
        sig = do_sig(sig, byte)
    return end_sig(sig)

def new_msg(cmd):
    msg = dcp_msg()
    msg.append(DCP_CLASS)
    msg.append(cmd)
    msg.add_tranno() # tranno
    msg.add_short(0) # security code
    return msg

# API
def get_settings_frame(settings): # [{setting},]
    msg = new_msg(GetSettings)
    ids = [setting.id for setting in settings]
    msg.add_short(min(ids))
    msg.add_short(max(ids) + 1)
    msg.add_short(get_signature(msg))
    return encode(msg)

def set_settings_frame(pairs): # [{setting,value},]
    msg = new_msg(SetSettings)
    for setting,value in zip(pairs[0::2],pairs[1::2]):
        msg.add_short(setting.id)
        msg.add_short(setting.length)
        msg.add_value(value, setting.length)

    msg.add_short(get_signature(msg))
    return encode(msg)

# communications
def read_frame(port):
    frame = bytearray(port.read())
    frame.extend(port.read(port.inWaiting()))
    return frame

def dcp_out(port, frame):
    if port:
        read_frame(port) # remove any previous replies
        port.write(frame)

'''
    class response(bytearray):
        def decode(self):
            self.outcome = self[3]
            self.devicetype = self[4] * 0x100 + self[5]
            self.major = self[6]
            self.minor = self[7]
            self.settings = dict()
            tupples = self[9:-2]
            while tupples:
                id = tupples.pop(0) * 0x100 + tupples.pop(0)
                length = (0x3F & tupples.pop(0)) * 0x100 + tupples.pop(0)
                result.settings[settings.get(id, id)] = int.from_bytes(tupples[:length],'big')
                tupples = tupples[length:]

    result = response(get_response(port))
    result.decode()
'''
def get_response(port, t=1):
    if port:
        time.sleep(t)
        response = dequote(deframe(read_frame(port)))
        if get_signature(response) == 0:
            return response
    return bytes()

# commands
CommitExit = 1
LoadOs = 5
CancelExit = 2
RefreshOnly = 4

# responses
BeCalm = 6
SessionEnding = 3

def control_msg(port, command, t=.1):
    msg = new_msg(Control)
    msg.append(command)
    msg.add_short(get_signature(msg))
    dcp_out(port, encode(msg))
    class response(packet):
        def extras(self):
            self.status = self[3] if len(self) > 3 else 0
    return response(get_response(port, t))

def cancel_exit(port):
    return control_msg(port, CancelExit)

'''DevCo 1645859454.363:
 BD F2 13 91 00 00 02 59 B5 BD
Sync: BD
Class: F2
Type: 13 Cmd: Control
Tranno: 91
 securitycode: 0000
 command: Cancel, Exit
Checksum: 59B5
Sync: BD
'''
def load_os(port):
    return control_msg(port, LoadOs)
''' BD F2 13 92 00 00 05 36 A6 BD
Sync: BD
Class: F2
Type: 13 Cmd: Control
Tranno: 92
 securitycode: 0000
 command: Load OS
Checksum: 36A6
Sync: BD
'''

def commit_exit(port):
    return control_msg(port, CommitExit)

def refresh_only(port):
    return control_msg(port, RefreshOnly)

''' BD F2 13 9C 00 00 01 1B 32 BD
Sync: BD
Class: F2
Type: 13 Cmd: Control
Tranno: 9C
 securitycode: 0000
 command: Commit, Exit
Checksum: 1B32
Sync: BD
'''

def get_settings(port, choices):
    dcp_out(port, get_settings_frame(choices))
    class response(packet):
        def extras(self):
            self.outcome = self[3]
            self.devicetype = self[4] * 0x100 + self[5]
            self.major = self[6]
            self.minor = self[7]
            self.settings = dict()
            tupples = self[9:-2]
            while tupples:
                id = tupples.pop(0) * 0x100 + tupples.pop(0)
                length = (0x3F & tupples.pop(0)) * 0x100 + tupples.pop(0)
                self.settings[settings.get(id, id)] = int.from_bytes(tupples[:length],'big')
                tupples = tupples[length:]
    return response(get_response(port))

def set_settings(port, settings):
    class response(packet):
        def extras(self):
            self.settings = dict()
            if len(self) < 4:
                self.outcome = 0
                return
            self.outcome = self[3]
            tupples = self[4:-2]
            while tupples:
                id = tupples.pop(0) * 0x100 + tupples.pop(0)
                value = tupples.pop(0)
                self.settings[id] = value

    dcp_out(port, set_settings_frame(settings))
    return response(get_response(port))

def as_float(xxxx):
    return struct.unpack('!f', xxxx)[0]

def as_unsigned(xxxx):
    l = len(xxxx)
    f = '!I' if l == 4 else '!H' if l == 2 else 'B'
    return struct.unpack(f, xxxx)[0]

def as_signed(xxxx):
    l = len(xxxx)
    f = '!i' if l == 4 else '!h' if l == 2 else 'b'
    return struct.unpack(f, xxxx)[0]

def float_hex(f):
    return struct.pack('!f', f)

# Test
if __name__ == "__main__":
    devco = bytearray(b'\xBD\xF2\x13\x9A\x00\x00\x04\x4F\x47\xBD')
    al200 = bytearray(b'\xBD\xF2\x93\x9A\x06\xBA\x43\xBD')
    al200a = bytearray(b'\xBD\xF2\x93\x9A')
    al200b = bytearray(b'\x06\xBA\x43\xBD')
    al200c = bytearray(b'\xBD\xF2\x8F\xA2\x01\x00\x2F\x02\x01\x00\x00\xB9\x40\x10\x44\x61\x74\x65\x3A\x20\x20\x20\x20\x54\x69\x6D\x65\x3A\x20\x00\xC9\xE2\xBD')
    al200d = bytearray(b'\xBD\xF2\x10\xA6\x00\x00\x00\xC3\x00\x02\x00\x50\xE0\x8D\xBD')
    al200e = bytearray(b'\xBD\xF2\x0F\xA5\x00\x00\x01\x64\x01\x68\xC5\xFC\xBD')
    al200f = bytearray(b'\xBD\xF2\x90\x83\x01\x00\x2F\x02\x01\x00\x00\xC3\x00\x02\x00\x3C\xF2\x58\xBD')
    al200g = bytearray.fromhex('BD F2 90 C3 01 00 D7 01 21 DF BD'.strip())
    # print(decode_dcp(devco))
    # print(decode_dcp(al200))
    # print(decode_dcp(al200a))
    # print(decode_dcp(al200b))
    # print(decode_dcp(al200b))
    # print(decode_dcp(al200b))
    # print(decode_dcp(al200b))
    # print(decode_dcp(al200c))
    # print(decode_dcp(al200d))
    # print(decode_dcp(al200e))
    # print(decode_dcp(al200g))
    # print(decode_dcp(bytearray.fromhex('BD F2 8F 39 01 00 6A 07 00 00 00 B9 40 15 20 32 30 32 34 2D 31 31 2D 30 35 20 31 30 3A 33 32 3A 34 30 00 33 F3 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 0F 3A 00 00 00 A4 00 A5 9D 76 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 8F 3A 01 00 6A 07 00 00 00 A5 00 01 00 00 A4 00 04 41 8B 5A 97 84 76 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 0F 3B 00 00 00 A7 00 A8 DA BA BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 8F 3B 01 00 6A 07 00 00 00 A7 40 04 00 00 00 00 00 A8 00 04 00 00 00 00 7D 57 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 0F 3C 00 00 00 B9 00 BA 43 A4 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 8F 3C 01 00 6A 07 00 00 00 B9 40 15 20 32 30 32 34 2D 31 31 2D 30 35 20 31 30 3A 33 32 3A 34 30 00 6A E6 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 10 3D 00 00 00 32 00 01 07 E8 94 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 90 3D 01 00 32 03 1B 63 BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 13 3E 00 00 01 C9 9D BD'.strip())))
    # print(decode_dcp(bytearray.fromhex('BD F2 93 3E 01 00 01 D9 24 BD'.strip())))
    # m = 'BD F2 13 00 00 00 04 CE 84 BD BD F2 93 00 06 00 04 9E F0 BD BD F2 0F 81 00 00 E8 6E BD BD F2 8F 81 01 00 6A 07 00 01 00 01 40 18 41 4C 32 30 30 58 2E 41 4C 45 52 54 32 2E 37 2E 42 65 74 61 2D 32 38 00 00 2D 00 01 04 00 2E 40 24 49 4E 44 20 6F 6E 20 63 6F 6D 31 2C 20 44 43 50 20 6F 6E 20 75 73 62 2C 20 43 4C 49 20 6F 6E 20 75 73 62 00 00 2F 00 01 00 00 32 00 01 07 00 3C 00 01 01 00 3D 00 01 00 00 5F 00 02 03 E8 00 64 00 02 00 01 00 69 00 01 01 00 6E 00 01 00 00 82 00 01 01 00 98 00 02 00 00 00 9B 00 02 3A 98 00 9C 00 01 00 00 9D 00 01 01 00 9E 00 01 00 00 A0 00 02 03 E8 00 A2 00 02 00 19 00 A4 00 02 C2 2B 00 A5 00 01 00 00 A6 00 01 00 00 A7 40 02 00 00 00 A8 00 02 00 00 00 A9 40 1C 0A 4E 6F 20 61 63 74 69 76 65 20 6F 72 20 70 65 6E 64 69 6E 67 20 6B 65 79 73 2E 00 00 AA 00 02 00 1E 00 AC 00 01 00 00 AE 00 01 00 00 AF 00 02 00 05 00 B9 40 15 20 32 30 32 34 2D 31 31 2D 31 39 20 30 39 3A 35 30 3A 32 38 00 00 BB 00 01 12 00 BE 00 02 00 05 00 C3 00 02 00 37 00 C8 00 02 00 05 00 CD 00 01 00 00 D2 00 02 01 90 00 D7 00 01 00 00 DC 00 02 02 EE 01 65 00 01 00 01 67 00 01 00 D5 3A BD BD F2 0F 82 00 00 81 67 C9 B7 BD BD F2 8F 82 01 00 6A 07 00 01 01 68 83 AE 56 57 43 5F 30 35 63 6D 00 0B 01 30 4D 31 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 31 30 63 6D 00 0C 01 30 4D 32 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 32 30 63 6D 00 0D 01 30 4D 33 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 33 30 63 6D 00 0E 01 30 4D 34 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 34 30 63 6D 00 0F 01 30 4D 35 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 35 30 63 6D 00 10 01 30 4D 36 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 30 35 63 6D 00 15 01 30 4D 31 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 31 30 63 6D 00 16 01 30 4D 32 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 32 30 63 6D 00 17 01 30 4D 33 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 33 30 63 6D 00 18 01 30 4D 34 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 34 30 63 6D 00 19 01 30 4D 35 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 35 30 63 6D 00 1A 01 30 4D 36 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 30 35 63 6D 00 1F 01 30 4D 31 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 31 30 63 6D 00 20 01 30 4D 32 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 32 30 63 6D 00 21 01 30 4D 33 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 33 30 63 6D 00 22 01 30 4D 34 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 34 30 63 6D 00 23 01 30 4D 35 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 35 30 63 6D 00 24 01 30 4D 36 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 30 35 63 6D 00 29 01 30 4D 31 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 31 30 63 6D 00 2A 01 30 4D 32 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 4D 50 BD BD F2 0F 83 00 00 81 68 81 99 BD BD F2 8F 83 01 00 6A 07 00 00 01 69 40 00 D8 E8 BD BD F2 11 84 00 00 01 68 00 00 03 AE 8A A8 BD BD F2 91 84 01 01 92 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 33 30 63 6D 00 2C 01 30 4D 34 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 34 30 63 6D 00 2D 01 30 4D 35 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 35 30 63 6D 00 2E 01 30 4D 36 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 74 65 6D 70 00 08 07 74 65 6D 70 65 72 61 74 75 72 65 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 63 6C 6F 63 6B 00 84 07 63 6C 6F 63 6B 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 73 74 61 74 75 73 00 CA 07 73 74 61 74 75 73 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 72 61 69 6E 00 00 06 63 6C 6F 73 65 73 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 CF EC BD BD F2 0F 85 00 00 00 B9 00 BA EA 09 BD BD F2 8F 85 01 00 6A 07 00 00 00 B9 40 15 20 32 30 32 34 2D 31 31 2D 31 39 20 30 39 3A 35 30 3A 32 38 00 F0 96 BD BD F2 0F 86 00 00 01 69 01 6A 8E 31 BD BD F2 8F 86 01 00 6A 07 00 00 01 69 40 00 55 02 BD BD F2 13 87 00 00 04 74 2A BD BD F2 93 87 06 00 04 45 96 BD BD F2 10 88 00 00 01 68 83 D4 62 6C 61 68 62 6C 61 68 00 0B 01 30 4D 31 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 31 30 63 6D 00 0C 01 30 4D 32 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 32 30 63 6D 00 0D 01 30 4D 33 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 33 30 63 6D 00 0E 01 30 4D 34 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 34 30 63 6D 00 0F 01 30 4D 35 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 35 30 63 6D 00 10 01 30 4D 36 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 30 35 63 6D 00 15 01 30 4D 31 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 31 30 63 6D 00 16 01 30 4D 32 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 32 30 63 6D 00 17 01 30 4D 33 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 33 30 63 6D 00 18 01 30 4D 34 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 34 30 63 6D 00 19 01 30 4D 35 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 35 30 63 6D 00 1A 01 30 4D 36 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 30 35 63 6D 00 1F 01 30 4D 31 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 31 30 63 6D 00 20 01 30 4D 32 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 32 30 63 6D 00 21 01 30 4D 33 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 33 30 63 6D 00 22 01 30 4D 34 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 34 30 63 6D 00 23 01 30 4D 35 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 35 30 63 6D 00 24 01 30 4D 36 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 30 35 63 6D 00 29 01 30 4D 31 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 31 30 63 6D 00 2A 01 30 4D 32 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 12 9D BD BD F2 90 88 01 01 68 69 94 BD BD F2 12 89 00 00 01 68 00 00 03 D4 01 6C 00 53 63 61 6E 00 45 43 5F 33 30 63 6D 00 2C 01 30 4D 34 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 34 30 63 6D 00 2D 01 30 4D 35 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 35 30 63 6D 00 2E 01 30 4D 36 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 74 65 6D 70 00 08 07 74 65 6D 70 65 72 61 74 75 72 65 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 63 6C 6F 63 6B 00 84 07 63 6C 6F 63 6B 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 73 74 61 74 75 73 00 CA 07 73 74 61 74 75 73 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 72 61 69 6E 00 00 06 63 6C 6F 73 65 73 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 B9 74 BD BD F2 92 89 01 25 6F BD BD F2 13 8A 00 00 01 23 09 BD BD F2 93 8A 01 00 01 30 8E BD'
    # dcp = bytearray.fromhex(m.strip())
    # print_dcp(dcp)
    # dcp = bytearray.fromhex('BD F2 90 8E 01 01 68 01 BE B9 BD BD F2 12 8F 00 00 01 68 00 00 03 D4 00 6D 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 70 32 00 00 01 6C 65 76 65 6C 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 B5 CF BD BD F2 12 8F 00 00 01 68 00 00 03 D4 00 6D 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 70 32 00 00 01 6C 65 76 65 6C 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 B5 CF BD BD F2 12 8F 00 00 01 68 00 00 03 D4 00 6D 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 70 32 00 00 01 6C 65 76 65 6C 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 B5 CF BD BD F2 12 8F 00 00 01 68 00 00 03 D4 00 6D 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 62 61 74 74 65 72 79 00 83 07 62 61 74 74 65 72 79 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 70 32 00 00 01 6C 65 76 65 6C 00 00 00 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 B5 CF BD'.strip())
    # print_dcp(dcp)


if __name__ == "xx__main__":
    dcp = serial.Serial('COM34', baudrate=57600, timeout=0.3)
    pdu = b'\x12\x34\x56\x78\xBD\xBC'
    frame = dcp_msg()
    frame.extend(pdu)
    frame.add_short(get_signature(frame))
    encoded = encode(frame)
    deframed = deframe(encoded)
    decoded = dequote(deframed)
    print(frame, encoded, decoded, deframed)
    print(dequote(deframe(encoded)))
    print("encode:","Pass" if frame == decoded else "Fail")
    # print("Sig:", get_signature((deframe(b'\xBD\xF2\x13\x9A\x00\x00\x04\x4F\x47\xBD'))))
    # pdu = dequote(deframe(b'\xBD\xF2\x13\x9A\x00\x00\x04\x4F\x47\xBD'))
    # print(hx4("Getsig: ", get_signature(pdu[:-2])), '4F47')
    sig = get_signature(decoded)
    print("signat:","Pass" if sig == 0 else hx4("Fail",sig))

    # frame = set_settings_frame([C1_Mode, 0, P1_Enable, 0, SE1_Mode, 0])
    # print(frame)
    # print(decode_dcp(frame))
    #
    # frame = get_settings_frame([C1_Mode, P1_Enable, SE1_Mode])
    # print(frame)
    # print(decode_dcp(frame))
    #
    # frame = get_settings_frame([C1_Status, P1_Transmitted, TBR_Accumulator])
    # print(frame)
    # print(decode_dcp(frame))

    set_settings(dcp, [SW12_Warm_Up_Time, 2, P1_Enable, 1, SE1_Multiplier, 1.0])
    print('Test get settings')
    result = get_settings(dcp, [SE1_Multiplier, SE1_Sensor_ID, SW12_Warm_Up_Time])
    print('SE1_Multiplier', as_float(result.settings[SE1_Multiplier.id]))
    print('SE1_Sensor_ID', as_unsigned(result.settings[SE1_Sensor_ID.id]))
    print('SW12_Warm_Up_Time', as_signed(result.settings[SW12_Warm_Up_Time.id]))

    print('\nTest set settings')
    result = set_settings(dcp, [SW12_Warm_Up_Time, 4, P1_Enable, 0, SE1_Multiplier, 2.0])
    setout = ['','set','not recognized','malformed','read only','no memory']
    for set,out, in result.settings.items():
        print(settings[set], setout[out])

    pdu = b'\x12\x34\x56\x78\xBD\xBC'
    print(dequote(deframe(encode(dcp_msg(pdu)))))

    sys.exit(0)
