from math import floor
from time import time
from typing import Callable
from ai import pittsLayer, pittsNetwork, sgnM
import numpy as np
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


class Generation:

    def __init__(
        self,
        base: list[BizNetwork],
        generation=1,
        populationMult=10,
    ):
        self.generation = generation
        self.populationSize = 0
        self.species: list[BizNetwork] = []
        for network in base:
            for _ in range(populationMult):
                self.populationSize += 1
                self.species.append(network)

    def testGen(self):

        for species in self.species:
            alive = 1
            while alive == 1:
                alive = species.action()
            # print('waiting...')
            # while alive == 0:
            #     alive = species.action()
            print('Next Species')


if __name__ == '__main__':
    while True:
        networks = [BizNetwork(
            0.1,
            [
                [1 for _ in range(169)],
                [1 for _ in range(7)],
            ],  # 7
            [
                np.matrix(np.random.rand(169, 169))-0.5,
                np.matrix(np.random.rand(7, 169))-0.5
            ],  # 7 x 169
        ) for _ in range(50)]
        gen = Generation(networks, populationMult=1)
        gen.testGen()
