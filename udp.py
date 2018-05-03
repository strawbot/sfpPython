# Host UDP server

import socket
import threading

class sockThread(threading.Thread):
    def __init__(self, port, timeout=30):
        threading.Thread.__init__(self)
        self.port = port
        self.name = "Port Thread {}".format(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('',port))
            self.start()
        except:


    def run(self):
        while True:
            try:
                data, address = self.sock.recvfrom(256)  # buffer size is 256 bytes
                print "address:", address, "received message:", data
                self.sock.sendto('Welcome to port:{}\n'.format(address[1]), address)
            except socket.timeout:
                self.sock.close()
                print "Socket:",self.port,"closed"
                break

# Create a UDP socket
def newSock(address, timeout=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.bind(address)
    return sock

address = ('', 1961) # ip,port
sock = newSock(address)

try:
    while True:
        data, address = sock.recvfrom(256)  # buffer size is 256 bytes
        print "address:", address, "received message:", data
        sockThread(address[1])
        sock.sendto('Set up new port:{}'.format(address[1]), address)
except KeyboardInterrupt:
    pass
finally:
    sock.close()

'''
each time a packet comes in on port 1961, it spawns a thread and a new socket assigned to the port that it
came in on. The thread sits and waits for an initial packet and answers it when it comes in. Each port thread
has a timeout and if nothing comes in within that time, then it will timeout and abandon that port.
'''