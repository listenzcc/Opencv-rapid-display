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

    arr1: 1.0 --------> 0.0
    arr2: 0.0 --------> 1.0

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


def get_monitor_size():
    """Get the monitor size of the main monitor

    Returns:
        width: The width in pixels of the monitor;
        height: The height in pixels of the monitor.
    """
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height


# %% ---- 2023-07-11 ------------------------
# Play ground


# %% ---- 2023-07-11 ------------------------
# Pending


# %% ---- 2023-07-11 ------------------------
# Pending
