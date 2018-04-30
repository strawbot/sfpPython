# Host UDP server

import socket

# Create a UDP socket
def newSock(address, timeout=0.001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.bind(address)
    return sock

ip = '192.168.0.112'
port = 1961
ip = '192.168.2.1'
ip = ''
address = (ip, port)

drawer = []
drawer.append(newSock(address, .1))

try:
    while True:
        i = 0
        while i < len(drawer):
            try:
                sock = drawer[i]
                data, address = sock.recvfrom(256)  # buffer size is 256 bytes
                print "address:", address, "received message:", data
                if i == 0:
                    message = 'This is the welcome message.\n'
                    sock = newSock(('',address[1]))
                    drawer.append(sock)
                    print len(drawer), "socks in drawer"
                else:
                    message = 'This is the final message.\n'
                sock.sendto(message, address)

            except socket.timeout:
                pass
            i += 1

finally:
    for sock in drawer:
        sock.close()

'''
each time a packet comes in on port 1961, it spawns a thread and a new socket assigned to the port that it
came in on. The thread sits and waits for an initial packet and answers it when it comes in. Each port thread
has a timeout and if nothing comes in withing that time, then it will timeout and abandon that port.
'''