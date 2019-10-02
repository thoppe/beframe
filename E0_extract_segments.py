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
    save_dest = f"data/frames/{name}"
    os.system(f"mkdir -p {save_dest}")

    N = df["End Frame"].max()
    is_target = np.zeros(shape=N, dtype=int)
    for i, j, k in zip(df["Start Frame"], df["End Frame"], df["Scene Number"]):
        is_target[i:j] = k

    print("Frame extraction points", df["Start Frame"].values)
    print(f"Extracting {(is_target>0).mean():0.3f} fraction")

    stream = cv2.VideoCapture(f_movie)
    # estimated_total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    # FPS = int(stream.get(cv2.CAP_PROP_FPS))
    # import imutils

    scene_n = None

    for i in tqdm(range(N)):
        # grab the frame from the threaded video file stream
        (grabbed, frame) = stream.read()

        if not grabbed:
            break

        if not is_target[i]:
            continue

        if scene_n != is_target[i]:
            print(f"Starting scene {is_target[i]}")
            idx = 0

        scene_n = is_target[i]

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        f_save = os.path.join(save_dest, f"{scene_n:04d}_{idx:06d}.png")

        cv2.imwrite(f_save, frame)
        idx += 1


##########################################################################

if __name__ == "__main__":
    f_movie = sys.argv[1]
    assert os.path.exists(f_movie)

    df = select_shots(f_movie, target_col)
    print(f"Extracting {len(df)} scenes from {f_movie}")

    segmented_iterator(f_movie, df)
