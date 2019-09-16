import cv2
import os


class Streamer:
    def __init__(self, f_movie, frame_speed=None):

        assert os.path.exists(f_movie)
        self.stream = cv2.VideoCapture(f_movie)

        if not frame_speed:
            self.frame_capture_unit = 1
        else:
            self.frame_capture_unit = int(frame_speed * self.fps)

    @property
    def n_frames(self):
        return int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def fps(self):
        return self.stream.get(cv2.CAP_PROP_FPS)

    def __len__(self):
        return (self.n_frames) // self.frame_capture_unit

    def __iter__(self):
        n = 0
        while True:

            try:
                (grabbed, frame) = self.stream.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                break

            if not grabbed:
                break

            n += 1

            if n % self.frame_capture_unit > 0:
                continue

            yield n, frame
