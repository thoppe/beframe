from tqdm import tqdm
import pandas as pd
import numpy as np
import os
import sys

import fastai
from fastai.vision import pil2tensor, Image as fastImage

from source.U0_frame_iterator import Streamer


learn = fastai.basic_train.load_learner(
    "models/shot-type-classifier/", file="shot-type-classifier.pkl"
)

# f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"

f_movie = sys.argv[1]
assert os.path.exists(f_movie)

save_dest = f"data/shot_detection"
os.system(f"mkdir -p {save_dest}")

f_save = os.path.join(save_dest, os.path.basename(f_movie) + ".npy")

data = []
for n, frame in tqdm(Streamer(f_movie, None)):

    # Convert to torch.Tensor, then fastai.tensor
    img = pil2tensor(frame, np.float32).div_(255)
    img = fastImage(img)

    pred = learn.predict(img)
    prob = pred[2].numpy()

    item = {"frame_n": n}
    for k, i in learn.data.c2i.items():
        item[k] = prob[i]

    data.append(item)
    # if len(data)> 10:
    #    break

cols = [
    "Close-Up",
    "Extreme Close-Up",
    "Extreme Wide",
    "Long",
    "Medium",
    "Medium Close-Up",
]

df = pd.DataFrame(data).set_index("frame_n")

# Make sure the column order is correct
df = df[cols]
# df.to_csv(f_save)

# Save the data to a lower resolution numpy array
x = df.values.astype(np.float16)
np.save(f_save, x)

print(f"Saved to {f_save}")
