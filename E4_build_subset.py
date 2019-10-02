from tqdm import tqdm
import numpy as np
import os, glob
import sys, json, shutil

f_movie = sys.argv[1]
assert os.path.exists(f_movie)

name = os.path.basename(f_movie)
F_SPEECH = sorted(glob.glob(f"data/google_speech/{name}/*.json"))

save_dest = f"data/beframed_clips/{name}"
os.system(f"mkdir -p {save_dest}")

for f0 in F_SPEECH:

    with open(f0) as FIN:
        js = json.load(FIN)

    n_results = js["n_results"]

    # Skip if we have a result (ie. we heard a speaker)
    if n_results:
        continue

    scene_n = int(os.path.basename(f0).split(".")[0])
    fm = os.path.join(f"data/clips/{name}/{scene_n:04d}.mp4")

    f1 = os.path.join(save_dest, os.path.basename(fm))

    if os.path.exists(f1):
        continue

    assert os.path.exists(fm)

    os.system(f"cp -v {fm} {f1}")


# Clean all the clips
clip_dir = f"data/clips/{name}"

if os.path.exists(clip_dir):
    print(f"Cleaning {clip_dir}")
    shutil.rmtree(clip_dir)
