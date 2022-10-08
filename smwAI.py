import sys
from BizNetwork import BizNetwork
from Generation import Generation
from SaveManager import SaveManager
import numpy as np


if __name__ == '__main__':
    print('loading networks')
    networks = SaveManager(relPath='two-layer-all-zeros.xml').parseNetworks()
    networks[0].learningRate = 0.1
    print('loaded')
    gen = Generation(networks, populationMult=10)
    while True:
        try:
            gen.mutate(ignoreThreshold=True)
            gen.testGen()
        except:
            print('error')
            break
    print('saving')
    SaveManager(outPath='output.xml').saveNetworks([gen.species[0]])
    print('saved')
