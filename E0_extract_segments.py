import pandas as pd
import numpy as np
from tqdm import tqdm
from imutils.video import VideoStream
import os
import cv2
from U0_frame_iterator import Streamer

target_col = "Close-Up"
target_col = "Extreme Close-Up"
##target_col = "Extreme Wide"
#target_col = "Long"

min_length = 1.0
#min_length = 0.0

frame_cutoff = 10000*1000

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"

args = {
    'codec' : 'MJPG',
    #'codec' : 'H264',
    #'codec' : 'X264',
    #'codec' : 'avc1',
    
    'f_output' : f'demo_{target_col}.mp4',
}
# Codec info: https://stackoverflow.com/a/30106506/249341
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

if os.path.exists(args['f_output']):
    os.system(f'rm -vf '+args['f_output'])


df = pd.read_csv("DEMO.csv")


entropy_vals = {
    "Extreme Close-Up":0.2,
    "Close-Up":0.2, # Works well!
    "Extreme Wide":0.6, # Good, but entropy can be higher >= 0.4
    "Long":0.6, # Good, but entropy can be higher >= 0.4
    "Medium":0.6, # Good, multiple character interactions
    "Medium Close-Up":0.6, # Good, character interactions
}

df = df[df['frame_entropy'] < entropy_vals[target_col]]
df = df[df[target_col] > 0.90]
print(len(df))
df = df[df['Length (seconds)'] >= min_length]
print(len(df))


n_frames = int(df.iloc[-1]['Start Frame'] + df.iloc[-1]['Length (frames)'])

# Mark which frames we want to keep
tags = np.zeros(shape=(n_frames*2,), dtype=bool)
for _,row in df.iterrows():
    k0 = int(row['Start Frame'])
    k1 = k0+int(row['Length (frames)'])
    tags[k0:k1-1] = True

# Sanity check
#assert(tags.sum() == df['Length (frames)'].sum())

movie = Streamer(f_movie, None)

# Match the FPS of the movie
args['fps'] = movie.fps

frames_written = 0

for i, frame in tqdm(movie):
    
    if i > frame_cutoff:break
    
    if not tags[i]:
        continue

    # check if the writer is None
    if writer is None:
        # store the image dimensions, initialize the video writer,
        # and construct the zeros array
        (h, w) = frame.shape[:2]

            
        writer = cv2.VideoWriter(
            args['f_output'], fourcc, args["fps"], (w, h), True)

        #writer = cv2.VideoWriter.open(
        #    args['f_output'],0x21,movie.fps,(w,h),True);

        #writer = cv2.VideoWriter(
        #    args['f_output'],21,movie.fps,(w,h),True);

    # write the output frame to file
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    writer.write(frame)

    frames_written += 1


writer.release()
print(f"Total time written {frames_written/movie.fps}")
