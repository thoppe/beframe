import os
import h5py
from tqdm import tqdm
import imutils
import cv2
import numpy as np
import pandas as pd
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize

#f_movie = 'sample.avi'
f_movie = 'single_movie/Die.Hard.1988.720p.BRRip.x264-x0r.mkv'

assert(os.path.exists(f_movie))
stream = cv2.VideoCapture(f_movie)

estimated_total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(stream.get(cv2.CAP_PROP_FPS))

frame_capture_unit = FPS
labels = pd.read_csv("model/coco_labels.csv")

class SimpleConfig(Config):
    # give the configuration a recognizable name
    NAME = "coco_inference"
 
    # set the number of GPUs to use along with the number of images
    # per GPU
    NUM_CLASSES = len(labels)
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
        
# initialize the inference configuration
config = SimpleConfig()
 
# initialize the Mask R-CNN model for inference and then load the
# weights
print("[INFO] loading Mask R-CNN model...")
model = modellib.MaskRCNN(
    mode="inference", config=config,
    model_dir='model/'
)
model.load_weights('model/mask_rcnn_coco.h5', by_name=True)

save_dest = f"data/COCO/{f_movie}"
os.system(f"mkdir -p {save_dest}")

for n in tqdm(range(estimated_total_frames)):
     
    # grab the frame from the threaded video file stream
    (grabbed, frame) = stream.read()
  
    if not grabbed:
        break

    if n%frame_capture_unit > 0:
        continue

    f_save = os.path.join(save_dest, f"{n:08d}.npy")
    if os.path.exists(f_save):
        continue
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = imutils.resize(frame, width=450)
    cv2.imshow("Frame", frame)
    cv2.waitKey(100)

    #height, width, channels = img.shape
    #img = imutils.resize(img, width=width)
    
    # Perform a forward pass of the network to obtain the results
    results = model.detect([img], verbose=0)
    r = results[0]

    total_pixels = img.shape[0]*img.shape[1]
    frac = np.zeros(len(labels), dtype=float)

    n_objs = r["rois"].shape[0]
    for i in range(n_objs):
        frac[r['class_ids'][i]] += r['masks'][:, :, i].sum()

    frac /= total_pixels
    labels['frac'] = frac
    print(f"Frame {n}, {frac.sum():0.3f}")
    print(labels.sort_values('frac',ascending=False).head())
    
    np.save(f_save, frac)
    


    '''
    visualize.display_instances(
        img, r['rois'], r['masks'], r['class_ids'], 
        labels.values, r['scores']
    )
    '''
