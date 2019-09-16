import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from source.U1_smart_cuts import composite_video

min_length = 1.0
is_HQ = False
f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"

name = os.path.basename(f_movie)
f_info = os.path.join('results/shot_summary', name+'.csv')
df = pd.read_csv(f_info)

save_dest = f'data/clips/{name}'
os.system(f'mkdir -p {save_dest}')

# Ad-hoc values measured for shot selection
entropy_vals = {
    "Extreme Close-Up": 0.2,
    "Close-Up": 0.2,  # Works well!
    "Extreme Wide": 0.6,  # Good, but entropy can be higher >= 0.4
    "Long": 0.6,  # Good, but entropy can be higher >= 0.4
    "Medium": 0.6,  # Good, multiple character interactions
    "Medium Close-Up": 0.6,  # Good, character interactions
}

for target_col in entropy_vals:

    named_col = target_col.replace(" ", "-")
    f_output = os.path.join(save_dest, f"{named_col}.mp4")                 

    if os.path.exists(f_output):
        continue

    print(f_output)
    
    # Filter for low entropy, high average shot, and min length
    df = df[df["frame_entropy"] < entropy_vals[target_col]]
    df = df[df[target_col] > 0.90]
    df = df[df["Length (seconds)"] >= min_length]

    T0 = df["Start Timecode"]
    DURATION = df["Length (timecode)"]

    composite_video(f_movie, f_output, T0, DURATION, is_high_quality=is_HQ)
