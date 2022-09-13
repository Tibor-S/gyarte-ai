import socket
from time import sleep

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 1234))
    print('BIND:', ('localhost', 1234))
    s.listen(5)
    print('waiting')
    clientS, address = s.accept()
    print('accepted')
    res = clientS.recv(256)
    print('RECEIVED:', res)
    bs = bytearray()
    bs.append(0)
    clientS.send(b"sent")
    print('sent', b"sent")
    sleep(1)
