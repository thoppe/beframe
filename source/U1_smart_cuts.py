import os, subprocess
import tempfile
import shutil
from tqdm import tqdm
import cv2

# from scenedetect import FrameTimecode
# def extract_clip(f_movie, f_save, t0, t1, keyframes, is_high_quality=True):


def extract_audio(f_movie, f_output):
    # low_res is for deepspeech
    quiet_args = " -hide_banner -loglevel panic "
    cmd = f"ffmpeg -y -i {f_movie} -f wav -ac 1 -ar 16000 -vn {f_output} {quiet_args}"
    os.system(cmd)


def extract_clip(f_movie, f_save, row):

    f_save = os.path.abspath(f_save)

    t0 = row["Start Timecode"]
    t1 = row["End Timecode"]

    fn0 = row["Start Frame"]
    fn1 = row["End Frame"]
    total_frames = fn1 - fn0

    # Find the first keyframe that captures this

    # video = cv2.VideoCapture(f_movie)
    # fps = video.get(cv2.CAP_PROP_FPS)
    # print(keyframes)

    duration = row["Length (timecode)"]
    quiet_args = " -hide_banner -loglevel panic "

    # Exactly two extra frames: FAST
    # encode_args = f'-ss {t0} -i {f_movie} -to {duration}'

    # Exactly two extra frames: Slower (still pretty fast)
    # encode_args = f'-i {f_movie} -ss {t0} -to {t1}'

    # OK, but sometimes video drops completely: FAST
    encode_args = f"-i {f_movie} -ss {t0} -to {t1} -c copy"
    # encode_args = f'-ss {t0} -i {f_movie} -to {duration} -c copy'

    # Check the file, if not video try to extract again?
    cmd = f"ffmpeg -y {encode_args} {quiet_args} {f_save}"
    os.system(cmd)

    stream_info = check_video_stream(f_save)

    if not len(stream_info):
        # Not perfect but usually fixes?
        # Try a second clip method if there is only audio?
        encode_args = f"-ss {t0} -i {f_movie} -c copy -frames:v {total_frames}"
        cmd = f"ffmpeg -y {encode_args} {quiet_args} {f_save}"
        os.system(cmd)

    expected_duration = row["Length (seconds)"]
    new_duration = float(check_duration(f_save))

    time_delta = abs(expected_duration - new_duration)

    if time_delta > 0.5:
        print(f"Failed to extract clip {f_save}, time mismatch")
        os.unlink(f_save)


def check_video_stream(f0):

    cmd = f"ffprobe -i {f0} -show_streams -select_streams v -loglevel error"

    info = subprocess.check_output(cmd, shell=True)
    # print(f"Couldn't read video stream {f0}")

    return info.strip()


def check_duration(f0):

    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1 {f0}"

    info = subprocess.check_output(cmd, shell=True)
    info = str(info.strip()).split("=")[-1].strip("'")
    return info


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

    # f_output = os.path.join(dest.name, f_save)
    shutil.move("output.mp4", f_save)
    os.chdir(org_dir)
    dest.cleanup()
