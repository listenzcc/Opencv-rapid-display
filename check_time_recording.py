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
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from rich import print


# %% ---- 2023-07-11 ------------------------
# Function and class
raw_data = pd.read_csv('time_recording.csv', index_col=0)
if not 'code' in raw_data.columns:
    raw_data['code'] = ''

table = raw_data.query(
    'recordEvent == "displayImage"').copy()
table.index = range(len(table))
print(table)


# %% ---- 2023-07-11 ------------------------
# Play ground
times = table['time'].to_numpy() * 1000
table.loc[1:, 'interval'] = times[1:] - times[:-1]

table = table.loc[1:]

table['mark'] = table['imgId'].map(
    lambda e: 'key' if not pd.isna(e) else 'interpolate')
print(table)


# %% ---- 2023-07-11 ------------------------
# Pending
fig = px.scatter(table, x='frameIdx', y='interval', color='mark', opacity=0.5)
trace1 = fig.data
# fig.show()

fig = px.violin(table, y='interval', color='mark', box=True)
trace2 = fig.data
# fig.show()


# %% ---- 2023-07-11 ------------------------
# Pending
df1 = raw_data.query('recordEvent == "displayImage"').copy()
df1 = df1[df1['imgId'].map(lambda e: not pd.isna(e))].copy()
df1['imgType'] = df1['imgId'].map(lambda d: d.split('.')[0])

df2 = raw_data.query('recordEvent == "keyPress"').copy()
df2['imgType'] = 'keyPress'

df = pd.concat([df1, df2])
df['size'] = 10

fig = px.scatter(df, x='time', y='imgType', hover_data='code',
                 color='recordEvent', opacity=0.5, size='size', size_max=10)
trace3 = fig.data
# fig.show()

# %%
fig = make_subplots(rows=1, cols=3, subplot_titles=(
    'Display scatters', 'Violins histogram', 'Target vs. KeyPress'))

for t in trace1:
    fig.add_trace(t, row=1, col=1)

for t in trace2:
    fig.add_trace(t, row=1, col=2)

for t in trace3:
    fig.add_trace(t, row=1, col=3)

fig.show()
# %%
