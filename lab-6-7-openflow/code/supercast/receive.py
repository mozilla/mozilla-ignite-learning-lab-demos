# Mozilla Ignite SDN Learning Lab
# Author: Kenny Katzgrau <katzgrau@gmail.com>
#
# This is a simple script that will listen on
# port 10002 for UDP requests, and output the 
# UDP payload when they come in
import socket
UDP_IP = "0.0.0.0"
UDP_PORT = 10002

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Received message:", data
