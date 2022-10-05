import sys
from BizNetwork import BizNetwork
from Generation import Generation
from SaveManager import SaveManager
import numpy as np


if __name__ == '__main__':
    print('loading networks')
    networks = SaveManager().parseNetworks()
    print('loaded')
    gen = Generation(networks, populationMult=10)
    while True:
        try:
            gen.mutate()
            gen.testGen()
        except KeyboardInterrupt:
            break
    print('saving')
    SaveManager().saveNetworks([gen.species[0]])
    print('saved')
