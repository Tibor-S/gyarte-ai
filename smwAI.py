from ai import pittsLayer, pittsNetwork, sgnM
import numpy as np
from connect import Connect


def format(n: int):
    if n == 2:
        return -1
    elif n == -1:
        return 2
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
        # self.learningRate = learningRate

    def action(self):
        self.con.awaitConnection()
        bs = self.con.recv().decode('utf-8')
        print(bs)
        # print(bs[0])
        bitmap = np.reshape([format(int(b)) for b in bs], (len(bs), 1))
        # print(bitmap)
        ### input = 169
        out = self.interact(bitmap).T
        ### out = 7
        # print(out)
        output = ''.join(
            [str(int(o)) for o in np.array(out)[0]]
        ).encode('utf-8')
        # print(output)
        # output = '0100101010'.encode('utf-8')
        self.con.send(output)


if __name__ == '__main__':
    network = BizNetwork(
        0.1,
        [
            [1 for _ in range(169)],
            [1 for _ in range(7)],
        ],  # 7
        [
            np.matrix(np.random.rand(169, 169))-.5,
            np.matrix(np.random.rand(7, 169))-.5,
        ],  # 7 x 169
    )

    print(
        network.learningRate,
        network.layers,
    )
    while True:
        network.action()
