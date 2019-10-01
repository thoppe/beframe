import pandas as pd
import numpy as np
import os, sys
from tqdm import tqdm
import cv2

min_length = 1.0
target_col = "Medium Close-Up"

### FFMPEG and CV2 are off by ***three*** whole frames?!?!
# For cv2 frames, the start is correct, the end is one too many
# For ffmpeg same thing, but offset by three forward???


##########################################################################


def select_shots(f_movie, target_col):

    name = os.path.basename(f_movie)
    f_info = os.path.join("data/info_scenes/", name + ".csv")
    assert os.path.exists(f_info)

    df = pd.read_csv(f_info)
    named_col = target_col.replace(" ", "-")

    # Ad-hoc values measured for shot selection
    entropy_vals = {
        "Extreme Close-Up": 0.2,
        "Close-Up": 0.2,  # Works well!
        "Extreme Wide": 0.6,  # Good, but entropy can be higher >= 0.4
        "Long": 0.6,  # Good, but entropy can be higher >= 0.4
        "Medium": 0.6,  # Good, multiple character interactions
        "Medium Close-Up": 0.6,  # Good, character interactions
    }

    # Filter for low entropy, high average shot, and min length
    dx = df.copy()
    dx = dx[dx["frame_entropy"] < entropy_vals[target_col]]
    dx = dx[dx[target_col] > 0.90]
    dx = dx[dx["Length (seconds)"] >= min_length]

    return dx


def segmented_iterator(f_movie, df):

    # Create the target directory
    name = os.path.basename(f_movie)
    save_dest = f"data/clips/{name}"
    os.system(f"mkdir -p {save_dest}")
    
    for _, row in df.iterrows():

        scene_n = row['Scene Number']
        f_save = os.path.join(save_dest, f"{scene_n:04d}.wav")
        
        if os.path.exists(f_save):
            continue

        print(f"Starting {scene_n}")
        
        t0, t1 = row["Start Timecode"], row["Length (timecode)"]
        #t0, t1 = row["Start Timecode"], row["End Timecode"]
        
        quiet =" -hide_banner -loglevel panic "

        cmd = f'ffmpeg {quiet} -ss {t0} -i {f_movie} -vn -t {t1} {f_save}'
        #cmd = f'ffmpeg {quiet} -i {f_movie} -vn -ss {t0} -t {t1} {f_save}'
        os.system(cmd)


##########################################################################


f_movie = sys.argv[1]
assert os.path.exists(f_movie)

df = select_shots(f_movie, target_col)
print(f"Extracting {len(df)} audio clips from {f_movie}")

segmented_iterator(f_movie, df)
