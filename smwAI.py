from Generation import Generation
from SaveManager import SaveManager


if __name__ == '__main__':
    print('loading networks')
    networks = SaveManager().parseNetworks()
    networks[0].learningRate = 0.5
    print('loaded')
    gen = Generation(networks, populationMult=5)
    while True:
        try:
            gen.mutate()
            gen.testGen()
        except:
            print('error')
            break
    print('saving')
    SaveManager().saveNetworks([gen.species[0]])
    print('saved')
