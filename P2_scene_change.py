#from tqdm import tqdm
#import pandas as pd
#import numpy as np
import os
#from U0_frame_iterator import Streamer

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
save_dest = f"data/scene_change/{f_movie}"
os.system(f"mkdir -p {save_dest}")

cmd = f'scenedetect --output {save_dest} --input {f_movie} '\
      f'time --start 300s --duration 900s '\
      f'detect-content list-scenes save-images '\

os.system(cmd)
print(cmd)

