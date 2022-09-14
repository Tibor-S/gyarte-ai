import socket


class Connect:

    def __init__(self, host='localhost', port=9999):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        print('BIND:', (host, port))
        s.listen(1)
        self.socket = s

    def awaitConnection(self):
        self.client = self.socket.accept()[0]

    def send(self, mes: bytes):
        self.client.send(mes)

    def recv(self, pkgSize=1024):
        return self.client.recv(pkgSize)


# if __name__ == '__main__':
#     while True:

#         res = clientS.recv(256)
#         clientS.send(b"0101010")
