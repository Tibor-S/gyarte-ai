
from math import sqrt
import numpy as np
from typing import Callable


class pittsNeuron():
    pheta: float
    weights: list[float]
    g: Callable[[float], float]

    def __init__(
        self,
        pheta: float,
        weights: list[float],
        g: Callable[[float], float]
    ):
        self.pheta = pheta
        self.weights = weights
        self.g = g

    def localField(self, x: list[float]):
        s = sum([self.weights[i] * x[i] for i in range(len(self.weights))])
        return s - self.pheta

    def interact(self, x: list[float]):
        return self.g(self.localField(x))


def sgn(f: float):
    if f == 0:
        return 1.0
    return f / sqrt(f ** 2)


class pittsLayer:
    weights: np.matrix  # m x n där m är antaler neuroner och n är antalet inputs
    thresholds: list[float]  # en threshold per neuron
    g: Callable[[np.matrix], np.matrix]
    learningRate: float

    def __init__(
        self,
        learningRate: float,
        thresholds: list[float],
        weights: np.matrix,
        g: Callable[[np.matrix], np.matrix]
    ):
        self.learningRate = learningRate
        self.thresholds = thresholds
        self.weights = weights
        self.g = g

    def localField(
        self,
        x: np.matrix
    ):  # x: m' x n där m' är antalet input neuroner och n är antaler weights per neuron
        # m x n * n x m' -* t = m x m'
        z = np.subtract(np.matmul(self.weights, x), np.reshape(
            self.thresholds, (len(self.thresholds), 1)))
        return z

    def interact(self, x: np.matrix):
        return self.g(self.localField(x))

    def adjustWeights(self, x: np.matrix, answer: np.matrix):  # x = n  x 1 ans = m x 1
        # print(answer, x.T, self.learningRate * np.matmul(answer, x.T))
        self.weights = np.add(
            self.weights, self.learningRate * np.matmul(answer, x.T))


def sgnM(m: np.matrix):
    mc = m.copy()
    mc[mc >= 0] = 1
    mc[mc < 0] = -1
    return mc


class pittsNetwork:
    layers: list[pittsLayer]
    learningRate: float

    def __init__(
        self,
        learningRate: float,
        thresholds: list[list[float]],
        weights: list[np.matrix],
    ):
        self.learningRate = learningRate
        self.layers = []
        for i in range(len(thresholds)):
            self.layers.append(
                pittsLayer(
                    learningRate,
                    thresholds[i],
                    weights[i],
                    sgnM
                )
            )

    def interact(self, inp: np.matrix):
        z = inp.copy()
        for layer in self.layers:
            z = layer.interact(z)
        return z

    def adjustWeights(self, xs: list[np.matrix], answers: list[np.matrix]):
        for i in range(len(xs)):
            self.layers[i].adjustWeights(xs[i], answers[i])
