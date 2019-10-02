# Run this first
# export GOOGLE_APPLICATION_CREDENTIALS="MovieTags-ce65c97a4c6b.json"

from tqdm import tqdm
import tempfile
import numpy as np
import io, os, sys, json
from source.pipeline import Pipeline

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "MovieTags-ce65c97a4c6b.json"
assert "GOOGLE_APPLICATION_CREDENTIALS" in os.environ

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()


def compute(f_wav, f1):
    print(f"Starting {f_wav}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as F:

        quiet = " -hide_banner -loglevel panic "
        cmd = f"ffmpeg {quiet} -y -i {f_wav} -ac 1 {F.name}"
        os.system(cmd)

    with io.open(F.name, "rb") as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        # sample_rate_hertz=48000,
        language_code="en-US"
    )

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    item = {
        "f_wav": f_wav,
        "n_results": len(response.results),
        "transcripts": [r.alternatives[0].transcript for r in response.results],
    }

    js = json.dumps(item, indent=2)
    print(js)

    with open(f1, "w") as FOUT:
        FOUT.write(js)


if __name__ == "__main__":

    # Get the framerate
    f_movie = sys.argv[1]
    assert os.path.exists(f_movie)

    name = os.path.basename(f_movie)
    save_dest = f"data/google_speech/{name}"
    load_dest = f"data/audio/{name}"

    P = Pipeline(
        load_dest=load_dest,
        save_dest=save_dest,
        old_extension="wav",
        new_extension="json",
        shuffle=False,
        # limit=3,
    )(compute, 1)
