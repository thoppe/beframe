from model.aesthetics.memnet.assessors.aestheticsnet import AestheticsNet
import model.aesthetics.memnet.utils.tensorflow
import tensorflow as tf
import numpy as np
import cv2
import pixelhouse as ph
from tqdm import tqdm
import pandas as pd


# Input layer
input_shape = (256, 256, 3)
image_input = tf.keras.Input(shape=input_shape)
model = AestheticsNet()
clf = model.aestheticsnet_fn(model.aestheticsnet_preprocess(image_input))

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
sess.run(tf.global_variables_initializer())

f_movie = 'single_movie/Die.Hard.1988.720p.BRRip.x264-x0r.mkv'
stream = cv2.VideoCapture(f_movie)

estimated_total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(stream.get(cv2.CAP_PROP_FPS))
frame_capture_unit = FPS

data = []

for n in tqdm(range(estimated_total_frames)):

    # grab the frame from the threaded video file stream
    try:
        (grabbed, frame) = stream.read()
    except:
        break

    if n%frame_capture_unit > 0:
        continue

    img = ph.Canvas(img=frame) #.rgb #.resize(0.25).rgb
    
    img = img.resize(output_size=(256,256)).rgb
    '''
    # Scale to the smallest of dimensions
    min_dim = min(img.shape[0], img.shape[1])
    scale = 256/min_dim
    img = img.resize(scale).rgb

    # Center crop
    remaining = max(img.shape[0], img.shape[1])  - 256
    img = img[:, remaining//2:remaining//2+256]
    
    '''
    imgs = np.array([img])
    res = sess.run(clf, feed_dict={image_input: imgs})

    for key in res:
        res[key] = res[key].ravel()[0]

    res['frame_n'] = n

    data.append(res)

    #if len(data)>1000:
    #    break
    
    '''
    # Make copies of the image across the larger dim
    # assume that width for now

    stride = max(img.shape[0], img.shape[1]) // (n_strides+2)
    imgs = [img[:, k*stride:k*stride+256][:,:256] for k in range(n_strides)]
    imgs = np.array(imgs)
    
    res = sess.run(clf, feed_dict={image_input: imgs})
    
    print(res)

    keys = res.keys()
    vals = np.array([res[k] for k in keys])
    vals = np.squeeze(vals)


    df = pd.DataFrame(data=vals, index=keys)
    print(df)
    exit()
    '''

df = pd.DataFrame(data).set_index('frame_n')
print(df)

df.to_csv("test_asethetics.csv")
