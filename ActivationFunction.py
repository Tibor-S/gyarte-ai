import numpy as np


class ActivationFunction:

    def func(x: np.matrix):
        return x

    def inverse(x: np.matrix):
        return x

    def derivate(x: np.matrix):
        return x


class Linear(ActivationFunction):

    def func(x: np.matrix):
        xc = x.copy()
        return xc

    def derivative(_: np.matrix):
        return 1


class SoftArgMax(ActivationFunction):

    def func(x: np.matrix):
        div = np.matrix(np.zeros((1, x.shape[1])))
        for i in range(x.shape[0]):
            div = np.add(div, np.power(np.e, x[i, :]))
        return np.matrix(np.divide(np.power(np.e, x), div))

    def derivative(x: np.matrix):
        return SoftArgMax.func(x)


class Logistic(ActivationFunction):

    def func(x: np.matrix):
        return np.matrix(np.divide(1, np.add(1, np.power(np.e, - x))))

    def derivative(x: np.matrix):
        return np.matrix(np.multiply(Logistic.func(x), np.subtract(1, Logistic.func(x))))


class SgnLogistic(ActivationFunction):

    def func(x: np.matrix):
        return np.matrix(np.div(
            np.subtract(1, np.power(np.e, - x)),
            np.add(1, np.power(np.e, - x))))  # 2 * l(x) - 1 => -1 < l(x) < 1

    def derivative(x: np.matrix):
        return np.matrix(np.multiply(2, Logistic.derivate(x)))


class Rectifier:

    def func(x: np.matrix):
        xc = x.copy()
        xc[xc < 0] = 0
        return xc

    def derivative(x: np.matrix):
        xc = x.copy()
        xc[x < 0] = 0
        xc[x >= 0] = 1
        return xc


class ReLU(Rectifier):
    pass


class Sgn(ActivationFunction):

    def func(x: np.matrix):
        xc = x.copy()
        xc[xc >= 0] = 1
        xc[xc < 0] = -1
        return xc

    def derivative(_: np.matrix):
        return 0
