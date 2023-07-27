"""
File: main.py
Author: Chuncheng Zhang
Date: 2023-07-27
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


# %% ---- 2023-07-27 ------------------------
# Requirements and constants
import mne

import pandas as pd
import plotly.express as px

from rich import print
from pathlib import Path
from IPython.display import display


# %% ---- 2023-07-27 ------------------------
# Function and class
parallel_tag = dict(
    rsvp_session_start=16,
    rsvp_session_stop=32,
    other_image_display=2,
    target_image_display=4,
    keypress_event=8,
)

# %% ---- 2023-07-27 ------------------------
# Play ground
df = pd.read_csv(Path('time_recording.csv'), index_col=0)
df1 = df.query('recordEvent == "keyPress"')
display(df1, len(df1))
df2 = df[df['imgId'].map(lambda e: str(e).startswith('target'))]
display(df2, len(df2))

df = pd.concat([df1, df2])
df = df.sort_values(by='time')
df.index = range(len(df.index))
df['time'] -= df.loc[0, 'time']
df['time'] *= 1000
df['time'] = df['time'].map(int)
display(df)


# %%
set(df['recordEvent'])

# %% ---- 2023-07-27 ------------------------
# Pending
raw = mne.io.read_raw_cnt('test.cnt')
events = mne.events_from_annotations(raw)
print(events, events[0].shape)

inv_table = dict()
for k, v in events[1].items():
    inv_table[v] = int(k)

events = pd.DataFrame(events[0], columns=['pos', 'lasting', 'event'])
events['code'] = events['event'].map(lambda e: inv_table[e])
events

events1 = events[events['code'].map(lambda e: e & 8 == 8)].copy()
events1['event'] = 'keyPress'
display(events1, len(events1))

events2 = events[events['code'].map(lambda e: e & 4 == 4)].copy()
events2['event'] = 'displayImage'
display(events2, len(events2))

events = pd.concat([events1, events2])
events = events.sort_values(by='pos')
events .index = range(len(events.index))
events['pos'] -= events.loc[0, 'pos']
display(events)


# %% ---- 2023-07-27 ------------------------
# Pending
display(df)

display(events)

# %%
fig = px.scatter(df, x='time', y='recordEvent')
fig.show()

fig = px.scatter(events, x='pos', y='event')
fig.show()

px.scatter(df['time'] - events['pos'])
# %%
