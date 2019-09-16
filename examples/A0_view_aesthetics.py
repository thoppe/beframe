import pandas as pd
import pixelhouse as ph
import pylab as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("test_asethetics.csv")


key = "Aesthetic"
#key = "BalancingElement"
#key = "MotionBlur"
#key = "Light"
#key = "ColorHarmony"
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

plt.plot(df.frame_n, df[key])
plt.plot(df.frame_n, smooth(df[key], 10), 'k',)
plt.show()
exit()

df = df.sort_values(key)[::-1]

c = ph.Canvas()
for frame_n, val in zip(df.frame_n[:20], df[key][:20]):
    f_jpg = f'data/frames/single_movie/Die.Hard.1988.720p.BRRip.x264-x0r.mkv/{frame_n:08d}.jpg'
    
    c = ph.load(f_jpg)

    min_dim = min(c.img.shape[0], c.img.shape[1])
    scale = 256/min_dim
    #c = c.resize(scale)
    #c = c.resize(output_size=(256,256))

    # Center crop
    #remaining = max(c.img.shape[0], c.img.shape[1]) - 256
    #c.img = c.img[:, remaining//2:remaining//2+256]

    c += ph.text(f"frame:{frame_n}", font_size=0.25, y=-1.5)
    c += ph.text(f"{key}:{val:0.3f}", font_size=0.25, y=1.5)
    
    c.show(0)



