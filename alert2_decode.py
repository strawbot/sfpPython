from protocols.tlv_types import d as csi
from protocols.tlv_types_blue_water import d as bw

d = bw
d.update(csi)

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
    return bytearray.fromhex(s).decode('utf-8', 'replace')

# value decoders by type
v = {}

# decodes
def value_decode(type, pdu):
    return v.get(type, hex_by2)(pdu)

def knit(hstring, fill):
    return fill.join('{:02X}'.format(hstring[i]) for i in range(len(hstring)))

def hex_by2(wool):
    return knit(wool, ' ')

def decimal(wool):
    return wool[0]

def abled(wool):
    return 'Enabled' if wool[0] else 'Disabled'

def boolean(wool):
    return 'True' if wool[0] else 'False'

def string(wool):
    return hexscii(wool)

# decoders
def xnum(pdu): # return 7 bit number or 15 bit number if first bit is high; plus remainder
    num = int(pdu[:2], 16)
    if num & 0x80:
        num = ((num&0x7F)<<8) + int(pdu[2:4], 16)
        return (pdu[4:], num)
    return (pdu[2:], num)

class alert1():
    def __init__(self, name, pdu):
        self.pdu = pdu
        self.name = name

    def decode(self):
        return hexscii(self.pdu)

class alert2(alert1):
    query = hexString("ALERT2")
    length = len(query)

    def decode(self): # "414C44525432..."
        if len(self.pdu) == 0:
            return 'empty PDU'
        pdu, type = xnum(self.pdu)
        pdu,tlv_length = xnum(pdu)

        defn = d.get(type,'--')
        value = value_decode(type, pdu)

        return 'ALERT2 {:>2}[ {:0>2x}{} {}[ {} ]]'.format(len(pdu),type,'{'+defn+'}',tlv_length,value)

# value definitions
v[0] = lambda wool : 'Application PDU{'+hex_by2(wool)+'}'
v[24] = decimal
v[25] = decimal
v[26] = abled
v[27] = boolean
v[30] = boolean
v[32] = abled
v[40] = abled
v[49] = decimal
v[50] = abled
v[51] = lambda s: ['Pass','Reject'][int(s)]
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
v[81] = decimal
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
v[118] = decimal
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
v[4097] = lambda s: ['None','Odd','Even'][int(s)]
v[4098] = decimal
v[4099] = lambda s: ['None','Hardware','Software'][int(s)]
v[4102] = decimal
v[4103] = decimal
v[4104] = lambda s: ['API','ALERT Concentration'][int(s)]
v[4105] = boolean
v[4106] = decimal
v[4107] = decimal
v[7000] = boolean
v[7001] = decimal
v[7003] = abled
v[7004] = string
v[7005] = string
v[7006] = string
v[7007] = string
v[7009] = lambda s: ['GPS','NTP','Disabled'][int(s)]
v[7010] = string
v[7011] = string
v[7012] = string
v[7013] = string
v[7014] = decimal
v[7015] = decimal
v[7016] = string
v[7017] = abled
v[7018] = decimal
v[7019] = decimal
v[7020] = decimal
v[7021] = decimal
v[7022] = decimal
v[7023] = decimal
