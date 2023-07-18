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
import os
import cv2
# import torch
import keyboard
import threading

import numpy as np

from util.constant import *
from util.toolbox import PreciseClock, pop, linear_interpolate
from util.image_loader import read_local_images


# %% ---- 2023-07-10 ------------------------
# Function and class
class DynamicOptions(object):
    def __init__(self):
        pass

    def start(self):
        self.receive_keyboard_flag = True
        self.recording = []

    def record(self, dct):
        threading.Thread(target=self.recording.append, args=(dct, )).start()

    def stop(self):
        self.receive_keyboard_flag = False


dy_opt = DynamicOptions()


def uint8(x):
    return x.astype(np.uint8)


def receive_keyboard():
    def _receive_keyboard():
        LOGGER.debug('Start receive keyboard')
        while dy_opt.receive_keyboard_flag:
            event = keyboard.read_event(suppress=True)
            t = time.time()
            if event.event_type == keyboard.KEY_DOWN:
                print('Key pressed {}'.format(event))
                dy_opt.record(dict(
                    time=t,
                    event=event,
                    recordType='keyDown'
                ))
        LOGGER.debug('Stop receive keyboard')

    threading.Thread(target=_receive_keyboard, daemon=True).start()


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
interval = 100  # milliseconds
display_seconds = 60  # seconds
frames = int(display_seconds / (interval / 1000))
print('Display with {} frames'.format(frames))

vfvsb = VeryFastVeryStableBuffer(images, m=1)
pc = PreciseClock(interval)

for _ in range(5):
    vfvsb.auto_append()

mats = vfvsb.pop()

for _ in range(vfvsb.m):
    cv2.imshow('Frame', mats.pop()[1])
    cv2.waitKey(100)

cv2.waitKey()

dy_opt.start()
receive_keyboard()

frame_idx = 0
time_recording = []

pc.start()
while frame_idx < frames:
    if pc.count() < frame_idx:
        continue

    pairs = vfvsb.pop()
    id, bgr = pairs.pop(0)

    if frame_idx % 2 == 1:
        bgr[:100, :100] = 255
    else:
        bgr[:100, :100] = 0

    t = time.time()
    cv2.imshow('Frame', bgr)
    # cv2.waitKey(1)

    while cv2.pollKey() > 0:
        cv2.pollKey()

    time_recording.append((frame_idx, id, t))
    dy_opt.record(dict(
        time=t,
        imgId=id,
        frameIdx=frame_idx,
        recordType='displayImage'
    ))
    print('Display {: 4d} at {:.4f} for {}'.format(
        frame_idx, time_recording[-1][-1], id))

    frame_idx += 1


cv2.waitKey(1)
dy_opt.stop()

table = pd.DataFrame(dy_opt.recording)
table.to_csv('time_recording.csv')


# %% ---- 2023-07-10 ------------------------
# Pending
# table = pd.DataFrame(time_recording, columns=['frameIdx', 'imageId', 'time'])

# table.to_csv('time_recording.csv')

# print(table)

os.system('python check_time_recording.py')

# %%
# %%
