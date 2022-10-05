from copy import deepcopy
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

    def mutate(self):
        base = self.species.copy()
        for network in base:
            for _ in range(self.populationMult - 1):
                self.species.append(deepcopy(network).mutate())
        return self

    def testGen(self):
        def fitness(bn: BizNetwork):
            return bn.currentFitness

        for species in self.species:
            alive = 1
            species.bizConnect()
            while alive == 1:
                alive = species.action()
            print('Final fitness', species.currentFitness)
            species.bizDisconnect()
            print('Next Species')
        self.species.sort(key=fitness, reverse=True)
        self.species = self.species[:self.populationMult]

        return self
