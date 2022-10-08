from copy import deepcopy
from traceback import print_tb
from BizNetwork import BizNetwork


class Generation:

    def __init__(
        self,
        base: list[BizNetwork],
        generation=1,
        populationMult=10,
    ):
        self.generation = generation
        self.populationMult = populationMult
        self.species: list[BizNetwork] = base.copy()

    def mutate(self, ignoreThreshold=False):
        print('\n')
        print('--MUTATING--')
        base = self.species.copy()
        print(' -BASING NEW GEN ON %d SPECIES' % len(base))
        print(' -FITNESS:')
        for network in base:
            print('  - %d' % network.topFitness)
            network.reset()
            for _ in range(self.populationMult - 1):
                self.species.append(deepcopy(network).mutate(
                    ignoreThreshold=ignoreThreshold).reset())
        print(' -NEW GENERATION HAS %d SPECIES' % len(self.species))
        return self

    def testGen(self):
        def fitness(bn: BizNetwork):
            return bn.topFitness
        print('Testing Gen')

        for species in self.species:
            alive = 1
            species.bizConnect()
            while alive == 1:
                alive = species.action()
            print('Final fitness', species.topFitness)
            species.bizDisconnect()
            print('Next Species')
        self.species.reverse()
        self.species.sort(key=fitness, reverse=True)
        self.species = self.species[:1]  # [:self.populationMult]

        return self
