import pandas as pd
import numpy as np
import os
import scipy.stats
from source.pipeline import Pipeline


def compute(f_shots, f1):
    name = os.path.basename(f_shots).split(".npy")[0]
    extension = name.split(".")[-1]

    f_scenes = os.path.join(
        "data/scene_change/", name, name.replace("." + extension, "-Scenes.csv")
    )

    if not os.path.exists(f_scenes):
        print(f"Missing {f_scene}")
        return False

    cols = [
        "Close-Up",
        "Extreme Close-Up",
        "Extreme Wide",
        "Long",
        "Medium",
        "Medium Close-Up",
    ]
    df = pd.DataFrame(data=np.load(f_shots), columns=cols, dtype=float)
    df.index.name = "frame_n"

    scenes = pd.read_csv(f_scenes, skiprows=1)

    # Fill in the scene information onto the shot dataframe
    df["scene_n"] = None
    df.loc[scenes["Start Frame"], "scene_n"] = scenes["Scene Number"].values
    df = df.fillna(method="ffill")

    # Compute an average over each shot type
    g = df.groupby("scene_n")

    for col in cols:
        scenes[col] = g[col].mean().values

    # Measure scene entropy
    entropy = []
    for _, dx in df.groupby("scene_n"):
        ent = [scipy.stats.entropy(q) for q in dx[cols].values]
        entropy.append(np.average(ent))
    scenes["frame_entropy"] = entropy

    scenes = scenes.set_index("Scene Number") #.round(4)

    scenes.to_csv(f1)#, float_format="%0.4f")
    print(f"Saved to {f1}")


P = Pipeline(
    load_dest="data/shot_detection",
    save_dest="data/info_scenes",
    old_extension="npy",
    new_extension="csv",
)(compute, 1)
