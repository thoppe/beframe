import pandas as pd
import numpy as np
from tqdm import tqdm
import os
#import cv2
#from U0_frame_iterator import Streamer
#from imutils.video import VideoStream
from moviepy.editor import VideoFileClip, concatenate_videoclips

#target_col = "Close-Up"
#target_col = "Extreme Close-Up"
#target_col = "Extreme Wide"
#target_col = "Long"
target_col = "Medium"
target_col = "Medium Close-Up"

min_length = 1.0
#min_length = 0.0

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
f_output = f'demo_{target_col}.mp4'

if os.path.exists(f_output):
    os.system(f'rm -vf {f_output}')


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
df = df[df['Length (seconds)'] >= min_length]
print(len(df))

movie = VideoFileClip(f_movie)

# Build subclips
subclips = [
    movie.subclip(t0, t1) for t0, t1 in
    tqdm(zip(df["Start Timecode"], df["End Timecode"]))
]

video = concatenate_videoclips(subclips)
print(video)
print(f"Wrote {video.duration:0.2f}s out of {movie.duration:0.2f}s")

video.write_videofile(f_output, fps=movie.fps, codec='libx264')
exit()
k = 7


t_start = df.iloc[k]["Start Timecode"]
t_end = df.iloc[k]["End Timecode"]
print(t_start, t_end)
c1 = clip.subclip(t_start, t_end)
c1.preview()
print(c1.duration)
print(dir(c1))
#c1.preview()
##help(clip)
exit()
#clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
#clip3 = VideoFileClip("myvideo3.mp4")
#final_clip = concatenate_videoclips([clip1,clip2,clip3])
#final_clip.write_videofile("my_concatenation.mp4")
print(df)
exit()


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
