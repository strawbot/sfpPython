if __name__ == "__main__":
    from tlv_types import d as csi
    from tlv_types_blue_water import d as bw
else:
    from .tlv_types import d as csi
    from .tlv_types_blue_water import d as bw
import numpy as np
import sys, traceback

t = bw
t.update(csi)
header = 'AL22b'

class checkAlert2():
    def __init__(self):
        self.flow = bytearray()
        self.times = []

    def __call__(self, start, end, text):
        self.flow += text
        step = (end - start) / len(text)
        tstamp = [int(t) for t in np.arange(start, end, step)] if step else [start]
        self.times += tstamp
        print ('Check:', start, end, text, tstamp)

        report = ''
        query = bytearray(header, 'utf-8')
        qlength = len(query)
        print(query, text)
        while len(self.flow) >= qlength + 2: # check for header and 2byte length
            index = self.flow.find(query)
            if index == 0: # found beginning of frame at beginning
                pdu, length = xnum_bin(self.flow[qlength:])
                if length == 0 or len(pdu) < length:
                    return 0,0 # there is no frame yet
                print('pdu,len',pdu, length)
                report = decode(pdu[:length])
                self.flow = pdu[length:]
            elif index > 0: # remove stuff before frame
                report = self.flow[:index].decode('utf-8', 'replace')
                self.flow = self.flow[index:]
            else:
                print("no frame header detected")
                return 0,0
            start = self.times[0]
            self.times = self.times[-len(self.flow):]
        return report, start

# utility
def isAscii(c):
    return ' ' <= c <= '~'

def toHex(c):
    return '<' + hex(ord(c))[2:] + '>'

def asciify(s):
    return ''.join([c if isAscii(c) else toHex(c) for c in s])

def hexString(s):
    return ''.join(map(lambda x: hex(ord(x))[2:], s))

def hexscii(s):
    if type(s) is type('s'):
        return bytearray.fromhex(s).decode('utf-8', 'replace')
    return s


# decoders
def xnum_bin(pdu):  # return 7 bit number or 15 bit number if first bit is high; plus remaining
    if pdu[0] & 0x80:
        return (pdu[2:], ((pdu[0] & 0x7F) << 8) + pdu[1])
    return pdu[1:], pdu[0]


def decode_tlv(tlv):
    rest, type = xnum_bin(tlv)
    rest, tlv_length = xnum_bin(rest)
    defn = t.get(type, '--')
    value = value_decode(type, rest[:tlv_length])
    report = '{:0>2x}{{{}}} {}[{}]'.format(type, defn, tlv_length, value)
    return report, rest[tlv_length:]

def decode(flow):
    n = len(flow)
    if n < 2:
        report = "too short to decode:" + ''.join(map(lambda x: hex(x)[2:], flow))
    else:
        report, flow = decode_tlv(flow)
        while flow:
            text, flow = decode_tlv(flow)
            report += ' ' + text
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
        while wool:
            n = (n<<8) + wool.pop(0)
        return '%i'%n
    return ''

def abled(wool):
    return 'Enabled' if wool[0] else 'Disabled'

def boolean(wool):
    return 'True' if wool[0] else 'False'

def string(wool):
    return hexscii(wool)

def setparams(wool):
    report = ''
    while wool:
        text, wool = decode_tlv(wool)
        report += text
    return report

def getparams(wool):
    return ' '.join('{:0>2x}{{{}}}'.format(type, t.get(type, '--')) for type in wool)

# decoders
# need to protect against bad decoding and then remove data still in stream
def xnum_hex(pdu): # return 7 bit number or 15 bit number if first bit is high; plus remainder
    num = int(pdu[:2], 16)
    if num & 0x80:
        num = ((num&0x7F)<<8) + int(pdu[2:4], 16)
        return (pdu[4:], num)
    return (pdu[2:], num)

def xnumba(pdu): # return 7 bit number or 15 bit number if first bit is high; plus remainder; bytearray
    num = pdu.pop(0)
    if num & 0x80:
        num = ((num&0x7F)<<8) + pdu.pop(0)
        return (pdu, num)
    return (pdu, num)

def nvalue(pdu): # return count prefixed value and leftover pdu
    pdu, length = xnumba(pdu)
    n = 0
    for i in range(length):
        n = (n << 8) + pdu.pop(0)
    return pdu, n

class alert1():
    def __init__(self, name, pdu):
        self.pdu = pdu
        self.name = name

    def decode(self):
        return hexscii(self.pdu)

class alert2(alert1):
    query = hexString(header)
    length = len(query)

    def decode(self): # "414C44525432..."
        print (self.pdu)
        if len(self.pdu) == 0:
            return 'empty PDU'
        pdu, type = xnum_hex(self.pdu)
        pdu,tlv_length = xnum_hex(pdu)

        defn = t.get(type,'--')
        value = value_decode(type, pdu)

        return 'ALERT2 {:>2}[ {:0>2x}{} {}[ {} ]]'.format(len(pdu),type,'{'+defn+'}',tlv_length,value)

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
v[124] = decimal
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
    check = checkAlert2()
    test0=bytes.fromhex('414C323262110A0C48022EE04B020BB84A0203')
    test1=b'414C32326222002070071DFFF461003C800B453441E2F5C241E30A3D41E2F5C241E2F5C241E30A3D'
    test2=b'414C3232622E002C700729FFF461003CF80B453441E31EB841E31EB841E3333341E3333341E35C2941E347AE41E370A441E39999'
    report, start = check(0, len(test0), test0)
    print(report)
