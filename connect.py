import socket
import sys
from time import sleep, time

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    print('BIND:', (socket.gethostname(), 1234))
    s.listen(5)
    HEADERSIZE = 10
    while True:
        msg = 'CONNECTED :)!'
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        print('waiting')
        clientS, address = s.accept()
        # print('CLIENT ADDRESS:', address)
        # print('SENDING MESSAGE', msg)
        print('accepted')
        res = clientS.recv(256)
        print('RECEIVED:', res)
        bs = bytearray()
        bs.append(0)
        clientS.send(b"sent")
        print('sent', b"sent")
        sleep(1)
        break
        # try:
        #     while True:
        #         sleep(3)
        #         msg = f'TIME IS {time()} :)!'
        #         msg = f'{len(msg):<{HEADERSIZE}}' + msg
        #         print('SENDING MESSAGE', msg)
        #         clientS.send(bytes(msg, "utf-8"))
        # except ConnectionResetError:
        #     print('CONNECTION WAS NOT FOUND AT TIME:', time())
