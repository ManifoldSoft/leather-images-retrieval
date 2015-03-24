# -*- coding: utf-8 -*-

from __future__ import print_function

from pylab import *

from skimage.feature import local_binary_pattern
from tools.imtools import get_imlist
from PIL import Image

import os
from skimage import io

import os.path

import numpy as np

import pickle

# settings for LBP
METHOD = 'uniform'
radius = 2
n_points = 8 * radius

# 设置recall@number，即计算前多少的MAP
recallAtK = 100


def kullback_leibler_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    filt = np.logical_and(p != 0, q != 0)
    return np.sum(p[filt] * np.log2(p[filt] / q[filt]))


def match(refs, imgQuery):
    lbp = local_binary_pattern(imgQuery, n_points, radius, METHOD)
    n_bins = lbp.max() + 1
    hist, _ = np.histogram(lbp, normed=True, bins=n_bins, range=(0, n_bins))
    scores = []
    for index, ref in enumerate(refs):
        ref_hist, _ = np.histogram(ref, normed=True, bins=n_bins, range=(0, n_bins))
        score = kullback_leibler_divergence(hist, ref_hist)
        scores = scores + [score]
    rankResult = sorted(range(len(scores)), key=lambda k: scores[k])
    return rankResult

imgDBpath = './Brodatz/'
imlist = [os.path.join(imgDBpath,f) for f in os.listdir(imgDBpath)]

ref_feats = []

if os.path.exists('lbpFeature.pkl'):
    inputFeature = open('lbpFeature.pkl', 'rb')
    ref_feats = pickle.load(inputFeature)
    print("--- finish loading feature---")
else:
    for index, imName in enumerate(imlist):
        print("processing %s" % imName)
        img = np.asarray(Image.open(imName).convert('L'))
        imgLBP = local_binary_pattern(img, n_points, radius, METHOD)
        ref_feats = ref_feats + [imgLBP]
    outputFeature = open('lbpFeature.pkl', 'wb')
    pickle.dump(ref_feats, outputFeature)
    outputFeature.close()
    print("--- finish extracting lbp feature---")

f = open('queryImgs.txt', "r")
lines = [line.rstrip('\n') for line in f]
f.close()

g = open('Brodatz111classes.txt', "r")
classLabelsAndNum = [line.rstrip('\n') for line in g]
g.close()

classLabels = [line[:3] for line in classLabelsAndNum]

AP = np.zeros((len(lines),))

for idx, imName in enumerate(lines):
    queryPath = imgDBpath + imName
    imgQuery = np.asarray(Image.open(queryPath).convert('L'))
    rankRes = match(ref_feats, imgQuery)
    queryClass = imName[:3]
    rankIDs = rankRes[:recallAtK]
    right_query_results = 0
    precision = np.zeros((recallAtK,))
    for index, rankID in enumerate(rankIDs):
        # 显示查询结果，用于验证AP计算是否正确
        rank_index_class = os.path.basename(imlist[rankID])[:3]
        #ax = subplot(5, 1, index + 1)
        #ax.set_title(os.path.basename(imlist[rankID]))
        #rgbImg = io.imread(imlist[rankID])
        #axis('off')
        #imshow(rgbImg, interpolation='nearest')
        if queryClass == rank_index_class:
            right_query_results += 1
            precision[index] = right_query_results / float(index + 1)
        else:
            right_query_results += 0
            precision[index] = 0.
    #show()
    indexer = classLabels.index(queryClass)
    relateNums = classLabelsAndNum[indexer][4:]
    AP[idx] = np.sum(precision) / float(relateNums)
    print ("%s query's AP is %f" % (imName, AP[idx]))

mAP = np.sum(AP) / len(lines)
print ("mAP is %f" % mAP)
