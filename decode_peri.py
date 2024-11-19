import struct, sys
from io import StringIO

m = '62 6C 61 68 62 6C 61 68 00 0B 01 30 4D 31 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 31 30 63 6D 00 0C 01 30 4D 32 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 32 30 63 6D 00 0D 01 30 4D 33 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 33 30 63 6D 00 0E 01 30 4D 34 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 34 30 63 6D 00 0F 01 30 4D 35 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 56 57 43 5F 35 30 63 6D 00 10 01 30 4D 36 21 00 01 FF 01 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 30 35 63 6D 00 15 01 30 4D 31 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 31 30 63 6D 00 16 01 30 4D 32 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 32 30 63 6D 00 17 01 30 4D 33 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 33 30 63 6D 00 18 01 30 4D 34 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 34 30 63 6D 00 19 01 30 4D 35 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 50 65 72 6D 5F 35 30 63 6D 00 1A 01 30 4D 36 21 00 01 FF 02 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 30 35 63 6D 00 1F 01 30 4D 31 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 31 30 63 6D 00 20 01 30 4D 32 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 32 30 63 6D 00 21 01 30 4D 33 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 33 30 63 6D 00 22 01 30 4D 34 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 34 30 63 6D 00 23 01 30 4D 35 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 54 43 5F 35 30 63 6D 00 24 01 30 4D 36 21 00 01 FF 03 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 30 35 63 6D 00 29 01 30 4D 31 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 31 30 63 6D 00 2A 01 30 4D 32 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 00 53 63 61 6E 00 45 43 5F 32 30 63 6D 00 2B 01 30 4D 33 21 00 01 FF 04 3F 80 00 00 00 00 00 00 53 6C 6F 74 00 53 63 61 6E 00 00 00 '
m = bytearray.fromhex(m.strip())
print(m)

def string0():
    s = 'None'
    if m:
        if m[0]:
            s = ''
            while m and m[0] != 0:
                s += '%c' % m.pop(0)
        m.pop(0)
    return s

def string(id=''):
    name = string0()
    if id:
        print(id+": ", end="")
    print(name, end=" ")
    return name

def byte(id=''):
    if id:
        print(id+": ", end="")
        print('0x%02X'%m[0])
    else:
        print('0x%02X ' % m[0], end="")
    m.pop(0)

def n1(id=''):
    if id:
        print(id+": ", end="")
        print(m[0])
        m.pop(0)
    else:
        if m:
            print(m.pop(0), ' ', end="")
        else:
            print(' ', end="")

def port():
    print([" ","C1","C2","C3","COM2","SE1","P1","IND"][m.pop(0)], end=' ')

def float4(id=''): # struct.unpack('>f', struct.pack('>f', 1.0))[0]
    if id:
        print(id+": ", end="")
        print('%f'%struct.unpack('>f', m[0:4])[0])
    else:
        print('%f '%struct.unpack('>f', m[0:4])[0], end="")
    m.pop(0)
    m.pop(0)
    m.pop(0)
    m.pop(0)

def m1(id=''):
    if id:
        print(id+": ", end="")
    if m[0] == 255:
       print('-1 ', end="")
    else:
        print(m[0], ' ', end="")
    m.pop(0)
    if id:
        print('')

def decode_settings(s):
    result = StringIO()
    stdout = sys.stdout
    try:
        sys.stdout = result
        m[:] = s[:]
        while m:
            print('')
            string()
            n1()
            port()
            string()
            n1()
            m1()
            n1()
            float4()
            float4()
            string()
            string()
            n1()
            string()
            n1()
            string()
        sys.stdout = stdout
        return result.getvalue()
    except:
        return ' decode peri error'

if __name__ == "__main__":
    while m:
        if False:
            print('Define:')
            name = string('name')
            n1('id')
            n1('port')
            string('command')
            n1('power')
            m1('warmup')
            n1('item')
            float4('multiplier')
            float4('offset')
            print('Config: ' + name)
            string('Scan')
            string('Report')
            n1('Format')
            string('Event')
            n1('Action')
        else:
            print('\nDefine: ', end="")
            name = string()
            n1()
            port()
            string()
            n1()
            m1()
            n1()
            float4()
            float4()
            print('\nConfig: '+name, end=" ")
            string()
            string()
            n1()
            string()
            n1()
            string()
