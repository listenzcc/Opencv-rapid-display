"""
File: fast-movie-player.py
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
# import torch
import numpy as np
from util.constant import *
from util.toolbox import PreciseClock, pop, linear_interpolate
from util.image_loader import read_local_images


# %% ---- 2023-07-10 ------------------------
# Function and class

def uint8(x):
    return x.astype(np.uint8)


class VeryFastVeryStableBuffer(object):
    def __init__(self, images, m=5):
        self.images = images
        self.m = m
        self.buffer = []
        self.size = 0

    def clear_buffer(self):
        [self.pop() for _ in range(self.size)]
        self.size = 0
        return

    def pop(self):
        mats = [self.buffer.pop(0) for _ in range(self.m)]
        self.size -= 1

        threading.Thread(target=self.auto_append, daemon=True).start()

        return mats

    def auto_append(self):
        image = pop(self.images)
        mat1 = image.get('bgr')
        id = image.get('image_id')
        mat2 = pop(self.images, shift_flag=False).get('bgr')

        for e in linear_interpolate(mat1, mat2, self.m):
            self.buffer.append((id, uint8(e)))
            # Only attach the id to the first element
            id = None

        self.size += 1

        return self.size

    def loop(self):
        threading.Thread(target=self._loop, args=(), daemon=True).start()
        return

    def _loop(self, sleep_interval=20):
        secs = sleep_interval / 1000
        while True:
            if self.size < 10:
                self.auto_append()

            time.sleep(secs)
            print('Loop', self.size, len(self.buffer))


# %% ---- 2023-07-10 ------------------------
# Play ground
images = read_local_images(Path(os.environ['OneDriveConsumer'],
                                'Pictures', 'DesktopPictures'))


# %% ---- 2023-07-10 ------------------------
# Pending
interval = 20  # milliseconds
display_seconds = 60  # seconds
frames = int(display_seconds / (interval / 1000))
print('Display with {} frames'.format(frames))

vfvsb = VeryFastVeryStableBuffer(images)
pc = PreciseClock(interval)

for _ in range(5):
    vfvsb.auto_append()


mats = vfvsb.pop()

for _ in range(vfvsb.m):
    cv2.imshow('Frame', mats.pop()[1])
    cv2.waitKey(100)

cv2.waitKey()

n = 0
time_recording = []

pc.start()
while n < frames:
    if pc.count() < n:
        continue

    if n % 5 == 0:
        pairs = vfvsb.pop()

    id, m = pairs.pop(0)

    if n % 10 < 2:
        m[:100, :100] = 255
    else:
        m[:100, :100] = 0

    # m[:100, :100] = (n % 2) * 255

    t = time.time()
    cv2.imshow('Frame', m)
    time_recording.append((n, id, t))
    cv2.waitKey(1)
    print('Display {: 4d} at {:.4f} for {}'.format(
        n, time_recording[-1][-1], id))

    n += 1


cv2.waitKey(1)

# %% ---- 2023-07-10 ------------------------
# Pending
table = pd.DataFrame(time_recording, columns=['frame', 'id', 'time'])

table.to_csv('time_recording.csv')

print(table)

# %%
# %%
