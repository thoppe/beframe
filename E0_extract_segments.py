import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from source.U1_smart_cuts import composite_video


#import cv2
#from imutils.video import VideoStream
#from moviepy.editor import VideoFileClip, concatenate_videoclips

#target_col = "Close-Up"
#target_col = "Extreme Wide"
#target_col = "Long"
#target_col = "Medium"
#target_col = "Medium Close-Up"
target_col = "Extreme Close-Up"

min_length = 1.0
#min_length = 0.0

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
f_output = f'demo_movies/demo_{target_col}.mp4'

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
print(df.columns)

T0 = df["Start Timecode"]
DURATION = df["Length (timecode)"]

composite_video(f_movie, f_output, T0, DURATION, False)

#print("HERE")
exit()

movie = VideoFileClip(f_movie)

# Build subclips
subclips = [
    movie.subclip(t0, t1) for t0, t1 in
    tqdm(zip(df["Start Timecode"], df["End Timecode"]))
]

video = concatenate_videoclips(subclips)
print(video)
print(f"Wrote {video.duration:0.2f}s out of {movie.duration:0.2f}s")

#help(video.write_videofile)

video.write_videofile(f_output, fps=movie.fps,
                      #codec='libx264',
                      codec='rawvideo',
                      ffmpeg_params=['-strict', '-2'],
                      #preset='veryslow',
                      #ffmpeg_params=['-crf', '18']
)
exit()

'''
k = 7
t_start = df.iloc[k]["Start Timecode"]
t_end = df.iloc[k]["End Timecode"]
print(t_start, t_end)
c1 = clip.subclip(t_start, t_end)
c1.preview()
print(c1.duration)
print(dir(c1))
'''
