"""
File: toolbox.py
Author: Chuncheng Zhang
Date: 2023-07-11
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


# %% ---- 2023-07-11 ------------------------
# Requirements and constants
from .constant import *


# %% ---- 2023-07-11 ------------------------
# Function and class

class PreciseClock(object):
    """
    Precise clock class for count by intervals
    """

    def __init__(self, interval=100):
        """Initialize the clock with the given interval

        Args:
            interval (int, optional): How many milliseconds the interval is. Defaults to 100.
        """
        self.interval = interval
        self.magic = 1000 / interval
        pass

    def start(self):
        """Start the clock.

        Returns:
            float: The starting time.
        """
        self.tic = time.time()
        return self.tic

    def count(self):
        """How many intervals are passed since the start of the clock.

        Returns:
            int: The number of intervals.
        """
        passed = time.time() - self.tic
        return int(passed * self.magic)


def pop(lst, idx=0, shift_flag=True):
    """Pop the lst's idx-th element from the lst.

    The function does not really pop out anything,
    since it either leaves the lst unchanged
    or append the idx-th element to the tail.

    Args:
        lst (list): The list being popped.
        idx (int, optional): The index to be popped. Defaults to 0.
        shift_flag (bool, optional): Whether shift the popped element to the tail, if False it keeps the lst unchanged. Defaults to True.

    Returns:
        list: The popped element.
    """

    if shift_flag:
        obj = lst.pop(idx)
        lst.append(obj)
    else:
        obj = lst[idx]
    return obj


def linear_interpolate(arr1, arr2, m=5):
    """Linear interpolate between two high-dimensional arrays, arr1 and arr2,
    with m segments.

    The r2 are [0, 1/m, 2/m, ... (m-1)/m],
    and the other r1 is computed by (1-r2),
    and the elements are

    r1 * arr1 + r2 * arr2

    Args:
        arr1 (np.Array): High-dimensional array.
        arr2 (np.Array): High-dimensional array, the shape is as the same as arr1.
        m (int, optional): The segments. Defaults to 5.

    Returns:
        list: The m elements of the linear interpolated array.
    """
    output = []

    for i in range(m):
        r2 = i / m
        r1 = 1 - r2

        output.append(arr1 * r1 + arr2 * r2)

    return output


# %% ---- 2023-07-11 ------------------------
# Play ground


# %% ---- 2023-07-11 ------------------------
# Pending


# %% ---- 2023-07-11 ------------------------
# Pending
