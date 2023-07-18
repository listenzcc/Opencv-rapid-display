"""
File: mk-RSVP-file-list.py
Author: Chuncheng Zhang
Date: 2023-07-18
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


# %% ---- 2023-07-18 ------------------------
# Requirements and constants

import random
import pandas as pd

from rich import print
from pathlib import Path
from tqdm.auto import tqdm


# %% ---- 2023-07-18 ------------------------
# Function and class

# %% ---- 2023-07-18 ------------------------
# Play ground
root = Path(__file__).parent
folder = Path('C:/Users/zcc/Desktop/rsvp-images/block1')
assert folder.is_dir(), 'Not a directory, {}'.format(folder)

targets = [e for e in folder.joinpath(
    'target').iterdir() if e.is_file() and e.name.endswith('.jpg')]
others = [e for e in folder.joinpath(
    'nontarget').iterdir() if e.is_file() and e.name.endswith('.jpg')]

print('Found targets {}, others {}'.format(len(targets), len(others)))


# %% ---- 2023-07-18 ------------------------
# Pending
file_list = []

tag = 'target'
for path in tqdm(targets, 'Stack targets'):
    img_id = tag + '.' + path.name
    file_list.append((path, img_id, tag))


tag = 'other'
for path in tqdm(others, 'Stack others'):
    img_id = tag + '.' + path.name
    file_list.append((path, img_id, tag))

random.shuffle(file_list)

table = pd.DataFrame(file_list, columns=['path', 'imgId', 'tag'])
table.to_csv(root.joinpath('example.csv'))
print(table)

# %% ---- 2023-07-18 ------------------------
# Pending
