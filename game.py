

from math import floor
import os
from random import random
from time import sleep
import keyboard


class Game():
    class Lost(Exception):
        def __init__(self, score: int):
            # Call the base class constructor with the parameters it needs
            super().__init__(score)
            self.score = score

        def __str__(self):
            return "GAME OVER!\nScore: %d" % self.score

    gameMap: list[tuple[int, int]]
    player: int
    score: int
    frame: int

    def __init__(self, distance=30):
        self.gameMap = [(0, 0) for _ in range(distance)]
        self.score = 0
        self.player = 0
        self.initInput()
        self.frame = 0

    def nextFrame(self):
        self.frame += 1
        self.render()
        self.checkPlayer()
        self.award()
        if self.frame % 5 == 0:
            self.scroll()
        sleep(1 / 30)
        return self

    def scroll(self):
        d = floor(10 * random())
        self.gameMap.pop(0)
        if d >= 8 and self.gameMap[-1] != (0, 1):
            self.gameMap.append((1, 0))
        elif d >= 6 and self.gameMap[-1] != (1, 0):
            self.gameMap.append((0, 1))
        else:
            self.gameMap.append((0, 0))

        return self

    def checkPlayer(self):
        if self.player == 0 and self.gameMap[0][0] == 1:
            raise self.Lost(self.score)
        elif self.player == 1 and self.gameMap[0][1] == 1:
            raise self.Lost(self.score)
        return self

    def award(self):
        self.score += 100

        return self

    def moveLeft(self):
        self.player = 0

        return self

    def moveRight(self):
        self.player = 1

        return self

    def render(self):
        os.system('cls')
        print('Score: %d' % self.score)
        # renderMap = self.gameMap.copy()
        # renderMap.reverse()
        L = len(self.gameMap)
        render = ''
        for i in range(L):
            obs: tuple[str, str]
            match self.gameMap[L - i - 1]:
                case (0, 0):
                    obs = (' ', ' ')
                case (1, 0):
                    obs = ('¤', ' ')
                case (0, 1):
                    obs = (' ', '¤')
            if i != L - 1:
                render += '| %s | %s |\n' % obs
            else:
                pl: tuple[str, str]
                match self.player:
                    case 0:
                        pl = ('^', obs[1])
                    case 1:
                        pl = (obs[0], '^')
                render += '| %s | %s |\n' % pl
        print(render)
        return self

    def initInput(self):
        keyboard.on_press_key("left", lambda _: self.moveLeft())
        keyboard.on_press_key("right", lambda _: self.moveRight())

        return self
