# utilities
def isAscii(c):
    if type(c) == type('0'):
        c = ord(c)
    return ord(' ') <= c <= ord('~')

def toHex(c):
    if type(c) == type('0'):
        c = ord(c)
    return '<{:02X}>'.format(c)

def asciify(s):
    text = [chr(c) if isAscii(c) else toHex(c) for c in s]
    return ''.join(text)

def hexify(s):
    return ''.join(map(lambda x: ' ' + toHex(x)[1:3], s))

def hexString(s):
    return ''.join(map(lambda x: hex(ord(x))[2:], s))

def hexscii(s):
    if type(s) is type('s'):
        return bytearray.fromhex(s).decode('utf-8', 'replace')
    return s

