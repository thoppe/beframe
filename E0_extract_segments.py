import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from source.U1_smart_cuts import composite_video

# target_col = "Close-Up"
# target_col = "Extreme Wide"
# target_col = "Long"
# target_col = "Medium"
# target_col = "Medium Close-Up"
target_col = "Extreme Close-Up"

min_length = 1.0

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"

df = pd.read_csv("DEMO.csv")

entropy_vals = {
    "Extreme Close-Up": 0.2,
    "Close-Up": 0.2,  # Works well!
    "Extreme Wide": 0.6,  # Good, but entropy can be higher >= 0.4
    "Long": 0.6,  # Good, but entropy can be higher >= 0.4
    "Medium": 0.6,  # Good, multiple character interactions
    "Medium Close-Up": 0.6,  # Good, character interactions
}

df = df[df["frame_entropy"] < entropy_vals[target_col]]
df = df[df[target_col] > 0.90]
df = df[df["Length (seconds)"] >= min_length]
print(len(df))
print(df.columns)

T0 = df["Start Timecode"]
DURATION = df["Length (timecode)"]

target_col = target_col.replace(" ", "-")
f_output = f"demo_movies/demo_{target_col}.mp4"

if os.path.exists(f_output):
    os.system(f"rm -vf {f_output}")


composite_video(f_movie, f_output, T0, DURATION, False)
