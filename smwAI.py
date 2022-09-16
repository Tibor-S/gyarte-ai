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
        self.species = 0
        self.timeoutCheck = time()
        self.comparePos = (0, 0)
        # self.learningRate = learningRate

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
            [str(int(o)) for o in np.array(out)[0]]
        ).encode('utf-8')

        # CHECK IF STUCK
        if self.comparePos != (xpos, ypos):
            self.comparePos = (xpos, ypos)
            self.timeoutCheck = time()
            print('not stuck')
        elif time() - self.timeoutCheck >= 2:
            status = 0
            print('stuck -> dead')
        else:
            print('stuck')

        # Send Actions
        if status == 1:
            self.con.send(output)
        else:
            if floor(time()) % 2 == 0:
                b = '0000100'.encode('utf-8')
            else:
                b = '0000000'.encode('utf-8')
            self.con.send(b)  # skickar endast A
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
            print('waiting...')
            while alive == 0:
                alive = species.action()
            print('Next Species')


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
    gen = Generation([network])
    gen.testGen()
