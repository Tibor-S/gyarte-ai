from copy import deepcopy
import numpy as np
from ActivationFunction import ActivationFunction, SoftArgMax


class StochasticNetwork:

    def __init__(
        self,
        learningRate: float,
        thresholds: list[list[float]],
        weights: list[np.matrix],
        Acts: list[ActivationFunction]
    ):
        self.learningRate = learningRate
        self.weights = deepcopy(weights)
        self.thresholds = deepcopy(thresholds)
        self.activations = deepcopy(Acts)
        self.size = min(len(weights), len(thresholds), len(Acts))
        self.cost = None
        self.values: list[np.matrix] = []

    def forwardProp(self, inp: np.matrix):
        self.values.clear()
        self.values.append(inp)
        for i in range(self.size):
            z0 = self.values[-1]  # m x n, n är antalet inputs som testas
            w = self.weights[i]  # m' x n'
            t = np.reshape(self.thresholds[i], (w.shape[0], 1))
            activation = self.activations[i]
            # (m' x n') x (m x n) -* (m' x 1) = m' x n -* (m' x 1) = m' x n
            activation.func(z0)
            z1 = activation.func(np.matrix(
                np.subtract(np.matmul(w, z0), t)))

            self.values.append(z1)

        return self

    def backProp(self, answers: np.matrix):
        for i in reversed(range(self.size)):
            if i == self.size - 1:
                z1 = answers
            else:
                z1 = self.values[i+1]
            z0 = self.values[i]
            w = self.weights[i]
            diff = np.array(
                np.mean(self.costGradient(z1 - z0), axis=1)).flatten()
            print('BACK_PROP:')
            print(f' -z1: {z1}')
            print(f' -z0: {z0}')
            print(f' -w: {w}')
            print(f' -diff: {diff}')
            print(f' -w - diff: {w - diff}')
            w = np.matrix(np.subtract(w, diff))

        # for i in range(len(xs)):
        #     self.layers[i].adjustWeights(xs[i], answers[i])

        return self

    def cost(self, vector: np.array):
        # vector should be (target - output)
        return np.divide(np.dot(vector, vector), 2)

    def costGradient(self, vector: np.array):
        return vector  # C = 1/2 * v_i^2 => d_i C = v_i => grad C = v, Changes if cost function changes


if __name__ == '__main__':
    network = StochasticNetwork(
        0.1,
        [
            [0 for _ in range(10)]
        ],
        [
            np.matrix(np.random.rand(10, 2) / 100)
        ],
        [
            SoftArgMax
        ]
    )
    network.forwardProp(np.matrix([[1, 1], [1, 0]])).backProp(
        np.matrix([[1, 1], [1, 1]]))
    print(network.values[1])

    # sample = DigitSample(test=True, randomD=True)
    # inp = np.matrix([np.ndarray.flatten(sample.bitmap)]).T
    # network = StochasticNetwork(
    #     0.1,
    #     [
    #         [0 for _ in range(10)]
    #     ],
    #     [
    #         np.matrix(np.random.rand(10, inp.shape[0]) / 100)
    #     ],
    #     [
    #         act.linear
    #     ]
    # )
    # print(inp.shape)
    # print(network.interact(inp))
