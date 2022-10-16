

from math import sqrt
import numpy as np
from connect import Connect


class BizInteract:

    def __init__(
        self,
        host='localhost',
        port=9999
    ):
        self.host = host
        self.port = port
        self.con = None

    def connect(self):
        self.con = Connect(self.host, self.port)
        self.con.connect()
        return self

    def disconnect(self):
        self.con.disconnect()
        self.con = None
        return self

    def receiveState(self, includeScore=True, state2d=False, stateWidth=0, stateHeight=0, clrDict: dict[int, list[int]] = {}):
        if self.con == None:
            raise 'Connection is not established, use self.connect()'

        self.con.awaitConnection()
        gameData = self.con.recv().decode('utf-8')
        i = 0
        j = 7
        marioX = int(gameData[i:j])
        i = j
        j += 7
        marioY = int(gameData[i:j])
        score = None
        if includeScore:
            i = j
            j += 10
            score = int(gameData[14:24])
        i = j
        j += 1
        status = int(gameData[i:j])
        i = j
        j += 13 ** 2
        state = np.reshape(
            [int(d) for d in gameData[i:j]],
            (len(gameData) - i, 1))

        # Formatera state:

        if state2d:
            sqrSize = int(sqrt(state.size))

            if stateWidth * stateHeight == state.size:
                state = np.reshape(state, (stateHeight, stateWidth))
            elif sqrSize ** 2 == state.size:
                state = np.reshape(state, (sqrSize, sqrSize))
            else:
                raise 'No dimensions were provided for 2d transformation and the matrix size is not a perfect square'

        if len(clrDict) > 0:
            nState = []
            for i in range(state.shape[0]):
                nState.append([])
                for j in range(state.shape[1]):
                    nState[-1].append(clrDict[state[i, j]])
            state = np.array(nState, np.float32)

        return marioX, marioY, score, status, state


if __name__ == '__main__':
    i = BizInteract()
    i.connect()
    i.receiveState()
    i.disconnect()
