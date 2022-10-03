from time import time
import numpy as np
from ai import pittsNetwork
from connect import Connect


def format(n: int):
    if n == 2:
        return -1
    elif n == -1:
        return 0
    return n


class BizNetwork(pittsNetwork):

    def __init__(
        self,
        learningRate: float,
        thresholds: list[list[float]],
        weights: list[np.matrix],
        host='localhost',
        port=9999
    ):
        super().__init__(learningRate, thresholds, weights)
        self.con = Connect(host, port)
        self.species = 0
        self.timeoutCheck = time()
        self.comparePos = (0, 0)

    def bizConnect(self):
        self.con.connect()

    def bizDisconnect(self):
        self.con.disconnect()

    def action(self):
        self.con.awaitConnection()

        # RECEIVE AND FORMAT
        bs = self.con.recv().decode('utf-8')
        xpos = int(bs[0:7])
        ypos = int(bs[7:14])
        status = int(bs[14])
        bitmap = np.reshape(
            [format(int(b)) for b in bs[15:]], (len(bs) - 15, 1)
        )
        out = self.interact(bitmap).T
        output = ''.join(
            [str(format(int(o))) for o in np.array(out)[0]]
        )

        # CHECK IF STUCK
        if self.comparePos != (xpos, ypos):
            self.comparePos = (xpos, ypos)
            self.timeoutCheck = time()
        elif time() - self.timeoutCheck >= 5:
            status = 0

        output += str(status)
        print(output)
        self.con.send(output.encode('utf-8'))
        return status
