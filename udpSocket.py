import socket

UDP_IP = "localhost"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_STREAM)  # UDP
sock.connect((UDP_IP, 8888))
print(sock.getsockname())
while True:
    data, addr = sock.recvfrom(256)  # buffer size is 1024 bytes
    bs = bytearray(data)
    for b in bs:
        print("received message: %s" % b)
