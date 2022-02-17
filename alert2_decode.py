if __name__ == "__main__":
    from tlv_types import p as parms, c as cw
    from tlv_types_blue_water import d as bw
else:
    from .tlv_types import p as parms, c as cw
    from .tlv_types_blue_water import d as bw
import numpy as np
import sys, traceback
from protocols.utilities import *

header = b'AL22b'

cp = dict(cw)
cp.update(parms)

class checkAlert2():
    def __init__(self):
        self.flow = bytearray()
        self.times = []

    def __call__(self, start, end, text):
        self.flow += text
        step = (end - start) / len(text)
        tstamp = [int(t) for t in np.arange(start, end, step)] if step else [start]
        self.times += tstamp
        # print ('Check:', start, end, text, tstamp)

        report = ''
        query = header
        qlength = len(query)
        # print(query, text)
        while len(self.flow) >= qlength + 2: # check for header and 2byte length
            index = self.flow.find(query)
            if index == 0: # found beginning of frame at beginning
                pdu, length = xnum_bin(self.flow[qlength:])
                if length == 0:
                    report += '0[zero length frame] '
                elif len(pdu) < length:
                    return 0,0 # there is no frame yet
                # print('pdu,len',pdu, length)
                else:
                    report += decode(pdu[:length])
                self.flow = pdu[length:]
            elif index > 0: # remove stuff before frame
                report += self.flow[:index].decode('utf-8', 'replace')
                self.flow = self.flow[index:]
            else:
                print("no frame header detected")
                return 0,0
            start = self.times[0]
            self.times = self.times[:len(self.flow)]
        return report, start

# utility
def isAscii(c):
    return ' ' <= c <= '~'

def toHex(c):
    return '<' + hex(ord(c))[2:] + '>'

def asciify(s):
    return ''.join([c if isAscii(c) else toHex(c) for c in s])

# decoders
def xnum_bin(pdu):  # return 7 bit number or 15 bit number if first bit is high; plus remaining
    if pdu[0] & 0x80:
        return (pdu[2:], ((pdu[0] & 0x7F) << 8) + pdu[1])
    return pdu[1:], pdu[0]


def decode_tlv(tlv, d):
    rest, type = xnum_bin(tlv)
    defn = d.get(type, '--')
    if rest:
        rest, tlv_length = xnum_bin(rest)
        value = value_decode(type, rest[:tlv_length])
        report = '{:0>2x}{{{}}} {}[{}]'.format(type, defn, tlv_length, value)
        return report, rest[tlv_length:]
    report = '{:0>2X}{{{}}}'.format(type, defn)
    return report,[]

def decode(flow):
    n = len(flow)
    if n < 2:
        report = "too short to decode:" + ''.join(map(lambda x: hex(x)[2:], flow))
    else:
        report, flow = decode_tlv(flow, cp)
        while flow:
            text, flow = decode_tlv(flow, cp)
            report += '\n\t' + text
    return '{}[{}]'.format(n, report)

# decodes
def value_decode(type, pdu):
    try:
        return v.get(type, hex_by2)(pdu)
    except Exception as e:
        print('type: ',type, '  pdu: ', pdu)
        print(e)
        traceback.print_exc(file=sys.stderr)
        return 'decode error'

def knit(hstring, fill):
    return fill.join('{:02X}'.format(x) for x in hstring)

def hex_by2(wool):
    return knit(wool, ' ')

def decimal(wool):
    if wool:
        n = 0
        for i in range(len(wool)):
            n = (n << 8) + wool[i]
        return '%i'%n
    return ''

def twolong(wool):
    out = ''
    out += decimal(wool[:4])
    return out + ' ' + decimal(wool[4:])

def abled(wool):
    return 'Enabled' if wool[0] else 'Disabled'

def boolean(wool):
    return 'True' if wool[0] else 'False'

def string(wool):
    return hexscii(wool)

def setparams(wool):
    report = ''
    while wool:
        text, wool = decode_tlv(wool, parms)
        report += text
    return report

def getparams(wool):
    out = ''
    while wool:
        wool, type = xnum_bin(wool)
        out += ''.join('{:0>2X}{{{}}}'.format(type, parms.get(type, '--')))
    return out
# decoders
# need to protect against bad decoding and then remove data still in stream
def xnum_hex(pdu): # return 7 bit number or 15 bit number if first bit is high; plus remainder
    num = int(pdu[:2], 16)
    if num & 0x80:
        num = ((num&0x7F)<<8) + int(pdu[2:4], 16)
        return (pdu[4:], num)
    return (pdu[2:], num)

def xnumba(pdu): # return 7 bit number or 15 bit number if first bit is high; plus remainder; bytearray
    if pdu:
        num = pdu.pop(0)
        if num & 0x80 and pdu:
            num = ((num&0x7F)<<8) + pdu.pop(0)
            return (pdu, num)
        return (pdu, num)
    return (pdu,None)

def nvalue(pdu): # return count prefixed value and leftover pdu
    pdu, length = xnumba(pdu)
    n = 0
    for i in range(length):
        n = (n << 8) + pdu.pop(0) if pdu else n
    return (pdu, n)


# value decoders by type
v = {}

# table generated code:
# value definitions
v[0] = lambda wool : 'Application PDU{' + hex_by2(wool) + '}'
v[10] = setparams
v[11] = getparams
v[24] = decimal
v[25] = decimal
v[26] = abled
v[27] = boolean
v[30] = boolean
v[32] = abled
v[40] = abled
v[49] = decimal
v[50] = abled
v[51] = lambda s: ["Pass", "Reject"][ord(s)] if ord(s) < 2 else ord(s)
v[52] = decimal
v[53] = decimal
v[54] = decimal
v[55] = decimal
v[56] = decimal
v[58] = boolean
v[63] = abled
v[64] = decimal
v[65] = boolean
v[66] = decimal
v[67] = decimal
v[72] = decimal
v[74] = decimal
v[75] = decimal
v[76] = decimal
v[77] = decimal
v[78] = decimal
v[79] = boolean
v[81] = lambda s: ["Drop", "Overrun"][ord(s)] if ord(s) < 2 else ord(s)
v[82] = decimal
v[96] = decimal
v[97] = decimal
v[98] = decimal
v[99] = boolean
v[100] = decimal
v[101] = boolean
v[102] = decimal
v[104] = decimal
v[117] = decimal
v[119] = string
v[120] = decimal
v[121] = decimal
v[122] = decimal
v[123] = decimal
v[124] = twolong
v[125] = decimal
v[126] = decimal
v[127] = decimal
v[130] = boolean
v[131] = decimal
v[132] = decimal
v[133] = string
v[134] = decimal
v[135] = decimal
v[136] = decimal
v[150] = string
v[4096] = decimal
v[1001] = lambda s: ['None', 'Odd', 'Even'][ord(s)] if ord(s) < 3 else ord(s)
v[4098] = decimal
v[4099] = lambda s: ['None', 'Hardware', 'Software'][ord(s)] if ord(s) < 3 else ord(s)
v[4102] = decimal
v[4103] = decimal
v[4104] = lambda s: ['API', 'ALERT Concentration'][ord(s)] if ord(s) < 2 else ord(s)
v[4105] = boolean
v[4106] = decimal
v[4107] = decimal
v[4113] = string
v[4114] = string
v[4115] = string
v[4116] = string
v[4117] = decimal
v[4118] = string
v[4119] = string
v[4120] = string
v[4121] = string
v[4122] = string
v[4123] = string


if __name__ == "__main__":
    def tsend(time, nchars):
        baud = 57600
        bittime = 1/baud
        chartime = (1 + 8 + 1) * bittime
        return time + chartime * nchars

    def test(frame):
        if type(frame) == type(''):
            frame = bytes.fromhex(frame)
        print('@@@ ',check(time.time()*1000, tsend(time.time(),len(frame)), frame))

    import time
    check = checkAlert2()
    test('414C323262035201B2')
    test('414C32326222002070071DFFF461003C800B453441E2F5C241E30A3D41E2F5C241E2F5C241E30A3D')
    test('414C3232622E002C700729FFF461003CF80B453441E31EB841E31EB841E3333341E3333341E35C2941E347AE41E370A441E39999')
    test(b'AL22b\x00')
    test('414C323262035201B2')
    test('414C323262017C')
    test('414C323262035201B2')
    test('414C32326219001770020A0114000000682015100201081212032413220276')
    test('41 4C 32 32 62 04 0B 02 80 96')
