from time import time
from typing import Callable
from ale_py import ALEInterface
import ale_py
import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers, Model
from baselines.common.atari_wrappers import make_atari, wrap_deepmind
from BizInteract import BizInteract


def breakoutEnv():
    # env = make_atari("BreakoutNoFrameskip-v4")
    env = gym.make('BreakoutNoFrameskip-v4', render_mode='human')
    env = wrap_deepmind(env, frame_stack=True, scale=True)
    env.seed(42)

    return env


def createModel(iShape: tuple, oSize: int):
    inputs = layers.Input(shape=iShape)

    l1 = layers.Conv2D(32, 8, strides=4, activation='relu')(inputs)
    l2 = layers.Conv2D(64, 4, strides=2, activation='relu')(l1)
    l3 = layers.Conv2D(64, 3, strides=1, activation='relu')(l2)
    l4 = layers.Flatten()(l3)
    l5 = layers.Dense(512, activation='relu')(l4)
    action = layers.Dense(oSize, activation='linear')(l5)

    return Model(inputs=inputs, outputs=action)


def reinforcement(
    getState: Callable[[], np.matrix],
    postAction: Callable[[np.matrix], tuple[np.matrix,
                                            int,
                                            bool]],
    nActions: int,
    render: Callable[[], None] = lambda _: _


):
    model = createModel((84, 84, 4), 4)
    tModel = createModel((84, 84, 4), 4)
    optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)

    gamma = 0.99
    epsilon = 1.0
    epsilonMin = 0.1
    epsilonMax = 1.0
    epsilonInterval = epsilonMax - epsilonMin
    sampleSize = 32
    eptMax = 10000

    # Buffer
    actionH = []
    stateH = []
    nStateH = []
    rewardsH = []
    rReward = 0
    doneH = []
    epRewardH = []
    epC = 0
    frC = 0
    rtEpsilon = 50000
    gtEpsilon = 1000000
    memoryMax = 100000
    aUpdate = 4
    nnUpdate = 1000
    lossFunc = keras.losses.Huber()

    while True:
        print('RESET')
        state = getState()
        epRew = 0

        tStart = time()
        atUpdate = time()
        mtUpdate = time()
        while time() - tStart < eptMax:
            # render()
            tDiff = time() - tStart
            frC += 1
            # Utför action
            if frC < rtEpsilon and epsilon > np.random.rand(1)[0]:
                action = np.random.choice(nActions)
            else:
                sTensor = tf.convert_to_tensor(state)
                sTensor = tf.expand_dims(sTensor, 0)
                aProb = model(sTensor, training=False)
                action = tf.argmax(aProb[0]).numpy()

            epsilon -= epsilonInterval / gtEpsilon
            epsilon = max(epsilon, epsilonMin)
            print('STEP')
            nState, reward, done, _ = postAction(action)
            print(f'STEPPED: s:{nState},r:{reward},d:{done}')
            epRew += reward

            # Logga state, action etc.
            actionH.append(action)
            stateH.append(state)
            nStateH.append(nState)
            doneH.append(done)
            rewardsH.append(reward)

            # Uppdatera modellen
            if frC % aUpdate == 0 and len(doneH) > sampleSize:
                atUpdate = time()

                indices = np.random.choice(
                    range(len(doneH)), size=sampleSize)

                sState = np.array([stateH[i] for i in indices])
                snState = np.array([nStateH[i] for i in indices])
                sRewards = np.array([rewardsH[i] for i in indices])
                sAction = np.array([actionH[i] for i in indices])
                sDone = tf.convert_to_tensor(
                    [float(doneH[i]) for i in indices]
                )

                fRewards = tModel.predict(snState)

                uQ = sRewards + gamma * tf.reduce_max(fRewards, axis=1)
                uQ = uQ * (1 - sDone) - sDone

                mask = tf.one_hot(sAction, nActions)

                with tf.GradientTape() as tape:

                    # Träna modellen på förutsädda states
                    vQ = model(sState)
                    aQ = tf.reduce_sum(tf.multiply(vQ, mask), axis=1)
                    loss = lossFunc(uQ, aQ)

                gradient = tape.gradient(loss, model.trainable_variables)
                optimizer.apply_gradients(
                    zip(gradient, model.trainable_variables))

            if frC % nnUpdate == 0:
                mtUpdate = time()

                tModel.set_weights(model.get_weights())
                print(f'updated target model')

            if len(rewardsH) > memoryMax:
                del rewardsH[:1]
                del actionH[:1]
                del stateH[:1]
                del nStateH[:1]
                del doneH[:1]

            if done:
                break

        epRewardH.append(rewardsH)
        if len(epRewardH) > 100:
            del epRewardH[:1]
        rReward = np.mean(epRewardH)

        epC += 1

        if rReward > 40:
            print(f'solved at ep: {epC}')
            break


if __name__ == '__main__':
    model = createModel((84, 84, 4), 4)
    targetModel = createModel((84, 84, 4), 4)
    brenv = breakoutEnv()

    b = BizInteract()
    b.connect()

    def log(x):
        print('x', type(x), x)

    def recv():
        return b.receiveState(state2d=True, clrDict={
            0: [0, 0, 0, 255],
            1: [255, 255, 255, 255],
            2: [255, 0, 0, 255]
        })

    def brecv():
        return np.array(brenv.reset())

    def braction(action):
        return brenv.step(action)

    reinforcement(
        brecv,
        braction,
        4,
        render=brenv.render)
