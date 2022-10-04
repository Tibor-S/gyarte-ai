import sys
from BizNetwork import BizNetwork
from SaveManager import SaveManager
import numpy as np


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
            species.bizConnect()
            while alive == 1:
                alive = species.action()
            species.bizDisconnect()
            # print('waiting...')
            # while alive == 0:
            #     alive = species.action()
            print('Next Species')


if __name__ == '__main__':
    print('loading networks')
    networks = SaveManager().parseNetworks()
    print('loaded')
    # networks = [BizNetwork(
    #     0.1,
    #     [
    #         [1 for _ in range(7)],
    #     ],  # 7
    #     [
    #         np.matrix(np.random.rand(7, 169))-0.5
    #     ],  # 7 x 169
    # ) for _ in range(50)]
    # networks = [BizNetwork(
    #     0.1,
    #     [[1 for _ in range(7)]],
    #     [np.matrix(np.zeros((7, 13 ** 2)))]
    # ) for _ in range(10)]
    gen = Generation(networks, populationMult=10)
    gen.testGen()
