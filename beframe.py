"""Beframe

Usage:
  beframe.py shot <name>
  beframe.py join <name>

Options:
  --<name>      Movie filename
"""

from docopt import docopt
import os

if __name__ == '__main__':
    args = docopt(__doc__, version='Beframe 1.0')

    if args['shot']:
        pipeline = [
            'P1_shot_detection.py',
            'P2_scene_change.py',
            'P3_measure_scenes.py',
        ]

    elif args['join']:
        pipeline = [
            'E0_extract_segments.py',
            'E1_extract_audio.py',
            'E2_combine.py',
            'E3_detect_speech.py',
            'E4_build_subset.py',         
        ]
        pass

    f_movie = args['<name>']

    for call in pipeline:
        cmd = f'python {call} {f_movie}'
        print(cmd)
        os.system(cmd)
    
