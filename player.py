"""
File: player.py
Author: Chuncheng Zhang
Date: 2023-07-10
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-07-10 ------------------------
# Requirements and constants
import cv2
import numpy as np
from util.constant import *
from util.image_loader import load_folder


# %% ---- 2023-07-10 ------------------------
# Function and class

class PreciseClock(object):
    def __init__(self, interval=100):
        self.interval = interval
        self.magic = 1000 / interval
        pass

    def start(self):
        self.tic = time.time()
        return self.tic

    def count(self):
        t = time.time()
        passed = t - self.tic
        return int(passed * self.magic)


# %% ---- 2023-07-10 ------------------------
# Play ground
images = load_folder(Path(os.environ['OneDriveConsumer'],
                          'Pictures', 'DesktopPictures'))


def shift():
    image = images.pop(0)
    images.append(image)
    return image.image['image_id'], cv2.cvtColor(np.array(image.image['img']), cv2.COLOR_RGB2BGR)

# %% ---- 2023-07-10 ------------------------
# Pending


pc = PreciseClock(20)

n = 0
times = []

pc.start()
while n < 500:  # len(images):
    if pc.count() < n:
        continue

    if n % 5 == 0:
        image_id, mat = shift()
        image_id2, mat2 = shift()

    r = (n % 5) / 5
    r1 = 1 - r

    n += 1

    times.append(time.time())
    cv2.imshow('Frame', (mat * r + mat2 * r1).astype(np.uint8))
    cv2.waitKey(1)
    print('Display frame {} on {}'.format(image_id, times[-1]))


print((np.array(times[1:]) - np.array(times[:-1])) * 1000)

cv2.waitKey(1)

# %% ---- 2023-07-10 ------------------------
# Pending
# %%
# %%
