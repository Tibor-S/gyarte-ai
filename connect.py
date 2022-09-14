import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9999))
    print('BIND:', ('localhost', 9999))
    s.listen(1)
    while True:
        # print('waiting')
        clientS, address = s.accept()
        # print('accepted')
        res = clientS.recv(256)
        # print('RECEIVED:', len(res.decode('utf-8')))
        clientS.send(b"0101010")
        # print('sent', b"0101010")
