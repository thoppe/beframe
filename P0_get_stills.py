import imutils
import cv2
import os
from tqdm import tqdm
from PIL import Image


f_movie = 'single_movie/Die.Hard.1988.720p.BRRip.x264-x0r.mkv'

assert(os.path.exists(f_movie))
stream = cv2.VideoCapture(f_movie)

estimated_total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(stream.get(cv2.CAP_PROP_FPS))
frame_capture_unit = FPS

save_dest = f"data/frames/{f_movie}"
os.system(f"mkdir -p {save_dest}")

for n in tqdm(range(estimated_total_frames)):
     
    # grab the frame from the threaded video file stream
    (grabbed, frame) = stream.read()
  
    if not grabbed:
        break

    if n%frame_capture_unit > 0:
        continue
    
    f_save = os.path.join(save_dest, f"{n:08d}.jpg")
    if os.path.exists(f_save):
        continue

    # bgr to rgb
    frame = frame[...,::-1]

    img = Image.fromarray(frame)
    img.save(f_save)

