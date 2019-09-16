import os
import tempfile
import shutil
from tqdm import tqdm

def composite_video(
        f_movie,
        f_save,
        T0, T1,
        is_high_quality=True,
):

    f_save = os.path.abspath(f_save)

    dest = tempfile.TemporaryDirectory()
    n_videos = len(T0)
    assert(len(T0) == len(T1))

    if is_high_quality:
        encode_args = "-vcodec libx264 -crf 27 -preset veryfast -c:a copy"
    else:
        encode_args = ""

    input_names = []
    
    for i, (t0, t1) in tqdm(enumerate(zip(T0,T1))):
        f_clip = os.path.join(dest.name, f"{i:08d}.mp4")
        cmd = f"ffmpeg -i {f_movie} {encode_args} -ss {t0} -t {t1} {f_clip}"
        os.system(cmd)

        f_clip = os.path.basename(f_clip)
        input_names.append(f"file '{f_clip}'")
        
        if i>=2:break
        
    f_input = os.path.join(dest.name, "inputs.txt")
    with open(f_input, 'w') as FOUT:
        FOUT.write('\n'.join(input_names))

    org_dir = os.getcwd()

    os.chdir(dest.name)
    cmd = f"ffmpeg -f concat -i inputs.txt -c copy output.mp4"    
    os.system(cmd)
    shutil.move('output.mp4', f_save)
    os.chdir(org_dir)
    
    #os.system("bash")
    dest.cleanup()
