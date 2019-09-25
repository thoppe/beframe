import pandas as pd
import numpy as np
import os
import scipy.stats

#f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
f_movie = "data/movies/Fight.Club.1999.10th.Ann.Edt.BluRay.720p.H264.mp4"

extension = f_movie.split('.')[-1]

name = os.path.basename(f_movie)

save_dest = 'results/shot_summary'
os.system(f'mkdir -p {save_dest}')
f_save = os.path.join(save_dest, name + '.csv')

f_shots = os.path.join("data/shot_detection/", name + ".npy")
f_scenes = os.path.join(
    "data/scene_change/",
    name,
    name.replace("."+extension, "-Scenes.csv")
)

cols = [
    'Close-Up', 'Extreme Close-Up', 'Extreme Wide', 'Long', 'Medium',
    'Medium Close-Up'
]
df = pd.DataFrame(data=np.load(f_shots), columns=cols, dtype=float)
df.index.name = 'frame_n'

scenes = pd.read_csv(f_scenes, skiprows=1)

# Fill in the scene information onto the shot dataframe
df["scene_n"] = None
df.loc[scenes["Start Frame"], "scene_n"] = scenes["Scene Number"].values
df = df.fillna(method="ffill")

# Compute an average over each shot type
g = df.groupby("scene_n")

for col in cols:
    scenes[col] = g[col].mean().values

# Measure scene entropy
entropy = []
for _, dx in df.groupby("scene_n"):
    ent = [scipy.stats.entropy(q) for q in dx[cols].values]
    entropy.append(np.average(ent))
scenes["frame_entropy"] = entropy

scenes = scenes.set_index("Scene Number").round(4)

scenes.to_csv(f_save, float_format="%0.4f")

print(f"Saved to {f_save}")
