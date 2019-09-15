import os

is_debug = False

f_movie = "data/movies/Die.Hard.1988.720p.BRRip.x264-x0r.mkv"
save_dest = f"data/scene_change/{os.path.basename(f_movie)}"
os.system(f"mkdir -p {save_dest}")

cmd = [
    f'scenedetect --output {save_dest} --input {f_movie}',
]

if is_debug:
    cmd.append(f'time --start 300s --duration 900s',)

cmd.append(f'detect-content list-scenes save-images ')

cmd = ' '.join(cmd)

os.system(cmd)
print(cmd)

