from Pylibs.protocols.ind_types import *
from Pylibs.protocols.alert2_decode import *

import time

AL22b = [0x41, 0x4C, 0x32, 0x32, 0x62]
frame = bytearray()

# tools
def data_bytes(data):
    bigend = bytearray()
    while True:
        bigend.insert(0, data&0xFF)
        data >>= 8
        if data == 0:
            break
    return bigend

def ext(n):
    return bytearray([n])  if  n < 128  else  bytearray([(n>>8)|0x80, n&0xFF])

def make_tlv(tlv_type, data):
    db = data  if  isinstance(data, bytearray)  else  data_bytes(data)
    return ext(tlv_type) + ext(len(db)) + db

def print_hex(h):
    print(''.join([' %02X'% x for x in h]))

# commands
def add_command(command, value=bytearray()):
    frame.extend(make_tlv(command, value))

def set_params(params):
    tlvs = bytearray()
    for p,d in zip(params[0::2],params[1::2]):
        tlvs.extend(make_tlv(p,d))
    add_command(Set_Parameter, tlvs)

def get_params(params):
    ps = bytearray()
    for p in params:
        ps.extend(ext(p))
    add_command(Get_Parameter, ps)

# communications
def read_port(port):
    frame = bytearray(port.read())
    frame.extend(port.read(port.in_waiting))
    return frame

def send_to_ind(port, port_tx=None):
    frame[0:0] = bytearray(AL22b) + ext(len(frame)) # prepend header
    if port:
        read_port(port) # remove any previous replies
        port.write(frame)
    del(frame[:])

def get_response(port, t=2):
    time.sleep(t)
    if port: # AL22b length parameter tlvs
        frame = read_port(port)
        if frame[:5] != b'AL22b':
            print("Bad Frame: ", frame.hex())
            return []
        frame, frame_length = xnumba(frame[5:])
        params = []
        frame = frame[:frame_length]
        while frame:
            frame, type = xnumba(frame)
            if v[type] == string:  # Evaluate if parameter is string type
                frame, frame_length = xnumba(frame)
                params.append(frame.decode())
                return params      # if so just return whole data as is
            frame, value = nvalue(frame)
            params.append(value)
        return params
    return []

def req_params(port, params):
    get_params(params)
    send_to_ind(port)
    resp = get_response(port)
    if resp:
        return resp
    print('retry once: response not good')
    get_params(params)
    send_to_ind(port)
    return get_response(port)


if __name__ == '__main__':
    print_hex(bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240]))
    print_hex(make_tlv(Set_Parameter, 128))
    print_hex(make_tlv(Set_Parameter, 256))
    print_hex(make_tlv(Set_Parameter, 65536))
    print_hex(ext(125))
    print_hex(ext(128))
    print_hex(ext(0x8081))
    set_params([tdmaframelength,257])
    send_to_ind(None)
    get_params([tdmaslotlength, tdmaframelength, tdmaslotoffset])
    send_to_ind(None)
    set_params([tdmaslotlength,1000, tdmaframelength,60000, tdmaslotoffset,30000])
    add_command(Save_Configuration)
    send_to_ind(None)