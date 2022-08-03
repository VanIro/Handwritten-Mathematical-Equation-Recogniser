

def get_layout2(boxes_seq): #box is L R T B
    layout_seq = [0]
    #print(boxes_seq)
    for i in range(1,len(boxes_seq)):
        base_leap = boxes_seq[i-1][3] - boxes_seq[i][3]
        cur_height = boxes_seq[i-1][3] - boxes_seq[i-1][2]
        if abs (base_leap/float(cur_height)) > 0.58:
            if(base_leap>0): layout_seq.append(1)
            else: layout_seq.append(-1)
        else:
            layout_seq.append(0)
    return layout_seq


import numpy as np
from pylatexenc.latex2text import LatexNodes2Text

normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-/*=()"
super_s = r"ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻′*⁼⁽⁾"

def apply_layout(string,layout_seq):
    # print(string)
    # print(layout_seq)
    # print("from layout")
    if False:#len(string)==0 and layout_seq==[0]:
        pass
    else:  assert len(layout_seq) == len(string)
    running_sup = False
    result=""
    for i in range(len(string)):
        if layout_seq[i]==1:
            running_sup = True
        if layout_seq[i]==-1:
            running_sup = False
        if running_sup:
            result =result + string[i].translate(string[i].maketrans(normal,super_s))
        else:
            result = result + string[i]
    return result