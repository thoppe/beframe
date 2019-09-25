import os
import tempfile
import shutil
from tqdm import tqdm


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
