from Pylibs.protocols.ind_types import *
from Pylibs.protocols.alert2_decode import *

import time

AL22b = [ord(c) for c in 'AL22b']
ALERT2 = [ord(c) for c in 'ALERT2']
ALERT2B = [ord(c) for c in 'ALERT2B']
prefix = AL22b

def alert():
    if prefix == AL22b:
        return 2.0
    if prefix == ALERT2B:
        return 1.1
    if prefix == ALERT2:
        return 1.0

def ind_api(version):
    global prefix
    if version == 1.0:
        prefix = ALERT2
    elif version == 1.1:
        prefix = ALERT2B
    else:
        prefix = AL22b

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

def print_hex_0x(h):
    print(''.join(['0x' + '%02X '% x for x in h]))

def hex_nums(h):
    return ''.join([' %02X'% x for x in h])

# commands
def add_command(command, value=bytearray()):
    frame.extend(make_tlv(command, value))

def set_params(params):
    tlvs = bytearray()
    for p,d in zip(params[0::2],params[1::2]):
        tlvs.extend(make_tlv(p,d))
    if alert() == 2.0:
        add_command(Set_Parameter, tlvs)
    else:
        frame.extend(tlvs)

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

def send_to_ind(port, port2 = None):
    frame[0:0] = bytearray(prefix) + ext(len(frame)) # prepend header
    for port in (port, port2):
        if port:
            read_port(port) # remove any previous replies
            port.write(frame)
    # print(frame.hex())
    del(frame[:])

def get_response(port, t=2):
    time.sleep(t)
    if port: # AL22b length parameter tlvs
        frame = read_port(port)
        if frame[:5] != bytearray(prefix):
            print("Bad Frame: ", frame.hex())
            return []
        frame, frame_length = xnumba(frame[5:])
        params = []
        frame = frame[:frame_length]
        print("Resp: {}".format(hex_nums(frame)))
        while frame:
            frame, type = xnumba(frame)
            if v.get(type, None) == string:  # Evaluate if parameter is string type
                frame, frame_length = xnumba(frame)
                params.append(frame[:frame_length].decode())
                frame = frame[frame_length:]
            else:
                frame, value = nvalue(frame)
                params.append(value)
        return params
    return []

def get_tlv_response(port, t=2):
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
            tlv_count = frame.pop(0)
            for i in range(tlv_count):
               params.append(frame.pop(0))
            return params
    return []

def get_config_response(port, t=2, report=False):
    time.sleep(t)
    if port: # AL22b length parameter tlvs
        frame = read_port(port)
        if frame[:5] != b'AL22b':
            print("Bad Frame: ", frame.hex())
            return []
        frame, frame_length = xnumba(frame[5:])
        if report:
            print(frame.hex())
        if len(frame) != frame_length:
            print("Wrong frame size. Says %i  actual %i"%(frame_length, len(frame)))
            raise()
        params = []
        frame = frame[:frame_length]
        while frame:
            frame, type = xnumba(frame)
            if type == 59:
                continue
            if type == 4108:
                continue
            if v[type] == string:  # Evaluate if parameter is string type
                frame, frame_length = xnumba(frame)
                params.append((type, frame[:frame_length].decode()))
                frame = frame[frame_length:]
                continue
            frame, value = nvalue(frame)
            params.append((type, value))
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
    import  serial
    AL200_CSIO = serial.Serial("/dev/cu.usbserial-143210", baudrate=115200, timeout=1.0)
    AL200_RS232 = serial.Serial("/dev/cu.usbserial-FTGCQG7I", baudrate=57600, timeout=1.0)
    # print_hex(bytearray([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240]))
    # print_hex(make_tlv(Set_Parameter, 128))
    # print_hex(make_tlv(Set_Parameter, 256))
    # print_hex(make_tlv(Set_Parameter, 65536))
    # print_hex(ext(125))
    # print_hex(ext(128))
    # print_hex(ext(0x8081))
    AL200 = AL200_RS232
    # AL200 = AL200_CSIO

    set_params([tdmaframelength,20000])
    send_to_ind(AL200)
    print(req_params(AL200, [tdmaslotlength, tdmaframelength, tdmaslotoffset]))
    # send_to_ind(AL200)
    set_params([tdmaslotlength,1000, tdmaframelength,60000, tdmaslotoffset,30000])
    add_command(Save_Configuration)
    send_to_ind(AL200)
    add_command(Query_Current_Configuration)
    send_to_ind(AL200)
    print(get_response(AL200))
    sys.exit(0)

    AL205B = serial.Serial('/dev/cu.usbserial-1430', baudrate=57600, timeout=1.0)
    ind_api(1.0)

    set_params([tdmaslotlength,1000, tdmaframelength,6000, tdmaslotoffset,3000])
    add_command(Save_Configuration)
    send_to_ind(AL205B)
    add_command(Query_Current_Configuration)
    send_to_ind(AL205B)

