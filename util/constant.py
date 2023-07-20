"""
File: constant.py
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
import sys
import time
import ctypes
import logging
import keyboard
import threading
import numpy as np
import pandas as pd

from PIL import Image
from pathlib import Path
from omegaconf import OmegaConf
from rich import print, inspect
from dataclasses import dataclass
from tqdm.auto import tqdm

from .logger import LOGGER


# %% ---- 2023-07-10 ------------------------
# Function and class

@dataclass
class ProjectConf:
    name: str = 'OpenCV-Display'
    version: str = '0.0.1'


# %% ---- 2023-07-10 ------------------------
# Play ground

CONFIG = OmegaConf.structured(dict(
    project=ProjectConf,
))

LOGGER.info('Constant is loaded')

# %% ---- 2023-07-10 ------------------------
# Pending


# %% ---- 2023-07-10 ------------------------
# Pending
