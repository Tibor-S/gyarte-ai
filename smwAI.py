from ai import pittsLayer, pittsNetwork, sgnM
import numpy as np
from connect import Connect


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
        # self.learningRate = learningRate

    def action(self):
        self.con.awaitConnection()
        bs = self.con.recv().decode('utf-8')
        print(bs[0])
        bitmap = np.reshape([int(b) for b in bs], (len(bs), 1))
        print(bitmap)
        # output = ''.join([str(o) for o in np.array(self.interact(bitmap).T)])
        output = b'0100101010'
        self.con.send(b"0100300202010021010")


if __name__ == '__main__':
    network = BizNetwork(
        0.1,
        [0],
        [0],
    )

    print(
        network.learningRate,
        network.layers,
    )
    while True:
        network.action()
        break
