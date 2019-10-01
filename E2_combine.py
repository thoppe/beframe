import os, sys, glob
import cv2
from tqdm import tqdm
from source.pipeline import Pipeline

# Get the framerate
f_movie = sys.argv[1]
assert os.path.exists(f_movie)
stream = cv2.VideoCapture(f_movie)
FPS = float(stream.get(cv2.CAP_PROP_FPS))

name = os.path.basename(f_movie)
save_dest = f"data/rendered_clips/{name}"
load_dest = f"data/clips/{name}"

def compute(f_audio, f_save):
    print(f"Starting {f_audio} {f_save}")

    scene_n = int(os.path.basename(f_audio).split('.')[0])
    f_clips = os.path.join(load_dest, f"{scene_n:04d}_%06d.png")
    #f_save = os.path.join(save_dest, f"{scene_n:04d}.mp4")

    quiet =" -hide_banner -loglevel panic "
    
    cmd = f"ffmpeg {quiet} -y -r {FPS} -i {f_clips} -i {f_audio} -c:v libx264 -preset slow -profile:v high -crf 18 -coder 1 -pix_fmt yuv420p -movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low {f_save}"

    os.system(cmd)


P = Pipeline(
    load_dest=load_dest,
    save_dest=save_dest,
    old_extension="wav",
    new_extension="mp4",
    shuffle=False,
)(compute, 1)
