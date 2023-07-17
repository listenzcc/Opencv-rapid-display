"""
File: check_time_recording.py
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
import pandas as pd
import plotly.express as px

from rich import print


# %% ---- 2023-07-11 ------------------------
# Function and class
table = pd.read_csv('time_recording.csv', index_col=0)
print(table)


# %% ---- 2023-07-11 ------------------------
# Play ground
table['interval'] = 20
times = table['time'].to_numpy() * 1000
table.loc[1:, 'interval'] = times[1:] - times[:-1]

table['mark'] = table['id'].map(
    lambda e: 'key' if not pd.isna(e) else 'interpolate')
print(table)


# %% ---- 2023-07-11 ------------------------
# Pending
fig = px.scatter(table, x='frame', y='interval', color='mark', opacity=0.5)
fig.show()

fig = px.violin(table, y='interval', color='mark', box=True)
fig.show()

# %% ---- 2023-07-11 ------------------------
# Pending
