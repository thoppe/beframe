from tqdm import tqdm
import json
import pandas as pd
import numpy as np
import subprocess
import collections
import os
from source.pipeline import Pipeline


def compute(f_movie, f1):
    print(f"Starting {f_movie}")

    # First count the total number of frames (should abstract this method)
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {f_movie}"

    try:
        n_frames = subprocess.check_output(cmd, shell=True)
        n_frames = int(n_frames)
    except ValueError:
        print(f"Couldn't read frame count for {f_movie}")
        n_frames = None

    # Now stream through the frames counting them
    cmd = f"ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv {f_movie}"
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    n = 0
    progress = tqdm(total=n_frames)

    frame_type = []

    for line in proc.stdout:
        line = line.decode().strip()
        if "frame" not in line:
            continue

        n += 1
        progress.update(1)

        frame_type.append(line.split(",")[1])

        # if n > 2000:
        #    break

    progress.close()

    df = pd.DataFrame(data=frame_type, columns=["frame_type"])

    # Only keep keyframes
    df = df[df.frame_type == "I"]

    keyframes = df.index.tolist()

    print(f"Out of {n_frames}, found {len(keyframes)} keyframes in {f_movie}")

    js = {
        "ffprobe_frame_count": n_frames,
        "total_keyframes": len(keyframes),
        "keyframes": keyframes,
    }

    js = json.dumps(js)

    with open(f1, "w") as FOUT:
        FOUT.write(js)


"""
f_movie = sys.argv[1]
assert os.path.exists(f_movie)

save_dest = f"data/keyframes"
os.system(f"mkdir -p {save_dest}")

f_save = os.path.join(save_dest, os.path.basename(f_movie) + ".json")
"""

P = Pipeline(
    load_dest="data/movies/",
    save_dest="data/keyframes/",
    # old_extension="mp4",
    new_extension="json",
)(compute, -1)
