from PIL import Image
import numpy as np
import math
from matplotlib import pyplot as plt

def pad2square(img):
    shape = img.shape
    dim_smaller = -1
    if shape[0]<shape[1]:
        nLines = shape[1]-shape[0]
        dim_smaller=0
    elif shape[1]<shape[0]:
        nLines = shape[0]-shape[1]
        dim_smaller=1

    shape_pad =  (math.floor(nLines/2),shape[1-dim_smaller])
    if dim_smaller==1: shape_pad = shape_pad[::-1]
    pad1 = np.zeros(shape_pad)

    shape_pad = (math.ceil(nLines/2),shape[1-dim_smaller])
    if dim_smaller==1: shape_pad = shape_pad[::-1]
    pad2 = np.zeros(shape_pad)

    #pad --> pad1:img:pad2
    img2=np.append(pad1,img,axis=dim_smaller)
    img2=np.append(img2,pad2,axis=dim_smaller)
    
    return img2

def reshape_28_28(img):
    img2 = np.array(pad2square(img),dtype='uint8')
    img3 = np.array(Image.fromarray(img2).resize((28,28),Image.LANCZOS).getdata(),dtype='uint8').reshape(28,28)
    return img3


def show_imgs_in_grid(n_per_line,imgs):
    n_per_line = 10
    for i,part in enumerate(imgs):
        if i%n_per_line == 0 :
            fig, ax = plt.subplots(ncols = n_per_line)
            for x in ax: x.axis('off')
        ax[i%n_per_line].imshow(part, cmap='gray')
    plt.show()


def get_overlap(boxLRTB1,boxLRTB2,dim=0):#dim=0 for horizontal, 1 for vertical | box : L R T B
    if dim>1: dim=1
    i0,i1 = 0+2*dim,1+2*dim
    
    d2 = boxLRTB2[i1] - boxLRTB2[i0]
    
    dL12 = boxLRTB2[i0] - boxLRTB1[i0]
    if dL12<0: 
        d2+=dL12
        
    dR12 = boxLRTB2[i1] - boxLRTB1[i1]
    if dR12>0:
        d2-=dR12
    
    return d2

def combine_boxes(box1, box2): #box : L R T B
    box3=box1.copy()
    if box2[0]<box1[0]: box3[0] = box2[0]
    if box2[1]>box1[1]: box3[1] = box2[1]
    if box2[2]<box1[2]: box3[2] = box2[2]
    if box2[3]>box1[3]: box3[3] = box2[3]
    return box3