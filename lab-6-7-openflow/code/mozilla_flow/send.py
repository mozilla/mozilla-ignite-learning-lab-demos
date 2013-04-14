# Mozilla Ignite SDN Learning Lab
# Author: Kenny Katzgrau <katzgrau@gmail.com>
#
# This is a simple script that will send UDP
# packets to port 10002 to a host that is
# specified on the command line.
#
# $ python send.py [ip-address] [message-to-send]
import socket
import sys

UDP_IP = sys.argv[1]
UDP_PORT = 10002
MESSAGE = sys.argv[2]

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "Message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
