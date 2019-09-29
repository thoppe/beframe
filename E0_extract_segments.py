import pandas as pd
import numpy as np
from tqdm import tqdm
import os, sys, json
from source.U1_smart_cuts import extract_clip


def extract_scenes(target_col):

    named_col = target_col.replace(" ", "-")

    # Filter for low entropy, high average shot, and min length
    dx = df.copy()
    dx = dx[dx["frame_entropy"] < entropy_vals[target_col]]
    dx = dx[dx[target_col] > 0.90]
    dx = dx[dx["Length (seconds)"] >= min_length]

    print(f"Extracting {len(dx)} scenes from {f_movie}")

    for _, row in tqdm(dx.iterrows()):
        n = row["Scene Number"]

        f_clip = os.path.join(save_dest, f"{named_col}_{n:05n}.mp4")
        if os.path.exists(f_clip):
            continue

        extract_clip(f_movie, f_clip, row)
        # if n >= 300: break

    # composite_video(
    #    f_movie, f_output, T0, DURATION, is_high_quality=is_HQ, cutoff=cutoff
    # )


##########################################################################


min_length = 1.0

f_movie = sys.argv[1]
assert os.path.exists(f_movie)

name = os.path.basename(f_movie)
f_info = os.path.join("data/info_scenes/", name + ".csv")
assert os.path.exists(f_info)

df = pd.read_csv(f_info)

# split_name = '.'.join(name.split('.')[:-1])
# f_keyframes = os.path.join('data/keyframes/', split_name + '.json')
# assert os.path.exists(f_keyframes)
# with open(f_keyframes, 'r') as FIN:
#    keyframes = json.load(FIN)['keyframes']

save_dest = f"data/clips/{name}"
os.system(f"mkdir -p {save_dest}")

# Ad-hoc values measured for shot selection
entropy_vals = {
    "Extreme Close-Up": 0.2,
    "Close-Up": 0.2,  # Works well!
    "Extreme Wide": 0.6,  # Good, but entropy can be higher >= 0.4
    "Long": 0.6,  # Good, but entropy can be higher >= 0.4
    "Medium": 0.6,  # Good, multiple character interactions
    "Medium Close-Up": 0.6,  # Good, character interactions
}

extract_scenes("Medium Close-Up")
