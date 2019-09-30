from tqdm import tqdm
import numpy as np
import os, glob
import sys, json

f_movie = sys.argv[1]
assert os.path.exists(f_movie)

name = os.path.basename(f_movie)
F_CLIPS = sorted(glob.glob(f"data/clips/{name}/*"))

save_dest = f'compiled/{name}'
os.system(f'mkdir -p {save_dest}')

for f0 in F_CLIPS:
    fc = os.path.join(f'data/deepspeech/{name}', os.path.basename(f0))
    fc = '.'.join(fc.split('.')[:-1])+'.json'

    if not os.path.exists(fc):
        #print(f"Missing {fc}")
        continue

    with open(fc) as FIN:
        js = json.load(FIN)

    text = js['text'].strip()

    if any(text):
        continue

    if not os.path.exists(os.path.join(save_dest, os.path.basename(f0))):
        os.system(f'cp -v {f0} {save_dest}')

