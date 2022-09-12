from random import random
import socket
from time import sleep

UDP_IP = "localhost"
UDP_PORT = 8888
MESSAGE = b"Hello, World!"

bs = bytearray()
for i in range(257):
    bs.append(int(random() * 3))

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_STREAM)  # UDP
sock.connect((UDP_IP, UDP_PORT))
i = 0
while True:
    i += 1
    sock.send(bytes(i % 256))
    sleep(.1)
    print(i)
    print(sock.recvfrom(256))
