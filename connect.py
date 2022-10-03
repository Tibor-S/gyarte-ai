import socket


class Connect:

    def __init__(self, host='localhost', port=9999):
        self.address = (host, port)

    def awaitConnection(self):
        self.client = self.socket.accept()[0]

    def send(self, mes: bytes):
        self.client.send(mes)

    def recv(self, pkgSize=1024):
        return self.client.recv(pkgSize)

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('BIND:', self.address)
        s.bind(self.address)
        s.listen(1)
        self.socket = s

    def disconnect(self):
        self.socket.close()


# if __name__ == '__main__':
#     while True:

#         res = clientS.recv(256)
#         clientS.send(b"0101010")
