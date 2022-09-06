import logging
from game import Game
from ai import pittsNetwork
import numpy as np


def main():

    network = pittsNetwork(
        0.5,
        [
            [0]
        ],
        [
            np.matrix([[0, 0, 0]])
        ]

    )
    while True:
        game = Game(10)
        status = 0
        dl = 0
        dr = 0
        try:
            while status == 0:
                game.nextFrame()
                dl = -1
                dr = -1

                d = 0
                for lo, ro in game.gameMap:
                    if dl == -1 and lo == 1:
                        dl = d
                    if dr == -1 and ro == 1:
                        dr = d
                    d += 1
                if dl == -1:
                    dl = d
                if dr == -1:
                    dr = d
                z = network.interact(
                    np.matrix([
                        [game.player],
                        [dl],
                        [dr]
                    ])
                )
                if z[0, 0] == -1:
                    game.moveLeft()
                else:
                    game.moveRight()

                print(z, dl, dr, network.layers[0].weights)
        except Game.Lost as e:
            print(e.__str__())
            answer = np.matrix([[((2 * game.player) - 1)/(-1)]])
            print(answer)
            print([
                np.matrix([
                    [(2 * game.player) - 1],
                    [dl + 1],
                    [dr + 1]
                ])
            ],
                [answer])
            network.adjustWeights(
                [
                    np.matrix([
                        [(2 * game.player) - 1],
                        [dl + 1],
                        [dr + 1]
                    ])
                ],
                [answer]
            )
            input()


if __name__ == '__main__':
    main()
