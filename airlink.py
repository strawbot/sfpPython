import io
'''
protocols often use consecutive bits, irrespective of byte boundaries,
called bit fields. This tool allows bit field templates to be used to
encode/decode byte frames.
create templates that can be placed over byte arrays to extract field values
    id = ser.settingid(msg)[1]
        where ser is a 'bitfields instance' with specific fields and names
        also an elemental part of a protocol frame
    the frame is passed in and it is viewed by its bit fields. different
    bitfields templates can apply to same frame
'''
class bit_fields():
    def __init__(self, fields):
        offset = 0
        for field in fields:
            name, span = field
            self.build(name, offset, span)
            offset += span
        self.nbits = offset

    def behead(self, mp):
        index = self.nbits//8
        return mp[:index], mp[index:]

    def betail(self, mp):
        index = -(self.nbits//8)
        return mp[:index], mp[index:]

    def build(self, name, offset, span):
        namec = name+':'
        index = offset//8
        end = offset + span -1
        shift = 7 - (end % 8)
        mask = (1<<span) - 1

        if end//8 == index:
            value = "ba[{}]".format(index)
        else:
            value = "((ba[{}]<<8)+ba[{}])".format(index, index+1) # big endian

        exec("self.{} = lambda ba: ('{}', ({}>>{}) & {})".format(name, namec, value, shift, mask))


def Short(ba):
    return (ba[0] << 8) + ba[1]

mh = bit_fields([ #(name, span)
        ("version", 2),
        ("protocol_id", 3),
        ("ts_service", 1),
        ("add_path_service", 1),
        ("inc_da", 1),

        ("port", 4),
        ("reserved", 3),
        ("ack", 1),

        ("added_header", 1),
        ("hop", 3),
        ("length", 12),

        ("source_address", 16),
        ])

def decode_mant_header(mp):# mp = bytearray([0x07, 0x06, 0x00, 0x10, 0x0D, 0x10])

    f = io.StringIO()

    try:
        print(*mh.version(mp), file=f) # 0
        print(*mh.protocol_id(mp), file=f) # 0
        print(*mh.ts_service(mp), file=f) # 1
        print(*mh.add_path_service(mp), file=f) # 1
        print(*mh.inc_da(mp), file=f) # 0

        print(*mh.port(mp), file=f) # 0
        print(*mh.reserved(mp), file=f) # 0
        print(*mh.ack(mp), file=f) # 0

        print(*mh.added_header(mp), file=f) # 1
        print(*mh.hop(mp), file=f) # 4
        print(*mh.length(mp), file=f) # 3862

        print(*mh.source_address(mp), file=f) # 45502
        # mpx = mh.behead(mp)[1]

        # if (mh.inc_da(mp)):
        #     print("Dest addr:", Short(mpx), file=f)
        #     mpx = mpx[2:]

        # if (mh.protocol_id(mp)):
        #     print("PDU ID:", mpx[0], file=f)
        #     mpx = mpx[1:]

        # if (mh.add_path_service(mp)):
        #     n = mpx[0]
        #     mpx = mpx[1:]
        #     print("Source Addresses:(%d)"%n, file=f)
        #     while n:
        #         print(Short(mpx), file=f)
        #         mpx = mpx[2:]
    except Exception as e:
        print (e)
        print("Decode error", file=f)

    a = f.getvalue()
    f.close()
    return a