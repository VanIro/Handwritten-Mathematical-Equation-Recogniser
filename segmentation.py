import numpy as np
import cv2
import copy
import matplotlib.pyplot as plt

from utils import *


extracted_boxes = None
extracted_imgs = None

def get_parts_from_image2(path, display_img = False ):
    img=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    img=img[:int(img.shape[0]*0.995),:int(img.shape[1]*0.995)]
    ret_img = img.copy()
    #print(img.shape)
    if display_img :
        print(path)
        plt.axis('off')
        plt.imshow(~img,cmap='gray')
        plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    imgs,boxes = extract_regions(img)
    global extracted_boxes
    global extracted_imgs
    extracted_boxes = list(boxes)
    #convert images to square size by padding, before resizing them
    for i,img in enumerate(imgs):
#         show_imgs_in_grid(1,[img])
        img2 = pad2square(img).astype('uint8') 
        img3 = np.array(Image.fromarray(img2).resize((28,28),Image.LANCZOS).getdata(),dtype='uint8').reshape(28,28)
#         print(np.unique(img3,return_counts=True))
        ret,img4 = cv2.threshold(img3,10,255,cv2.THRESH_BINARY)
        img4 = img4*0.7+img3*0.3
        imgs[i] = img4
#         print('get_parts_from_image2')
#         show_imgs_in_grid(3,[img2,img3,img4])
        
    extracted_imgs = copy.copy(imgs)
    return imgs, boxes, ret_img





save_imgs_path = r'.\extracted_images'

def extract_regions(img_in,save_imgs_path=save_imgs_path): #returns bounding boxes of extracted regions and saves those regions 
                                         #in a new image in path arg[1]
    img= copy.copy(img_in)
    img=~img
    ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    img = thresh
#     plt.axis('off')
#     plt.imshow(img,cmap='gray')
#     plt.show()
    img_count=0
    bounding_boxes = []
    imgs_segmented = []
    for i in range(img.shape[0]):#along y
        #print(i)
        for j in range(img.shape[1]):#along x
            if img[i][j]==0:
                continue
            else:
                #start new
                #print("-->",img_count)
                new_img = np.zeros((img.shape[0]-i,img.shape[1]))
                #print(new_img.shape)
                boundary = [(j,i)]
                bounding_box=[j,j,i,i] #L R T B
                max_len_boundary = 0  #just for info
                n_iters = 0  #just for info
                while len(boundary)>0:
                    n_iters+=1
                    ##print("***",len(boundary))
                    if(len(boundary)>max_len_boundary):
                        max_len_boundary = len(boundary)
                    x,y = boundary.pop()
                    img[y][x]=0
                    new_img[y-i][x]=255

                    #update bounding box
                    if x<bounding_box[0]:
                        bounding_box[0]=x
                    elif x>bounding_box[1]:
                        bounding_box[1]=x

                    if y<bounding_box[2]:
                        bounding_box[2]=y
                    elif y>bounding_box[3]:
                        bounding_box[3]=y

                    #expand boundary if possible
                    for dx in [0,-1,1]:
                        for dy in [0,-1,1]:
                            if (y==0 and dy==-1) or (y == img.shape[0]-1 and dy==1): continue
                            if (x==0 and dx==-1) or (x == img.shape[1]-1 and dx==1): continue
                            if img[y+dy][x+dx]>0: #and new_img[i+dy][j+dx]==0:
                                boundary.append((x+dx,y+dy))

                #print("*** max boundary size = ",max_len_boundary)
                #print("*** no. of iterations = ",n_iters)
                #save new_img and associate it with a bounding box
                bounding_boxes.append(copy.copy(bounding_box))
                ##print(f'[:{bounding_box[3]-i},{bounding_box[0]}:{bounding_box[1]}]')
                img_segment = new_img[:bounding_box[3]-i,
                                    bounding_box[0]:bounding_box[1]]
                cv2.imwrite(save_imgs_path+'/extracted_region_{}.bmp'.format(img_count), img_segment)
                
                #img_segment_resized = cv2.resize(img_segment,(28,28))
                #imgs_segmented.append(img_segment_resized)
                imgs_segmented.append(img_segment)
                img_count+=1
    
    sorted_indicesL2R = sorted(range(len(bounding_boxes)),key=lambda i : bounding_boxes[i][0],reverse=False)
    imgs_segmented = [imgs_segmented[i] for i in sorted_indicesL2R]
    bounding_boxes = [bounding_boxes[i] for i in sorted_indicesL2R]
    return imgs_segmented, bounding_boxes


import os
import glob

def remove_temp_extracted_image_segments():
    file_list = glob.glob(save_imgs_path + r'\extracted_region_*.bmp')
    for file in file_list:
        os.remove(file)