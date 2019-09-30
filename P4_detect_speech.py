from tqdm import tqdm
import numpy as np
import os, glob, subprocess, tempfile
import sys, json
from source.U1_smart_cuts import extract_audio
from source.pipeline import Pipeline

f_movie = sys.argv[1]
assert os.path.exists(f_movie)


def deepspeech(f_audio):

    base_cmd = "deepspeech --model models/deepspeech-0.5.1-models/output_graph.pbmm --alphabet models/deepspeech-0.5.1-models/alphabet.txt --lm models/deepspeech-0.5.1-models/lm.binary --trie deepspeech-0.5.1-models/trie "

    cmd = f"{base_cmd}  --audio {f_audio}"
    info = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)

    return info.decode()


def compute(f0, f1):

    with tempfile.NamedTemporaryFile(suffix=".wav") as FOUT:
        extract_audio(f0, FOUT.name)
        cmd = f"ffmpeg-normalize -f {FOUT.name} -nt peak -t 0 -o {FOUT.name}"
        subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)

        text = deepspeech(FOUT.name)

    js = {"f_clip": f0, "text": text}
    js = json.dumps(js, indent=2)

    print(js)

    with open(f1, "w") as FOUT:
        FOUT.write(js)


def safe_compute(*args):
    try:
        compute(*args)
    except Exception as EX:
        print(f"Failed with {EX}")


name = os.path.basename(f_movie)
F_CLIPS = sorted(glob.glob(f"data/clips/{name}/*"))

P = Pipeline(
    load_dest=F_CLIPS,
    save_dest=f"data/deepspeech/{name}",
    new_extension="json",
    save_only=True,
)(safe_compute, 8)
