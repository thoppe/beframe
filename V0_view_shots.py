import pandas as pd
import pixelhouse as ph
import os

target_col = "Long"

df = pd.read_csv("DEMO.csv")

total_time = df["Length (seconds)"].sum() / 60
print(f"Total time {total_time:0.2f}")

df = df.sort_values("frame_entropy")
df = df[df["frame_entropy"] < 0.90]

entropy_vals = {
    "Extreme Close-Up": 0.2,
    "Close-Up": 0.2,  # Works well!
    "Extreme Wide": 0.6,  # Good, but entropy can be higher >= 0.4
    "Long": 0.6,  # Good, but entropy can be higher >= 0.4
    "Medium": 0.6,  # Good, multiple character interactions
    "Medium Close-Up": 0.6,  # Good, character interactions
}

cols = [
    "Extreme Close-Up",
    "Close-Up",  # Works well!
    "Extreme Wide",  # Good, but entropy can be higher >= 0.4
    "Long",  # Good, but entropy can be higher >= 0.4
    "Medium",  # Good, multiple character interactions
    "Medium Close-Up",  # Good, character interactions
]

for key in cols:
    dx = df[df[key] > 0.90]
    dx = dx[dx["frame_entropy"] < entropy_vals[key]]
    time = dx["Length (seconds)"].sum() / 60
    print(f"{key} total minutes {time:0.2f}")


df = df[df["frame_entropy"] < entropy_vals[target_col]]
df = df[df[target_col] > 0.90]

for _, row in df.iterrows():
    n = int(row["Scene Number"])

    for k in range(1, 4):
        f_img = f"data/scene_change/Die.Hard.1988.720p.BRRip.x264-x0r.mkv/Die.Hard.1988.720p.BRRip.x264-x0r-Scene-{n:04d}-{k:02d}.jpg"

        assert os.path.exists(f_img)
        c = ph.load(f_img)

        ex = row["frame_entropy"]
        c += ph.text(f"Entropy {ex:0.3f}", x=1.5, y=-1.5, font_size=0.25)

        ex = row[target_col]
        c += ph.text(f"{target_col} {ex:0.3f}", x=-1.5, y=-1.5, font_size=0.25)
        c.show()
