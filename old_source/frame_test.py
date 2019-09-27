import cv2
import imutils
from tqdm import tqdm
import numpy as np
from imutils.video import FPS

# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

f_movie = 'sample.avi'
stream = cv2.VideoCapture(f_movie)

for _ in tqdm(range(4000)):

    # grab the frame from the threaded video file stream
    (grabbed, frame) = stream.read()
 
    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    # resize the frame and convert it to grayscale (while still
    # retaining 3 channels)
    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    # display a piece of text to the frame (so we can benchmark
    # fairly against the fast method)
    cv2.putText(frame, "Slow Method", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
