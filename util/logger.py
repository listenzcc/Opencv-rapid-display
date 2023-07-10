"""
File: logger.py
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
import logging
from pathlib import Path


# %% ---- 2023-07-10 ------------------------
# Function and class
log_folder = Path(__file__).parent.parent.joinpath('log')
log_folder.mkdir(parents=True, exist_ok=True)


class MyLogger(object):
    name = 'OpenCV-Display'
    file_handler_log_level = logging.DEBUG
    file_handler_log_fmt = '%(asctime)s %(name)s %(levelname)-8s %(message)-40s {{%(filename)s:%(lineno)s:%(module)s:%(funcName)s}}'
    filepath = log_folder.joinpath('OpenCV-Display.log')
    stream_handler_log_level = logging.DEBUG
    stream_handler_log_fmt = '%(asctime)s %(name)s %(levelname)-8s %(message)-40s {{%(filename)s:%(lineno)s}}'

    def __init__(self):
        self.logger = self.mk_logger()

    def mk_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(self.filepath)
        fh.setFormatter(logging.Formatter(self.file_handler_log_fmt))
        fh.setLevel(self.file_handler_log_level)

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(self.stream_handler_log_fmt))
        sh.setLevel(self.stream_handler_log_level)

        for hdl in [fh, sh]:
            logger.addHandler(hdl)
        return logger


LOGGER = MyLogger().logger

# %% ---- 2023-07-10 ------------------------
# Play ground


# %% ---- 2023-07-10 ------------------------
# Pending


# %% ---- 2023-07-10 ------------------------
# Pending
