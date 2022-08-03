

labels_symbols=dict()
for i in range(0,10):
    labels_symbols[i] = chr(48+i)
labels_symbols .update( {
    10:'-', 11:'+', 12:'*', 13:'=', 14:'A', 15:'b', 16:'<', 17:'>', 18:'/',19:'√', 20:'(',21:')'
})
symbols_folder = {'*':'times','/':'forward_slash','<':'lt','>':'gt','√':'sqrt'}#'(':'',')':''}

labels_symbols2 = {22:'C',23:'X',24:'y',25:'z',26:'alpha',27:'beta',
                  28:'gamma',29:'lambda',30:'Delta',31:'sigma',32:'theta', 33:'phi',34:'mu', 35:'N', 36:'u', 37:'v'}

labels_symbols.update(labels_symbols2)

exclude_symbols = []