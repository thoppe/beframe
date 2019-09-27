import os
import tempfile
import shutil
from tqdm import tqdm
import cv2

from scenedetect import FrameTimecode

def extract_clip(f_movie, f_save, t0, t1, is_high_quality=True):

    f_save = os.path.abspath(f_save)

    video = cv2.VideoCapture(f_movie)
    fps = video.get(cv2.CAP_PROP_FPS)
    T0 = FrameTimecode(t0, fps)
    T1 = FrameTimecode(t1, fps)

    T0 += 2
    print(T0)
    print(T0-1)
    print(T1, t1)

    quiet_args = " -hide_banner -loglevel panic "

    quiet_args = ""
    encode_args = "-c:v libx264 -c:a aac"

    cut_args = f'-vf select="between(n\,{t0}\,{t1}),setpts=PTS-STARTPTS"'
        
    cmd = (
        f"ffmpeg -y -ss {T0} -i {f_movie} -strict -2 -t {T1} -sn "
        f"{f_save}"
    )
    print(cmd)
    os.system(cmd)
    #exit()

def composite_video(f_movie, f_save, T0, T1, is_high_quality=True, cutoff=None):

    f_save = os.path.abspath(f_save)

    dest = tempfile.TemporaryDirectory()
    n_videos = len(T0)
    assert len(T0) == len(T1)

    if not is_high_quality:
        encode_args = "-vcodec libx264 -crf 27 -preset veryfast -c:a copy"
    else:
        encode_args = ""

    input_names = []
    quiet_args = " -hide_banner -loglevel panic "

    for i, (t0, t1) in tqdm(enumerate(zip(T0, T1)), total=n_videos):
        f_clip = os.path.join(dest.name, f"{i:08d}.mp4")
        cmd = (
            f"ffmpeg -i {f_movie} {encode_args} {quiet_args} "
            f"-ss {t0} -t {t1} {f_clip}"
        )
        
        os.system(cmd)

        f_clip = os.path.basename(f_clip)
        input_names.append(f"file '{f_clip}'")

        if cutoff and i >= cutoff:
            break

    org_dir = os.getcwd()
    os.chdir(dest.name)

    with open("inputs.txt", "w") as FOUT:
        FOUT.write("\n".join(input_names))

    cmd = f"ffmpeg -f concat -i inputs.txt -c copy output.mp4"
    os.system(cmd)
    
    #f_output = os.path.join(dest.name, f_save)
    shutil.move("output.mp4", f_save)
    os.chdir(org_dir)
    dest.cleanup()
