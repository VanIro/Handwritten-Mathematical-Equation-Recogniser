
import numpy as np
import keras
from matplotlib import pyplot as plt
import cv2

import pickle


from layout import *
from segmentation import get_parts_from_image2
from utils import *

modelI=keras.models.load_model('./models/model2OvSampled.keras')

label_indices=None
with open('label_indices_now.pickle','rb') as file:
    label_indices = pickle.load(file)

def recognise_parts(imgs,layout_seq, symb_imgs_store=None, model_pars=None):

    label_mapping = None
    model = None

    if not ( (model_pars is not None) and "model" in model_pars) :
            model=modelI
    else:
        if "mapping" in model_pars:
            label_mapping = model_pars["mapping"]
            model = model_pars["model"]
        else:
            model = modelI
    if label_mapping is None:
        label_mapping = label_indices
    s=[]
    for i in range(len(imgs)):
        if symb_imgs_store is not None:
            symb_imgs_store.append(imgs[i])
        imgs[i]=np.array(imgs[i])
        imgs[i]=imgs[i].reshape(1,28,28,1)
    #     result=modelI.predictclasses(train_data[i])
        prediction_scores = model.predict(imgs[i]).squeeze()  
#         prediction_scores.shape
        sorted_indices = sorted(range(len(prediction_scores)),key=lambda x:prediction_scores[x],reverse=True)
        labels = [label_mapping[k].split('/')[-2] for k in sorted_indices]
        result=np.argmax(prediction_scores, axis=0)
#         try:
#             s.append( labels_symbols[result]) #result[0]] )
#         except:
#             s.append(labels_symbols2[result]) #result[0]] )
        s.append(label_indices[result].split('/')[-2])
        
        
    return apply_layout(s,layout_seq)



def predict_image(img_path,display_parts=False,symb_imgs_store=None, model_pars=None):
    train_data, boxes, orig_img = get_parts_from_image2(img_path, display_img = False)
#     print(type(train_data))
    
#     print(orig_img.shape)
#     print(boxes)

    for i in range(len(boxes)-1,0,-1):
        overlap = get_overlap(boxes[i-1],boxes[i],dim=0)
        lengthi = boxes[i][1] - boxes[i][0]
        lengthip = boxes[i-1][1] - boxes[i-1][0]
                
        thresh_group = 0.95
        del_indices=[]
        if overlap/lengthi > thresh_group or  overlap/lengthip > thresh_group:
            #if heights don't overlap
            if get_overlap(boxes[i-1],boxes[i],dim=1) > 0 : continue
            
            #combine the two 
            comb_box = combine_boxes(boxes[i-1],boxes[i])
            #remove i and add it to i-1
            del boxes[i]
            
            boxes[i-1] = comb_box
            
            new_img = ~orig_img[comb_box[2]:comb_box[3]+1,comb_box[0]:comb_box[1]+1]
            
            train_data[i-1] = reshape_28_28(new_img)
            del train_data[i]
            
            # show_imgs_in_grid(1, [train_data[i-1]])
            # plt.show()
            # print(len(train_data))
        
#         for d in reversed(del_indices):
#             del boxes[d]
#             del train_data[d]
    
    layout_seq = get_layout2(boxes)
    
    # if display_parts:
    #     print(f"number of parts = {len(train_data)}")
    # plt.rcParams["figure.figsize"] = (20,2)
    # n_per_line = 10
    # if display_parts:
    #     show_imgs_in_grid(n_per_line,train_data)
    #     plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"] 
    #     plt.show()

    detected_exp = recognise_parts(train_data,layout_seq, symb_imgs_store = symb_imgs_store, model_pars=model_pars)

    if display_parts: 
        print(f"Detected Expression : {detected_exp}")
    
    return detected_exp


def make_prediction(img, model_pars=None):
        img_path = "./extracted_images/hellohi.jpg"
        cv2.imwrite(img_path,img)
        cached_img_path=img_path
        error_imgs_train_cache = []
        ans = predict_image(img_path, symb_imgs_store = error_imgs_train_cache, model_pars=model_pars)

        return str(ans)