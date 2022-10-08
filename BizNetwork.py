from random import random
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
        port=9999,
        fitnessQuota=100,
        timeQuota=5
    ):
        super().__init__(learningRate, thresholds, weights)
        self.host = host
        self.port = port
        self.timeoutCheck = time()
        self.compareFitness = 0
        self.currentFitness = 0
        self.topFitness = 0
        self.fitnessQuota = fitnessQuota
        self.timeQuota = timeQuota

    def reset(self):
        self.compareFitness = 0
        self.currentFitness = 0
        self.topFitness = 0
        self.timeoutCheck = time()
        return self

    def bizConnect(self):
        self.con = Connect(self.host, self.port)
        self.con.connect()
        return self

    def bizDisconnect(self):
        self.con.disconnect()
        self.con = None
        return self

    def fitness(self, xPos: int, yPos: int):
        return np.sqrt(xPos ** 2 + yPos ** 2)

    def acceptableFitness(self):
        return np.abs(self.currentFitness - self.compareFitness) >= self.fitnessQuota

    def mutate(self, ignoreThreshold=False):
        for lay in self.layers:
            ww, wh = lay.weights.shape
            dWeights = np.matrix(
                (np.random.rand(ww, wh) * 2 - 1) * self.learningRate)
            dThresholds = [(random() * 2 - 1) * self.learningRate
                           for _ in lay.thresholds]

            lay.weights = np.matrix(np.add(
                lay.weights,
                dWeights))
            if not ignoreThreshold:
                lay.thresholds = list(np.add(
                    lay.thresholds,
                    dThresholds))

        return self

    def action(self):
        self.con.awaitConnection()

        # RECEIVE AND FORMAT
        while True:
            try:
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
                break
            except Exception as e:
                print(e)

        # CHECK IF STUCK
        self.currentFitness = self.fitness(xpos, ypos)
        if self.acceptableFitness():
            self.compareFitness = self.currentFitness
            self.timeoutCheck = time()
        elif time() - self.timeoutCheck >= self.timeQuota:
            print('stuck', time() - self.timeoutCheck)
            status = 0

        if self.currentFitness > self.topFitness:
            self.topFitness = self.currentFitness

        output += str(status)
        # print(output)
        self.con.send(output.encode('utf-8'))
        return status
