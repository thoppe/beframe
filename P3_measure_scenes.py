import pandas as pd
import numpy as np
import os
import scipy.stats

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
name = os.path.basename(f_movie)
f_shots = os.path.join("data/shot_detection/", name + '.csv')
f_scenes = os.path.join(
    "data/scene_change/", name, name.replace('.mkv', '-Scenes.csv'))


df = pd.read_csv(f_shots)

# Shot detection frames are off by one
df.frame_n -= 1
df = df.set_index('frame_n')
cols = df.columns

keep_cols = [
    'Start Frame', 'Scene Number', 'Length (frames)', 'Length (seconds)']
scenes = pd.read_csv(f_scenes, skiprows=1)# usecols=keep_cols)

# Fill in the scene information onto the shot dataframe
df['scene_n'] = None
df.loc[scenes['Start Frame'], 'scene_n'] = scenes['Scene Number'].values
df = df.fillna(method='ffill')

# Compute an average over each shot type
g = df.groupby('scene_n')

for col in cols:
    scenes[col] = g[col].mean().values

# Measure scene entropy
entropy = []
for _, dx in df.groupby('scene_n'):
    ent = [scipy.stats.entropy(q) for q in dx[cols].values]
    entropy.append(np.average(ent))
scenes['frame_entropy'] = entropy

scenes = scenes.set_index('Scene Number').round(4)
scenes.to_csv("DEMO.csv", float_format='%0.4f')
print(scenes)
exit()




#print(df.groupby('scene_n').size())
import seaborn as sns
import pylab as plt

x = df.groupby('scene_n').size().sort_values() / 24.0
print("Median scene duration", x.median())
sns.distplot(x)
plt.show()
