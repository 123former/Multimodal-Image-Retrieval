import re
import pandas as pd
import numpy as np
from irma_reader import *
from auc_ap import auc
import os
from autoencoder import autoencoder
from co_occurence import *

def euclidean(x,y):

    return np.sqrt(np.sum(np.square(x-y)))

vistex = get_vistex()

ipath_cache_file = os.path.join('cache', 'paths.pkl')

if os.path.isfile(ipath_cache_file):
    # print('Loading image paths from : ' + ipath_cache_file)
    with open(ipath_cache_file, 'rb') as f:
        ipath = cPickle.load(f)

def vistex_query():

    idx = np.random.randint(0,len(vistex))
    query_feature = vistex[idx]

    result = []
    for i,feature in enumerate(vistex):

        dis = euclidean(feature,query_feature)
        result.append((dis,ipath[i][:-4]))

    result = sorted(result)
    # print result
    return result,ipath[idx][:-4]

def evaluate(num_queries=10):

    class_info = pd.read_csv("ImageCLEFmed2009_train_codes.02.csv")
    class_i = np.array(class_info["05_class"])
    print class_i.shape

    class_count = {}

    for c in class_i:
        if not class_count.get(c):
            class_count[c] = 1
        else:
            class_count[c] += 1

    # print class_count
    get_class = {}
    path = "dataset/ImageCLEFmed2009_train.02/"

    for img_id,img_class in zip(class_info["image_id"],class_info["05_class"]):

        get_class[path+str(img_id)] = img_class
    
    # print get_class

    # model = ae_model()

    mAP = 0.0
    count = 0
    
    for i in range(num_queries):

        result,query = vistex_query()
        try:
            query_class = get_class[query]
        except:
            i = i-1
            continue
        
        count+=1
        print 'query class ',query_class
        print 'total relavant: ', class_count[query_class]
        simplified_result = []
        for x in result:
            # print x[1], get_class[x[1]]
            try:
                if(get_class[x[1]]==query_class):
                    simplified_result.append(1)
                else:
                    simplified_result.append(0)
            except:

                continue

        # print simplified_result
        
        AP = auc(simplified_result,class_count[query_class])
        print 'query ', i, ' AP : ', AP
        mAP+=AP
    
    mAP /= count

    print 'mAP : ', mAP
    return mAP

if __name__ == '__main__':

    # os.environ['CUDA_VISIBLE_DEVICES'] = ''
    # model = ae_model()
    # print model.query()

    evaluate(100)