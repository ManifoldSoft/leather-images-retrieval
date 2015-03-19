# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

from pylab import *

from skimage.transform import rotate
from skimage.feature import local_binary_pattern
from skimage import data
from tools.imtools import get_imlist
from PIL import Image

import os
from skimage import io

# settings for LBP
METHOD = 'uniform'
radius = 2
n_points = 8 * radius


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

imlist = get_imlist('./Brodatz/')

ref_feats = []

for index,imName in enumerate(imlist):
    print ("processing %s" % imName)
    img = np.asarray(Image.open(imName).convert('L'))
    imgLBP = local_binary_pattern(img, n_points, radius, METHOD)
    ref_feats = ref_feats+[imgLBP]

imgQuery = np.asarray(Image.open(imlist[120]).convert('L'))

rankRes = match(ref_feats, imgQuery)

# Plot search result images
figure()
nbr_results = len(rankRes)
i = 1
for index in rankRes:
    ax = subplot(5,4,i)
    ax.set_title(os.path.basename(imlist[index]))
    rgbImg = io.imread(imlist[index])
    imshow(rgbImg,interpolation='nearest')
    axis('off')
    i = i+1
    if i == 20:
        break
show()
