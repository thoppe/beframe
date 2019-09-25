from tqdm import tqdm
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt

f_shots = "data/shot_detection/Die.Hard.1988.720p.BRRip.x264-x0r.mkv.npy"

cols = [
    'Close-Up', 'Extreme Close-Up', 'Extreme Wide', 'Long', 'Medium',
    'Medium Close-Up'
]
df = pd.DataFrame(data=np.load(f_shots), columns=cols, dtype=float)
df.index.name = 'frame_n'


df = df[5000:8000]

plt.plot(df["Medium"])
plt.show()
