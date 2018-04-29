import socket
import sys
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.19.1', 1961)
message = 'This is the message. It will be repeated.\n'

try:

    # Send data
    # print >>sys.stderr, 'sending "%s"' % message
    print sock.sendto(message, server_address)
#
    # time.sleep(5)
    # # Receive response
    # print >>sys.stderr, 'waiting to receive'
    # data, server = sock.recvfrom(10000)
    # print >>sys.stderr, 'received "%s"' % data

finally:
    # print >>sys.stderr, 'closing socket'
    sock.close()