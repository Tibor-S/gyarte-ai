import sys
from BizNetwork import BizNetwork
from Generation import Generation
from SaveManager import SaveManager
import numpy as np


if __name__ == '__main__':
    print('loading networks')
    networks = SaveManager(relPath='output.xml').parseNetworks()
    networks[0].learningRate = 0.1
    for lay in networks[0].layers:
        for i in range(len(lay.thresholds)):
            lay.thresholds[i] = 0.5
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
