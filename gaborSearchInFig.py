# -*- coding: utf-8 -*-

from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as nd

from skimage import data
from skimage.util import img_as_float
from skimage.filters import gabor_kernel

from tools.imtools import get_imlist
from skimage import io

# import PIL and pylab for plotting        
from PIL import Image
from pylab import *

import time
import os

import pickle


def compute_feats(image, kernels):
    feats = np.zeros((len(kernels), 2), dtype=np.double)
    for k, kernel in enumerate(kernels):
        filtered = nd.convolve(image, kernel, mode='wrap')
        feats[k, 0] = filtered.mean()
        feats[k, 1] = filtered.var()
    return feats


#def match(feats, ref_feats):
#    min_error = np.inf
#    min_i = None
#    for i in range(ref_feats.shape[0]):
#        error = np.sum((feats - ref_feats[i, :])**2)
#        if error < min_error:
#            min_error = error
#            min_i = i
#    return min_i

def rank(feats, ref_feats):
    dis = []
    for i in range(ref_feats.shape[0]):
        error = np.sum((feats - ref_feats[i, :])**2)
        dis = dis+[error]
    rankResult = sorted(range(len(dis)), key=lambda k: dis[k])
    return rankResult


# prepare filter bank kernels
kernels = []
for theta in range(4):
    theta = theta / 4. * np.pi
    for sigma in (1, 3):
        for frequency in (0.05, 0.25):
            kernel = np.real(gabor_kernel(frequency, theta=theta,
                                          sigma_x=sigma, sigma_y=sigma))
            kernels.append(kernel)

imlist = get_imlist('./leatherImgs/')

inputFeature = open('gaborFeature.pkl', 'rb')
ref_feats = pickle.load(inputFeature)
inputFeature.close()

img = img_as_float(np.asarray(Image.open(imlist[0]).convert('L')))

feats = compute_feats(img, kernels)
rankRes = rank(feats, ref_feats)

# Plot search result images
figure()
nbr_results = len(rankRes)
i = 1
for index in rankRes:
    ax = subplot(5,4,i)
    ax.set_title(os.path.basename(imlist[index]))
    rgbImg = io.imread(imlist[index])
    imshow(rgbImg)
    axis('off')
    i = i+1
    if i == 20:
        break
show()