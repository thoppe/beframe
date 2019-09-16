from shot_type_classifier.initialise import *
import glob
from tqdm import tqdm
import imutils
import cv2
from PIL import Image
import tempfile
import imageio

from PIL import Image as PImage
from fastai.vision import Image as fastImage
import io


# Currently getting 16 fps
#print(get_tfms())
#exit()

f_movie = 'single_movie/Die.Hard.1988.720p.BRRip.x264-x0r.mkv'
assert(os.path.exists(f_movie))
stream = cv2.VideoCapture(f_movie)

estimated_total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(stream.get(cv2.CAP_PROP_FPS))
frame_capture_unit = FPS
frame_capture_unit = 1


save_dest = f"data/shot_detection/{os.path.basename(f_movie)}"
os.system(f"mkdir -p {save_dest}")

f_data_save = os.path.join(save_dest, 'shots.csv')

##########################################################################

'''
f_model = "shot-type-classifier"
path = "shot_type_classifier/"

data = ImageDataBunch.from_folder(
    path,
    "train",
    "valid",
    size=(375, 666),
    #ds_tfms=get_tfms(),
    bs=1,
    #resize_method=ResizeMethod.SQUISH,  ### NOT Needed?
    #num_workers=0,
).normalize(imagenet_stats)


learn = cnn_learner(data, models.resnet50, metrics=[accuracy], pretrained=True)
learn = learn.to_fp16()
learn.load(f_model)
'''

learn = load_learner(
    'shot-type-classifier/models',
    file='shot-type-classifier.pkl'
)

print(learn)

##########################################################################


error = 0.0

stack = []
for n in tqdm(range(estimated_total_frames)):
     
    # grab the frame from the threaded video file stream
    try:
        (grabbed, frame) = stream.read()
    except:
        break

    if n < 907:
       continue


    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    '''
    pil_im = PImage.fromarray(frame) 
    x = pil2tensor(pil_im ,np.float32)
    preds_num = learn.predict(Image(x))[2].numpy()
    
    #pil = Image.fromarray(frame) 
    #x = pil2tensor(pil, np.float32)
    #preds_num = learn.predict(x)[2].numpy()
    print(preds_num)
    continue
    exit()
    '''
    
    #if n%frame_capture_unit > 0:
    #    continue



    with tempfile.NamedTemporaryFile(suffix='.jpg') as FOUT:
        imageio.imwrite(FOUT.name, frame)
        FOUT.flush()
        print(FOUT.name)
        os.system(f'eog {FOUT.name}')

        x = open_image(FOUT.name)
        print(x.data.shape)
        
        p0 = learn.predict(x)[2].numpy()
        # [3.246346e-03 9.929292e-01 1.588311e-03 ... ]
        
        img = PIL.Image.fromarray(frame).convert('RGB')
        img = pil2tensor(img, np.float32).div_(255) # Convert to torch.Tensor
        #print(img)
        img = fastImage(img) # Convert to fastai.vision.image.Image
        print(img.data.shape)

        #print(learn.predict(img)[0]) # --> Shot Type
        #print(learn.predict(img)[2]) # --> Probabilities
        p1 = learn.predict(img)[2].numpy()

        
        print(n, p0.dot(p1))
        error += 1 - p0.dot(p1)
        if n > 1000:break
        continue
        y = fastImage(np.transpose(frame,[2,0,1]))
        exit()
        #exit()
        preds_num = learn.predict(x)[2].numpy()

        # form data-frame
        item = dict(zip(data.classes, preds_num))
        item['frame_n'] = n
        #print(item)
        stack.append(item)

    print(preds_num)
    continue
    exit()
        
    #if len(stack) > 100:
    #    break
print(error)
exit()

df = pd.DataFrame(stack).set_index('frame_n')
print(df)
df.to_csv(f_data_save)
print(f_data_save)
