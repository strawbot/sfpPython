import io, traceback, sys
from protocols.utilities import asciify

if __name__ == "__main__":
    from airlink import bit_fields
else:
    from .airlink import bit_fields

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

def typify(s,n):
    index = 0x7F & n
    types = {0x0F: 'Get Settings',
             0x10: 'Set Settings',
             0x11: 'Get Fragment',
             0x12: 'Set Fragment',
             0x13: 'Control',
             0x14: 'File Send',
             0x17: 'Discovery'}[index]
    dir = 'Cmd:' if n < 0x7F else 'Rsp:'
    return '{} {} {} {}'.format(s,toHex(n)[1:-1],dir,types)

def to_n(msg):
    n = 0
    for m in msg:
        n = n << 8 | m
    return n


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

ghr = bit_fields([ # get settings response header
    ("outcome", 8),
    ("devicetype", 16),
    ("majorversion", 8),
    ("minorversion", 8),
    ("moresettings", 8)
])

settings = {
1: 'OS Version',
30: 'Battery',
32: 'SE1 Scaled Reading',
33: 'P1 Total',
34: 'C1 Scaled Reading',
35: 'SE1 Raw Reading',
36: 'C1 Raw Reading',
46: 'Port Protocols',
50: 'RS-232 Baud Rate',
55: 'RS-232 Parity',
60: 'RS-232 Stop Bits',
61: 'RS-232 HW Flow Control',
75: 'CS I/O SDC Address',
95: 'Station Source Address',
100: 'Destination Address',
105: 'Path Service Request Enabled',
110: 'Add Destination Address',
130: 'Hop Limit',
155: 'TDMA Frame Length',
156: 'FEC Mode',
157: 'Enable TDMA',
158: 'Center Transmission',
159: 'TDMA Slot Overrun Behavior',
160: 'TDMA Slot Length',
161: 'TDMA Slot Start Offset',
162: 'TDMA Slot Padding',
280: 'TDMA Bytes Remaining',
164: 'Encryption Key Rotation Time',
165: 'Encrypt Outgoing Messages',
166: 'Encryption Set Key',
168: 'Encryption EMID',
169: 'Encryption Key Status',
170: 'GPS Power On Interval',
171: 'Encryption Source Address To Configure',
172: 'Encryption Remove Key',
175: 'GPS On Max',
185: 'Last GPS Fix',
186: 'Tick Lock Loop',
190: 'Carrier Only time',
195: 'AGC time',
200: 'RF Tail Time',
205: 'Invert Modulation',
210: 'Modulation Voltage',
215: 'Radio Power Up Mode',
220: 'Radio Warm Up',
255: 'Multi-Sensor Report',
257: 'Self Report Interval',
260: 'Sensor Scan Interval',
262: 'Configuration Sensor Scan Interval',
265: 'SW12 Warm Up Time',
267: 'Clock Status in Self Report',
268: 'Clock Status Sensor ID',
270: 'P1 Enable',
310: 'SE1 Mode',
312: 'SE1 Sensor ID',
315: 'SE1 Transmitted',
317: 'C1 Transmitted',
325: 'SE1 Multiplier',
330: 'SE1 Offset',
340: 'SE1 Tx Change',
345: 'SDI-12 Command',
346: 'SDI-12 Value to Send',
347: 'C1 Sensor ID',
348: 'SDI-12 Multiplier',
349: 'SDI-12 Offset',
350: 'SDI-12 Tx Change',
355: 'C1 Mode',
356: 'C1 Status',
357: 'P1 Transmitted',
358: 'TBR Accumulator',
}


RESP = 0x80
Control = 0x13
Response = Control + RESP
GetSettings = 0x0F
SetSettings = 0x10
GetSettingsResponse = GetSettings + RESP
SetSettingsResponse = SetSettings + RESP

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
        del(msg[:4])
        out += '    value:' + hexify(msg[:length]) + '\n'
        del (msg[:length])
    return out[:-1]

def ssr_msg(msg):
    out = ' ' + hb(*ghr.outcome(msg)) + '\n'
    del(msg[0])
    while msg:
        id, name = id_name(msg)
        out += '  ' + hx(*so.settingid(msg)) + '(%i) %s\n' % (id, name)
        out += '   ' + hx(*so.settingoutcome(msg)) + '\n'
        del(msg[:3])
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
    return 'Msg:%s'%hexify(msg)

SYNC = 0xBD

def decode_frame(frame):
    f = io.StringIO()
    try:
        print(hx(*h.Sync(frame)), file=f)
        print(hx(*h.Class(frame)), file=f)
        print(typify(*h.Type(frame)), file=f)
        print(hx(*h.Tranno(frame)), file=f)

        head, rest = h.behead(frame)
        msg, tail = t.betail(rest)

        print(decode_msg(h.Type(frame)[1], msg), file=f)
        print(hx(*t.Checksum(tail)), file=f)
        print(hx(*t.Sync(tail)), file=f)
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stderr)
        print("Decode error", file=f)

    a = f.getvalue()
    f.close()
    return a


def dequote(frame):
    QUOTED = 0xBC
    MASKER = 0x20
    out = bytearray()
    quote = False
    for b in frame:
        if b is QUOTED:
            quote = True
        elif quote:
            quote = False
            newb = b - MASKER
            if newb in [SYNC, QUOTED]:
                out.append(newb)
            else:
                print("Error: not a quoted byte %02X"%newb)
                out.append(b)
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
            del(input[0])
            return ''
        end = input[1:].find(bytes([SYNC]))
        if end != -1:
            end += 2
            raw = bytearray(input[:end])
            frame = dequote(raw)
            del(input[:end])
            return '\n' + hexify(raw) + '\n' + decode_frame(frame)
    else:
        start = input.find(bytes([SYNC]))
        if start == -1 and input:
            start = len(input)
        out = asciify(input[:start])
        del(input[:start])
        return out
    return ''

if __name__ == "__main__":
    devco = bytearray(b'\xBD\xF2\x13\x9A\x00\x00\x04\x4F\x47\xBD')
    al200 = bytearray(b'\xBD\xF2\x93\x9A\x06\xBA\x43\xBD')
    al200a = bytearray(b'\xBD\xF2\x93\x9A')
    al200b = bytearray(b'\x06\xBA\x43\xBD')
    al200c = bytearray(b'\xBD\xF2\x8F\xA2\x01\x00\x2F\x02\x01\x00\x00\xB9\x40\x10\x44\x61\x74\x65\x3A\x20\x20\x20\x20\x54\x69\x6D\x65\x3A\x20\x00\xC9\xE2\xBD')
    al200d = bytearray(b'\xBD\xF2\x10\xA6\x00\x00\x00\xC3\x00\x02\x00\x50\xE0\x8D\xBD')
    al200e = bytearray(b'\xBD\xF2\x0F\xA5\x00\x00\x01\x64\x01\x68\xC5\xFC\xBD')
    al200f = bytearray(b'\xBD\xF2\x90\x83\x01\x00\x2F\x02\x01\x00\x00\xC3\x00\x02\x00\x3C\xF2\x58\xBD')
    print(decode_dcp(devco))
    print(decode_dcp(al200))
    print(decode_dcp(al200a))
    print(decode_dcp(al200b))
    print(decode_dcp(al200b))
    print(decode_dcp(al200b))
    print(decode_dcp(al200b))
    print(decode_dcp(al200c))
    print(decode_dcp(al200d))
    print(decode_dcp(al200e))
    print(decode_dcp(al200f))
