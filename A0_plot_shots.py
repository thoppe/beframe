from tqdm import tqdm
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt

df = pd.read_csv(
    "data/shot_detection/Die.Hard.1988.720p.BRRip.x264-x0r.mkv.csv")

df = df[5000:8000]

plt.plot(df['Medium'])
plt.show()
