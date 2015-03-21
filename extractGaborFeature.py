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

import pickle


def compute_feats(image, kernels):
    feats = np.zeros((len(kernels), 2), dtype=np.double)
    for k, kernel in enumerate(kernels):
        filtered = nd.convolve(image, kernel, mode='wrap')
        feats[k, 0] = filtered.mean()
        feats[k, 1] = filtered.var()
    return feats


# prepare filter bank kernels
kernels = []
for theta in range(5):                       # This parameter decides what kind of features the filter responds to.
    theta = theta / 5. * np.pi
    for sigma in (1, 3, 5, 9, 11, 13, 15, 17):       #  This parameter controls the width of the Gaussian envelope used in the Gabor kernel. Here are a few results obtained by varying this parameter.
        for frequency in (0.05, 0.25):
            kernel = np.real(gabor_kernel(frequency, theta=theta,
                                          sigma_x=sigma, sigma_y=sigma))  
            kernels.append(kernel)

# imlist = get_imlist('./leatherImgs/')
imlist = get_imlist('./Brodatz/')

shrink = (slice(0, None, 3), slice(0, None, 3))
# brick = img_as_float(data.load('brick.png'))[shrink] # numpy.ndarray类型
# grass = img_as_float(data.load('grass.png'))[shrink] # img_as_float为用255归一化到0-1
# wall = img_as_float(data.load('rough-wall.png'))[shrink]
# image_names = ('brick', 'grass', 'wall')
# images = (brick, grass, wall) # tuple类型
# prepare reference features
ref_feats = np.zeros((len(imlist), len(kernels), 2), dtype=np.double)
start_extractTime = time.time()
for index,imName in enumerate(imlist):
    print ("processing %s" % imName)
    img = img_as_float(np.asarray(Image.open(imName).convert('L')))[shrink]
    # img = img_as_float(io.imread(imName, as_grey=True))[shrink]
    ref_feats[index, :, :] = compute_feats(img, kernels) # ref_feats numpy.ndarray

outputFeature = open('gaborFeature.pkl', 'wb')
pickle.dump(ref_feats, outputFeature)
outputFeature.close()
print("--- finish extracting feature, it takes %s seconds ---" % (time.time() - start_extractTime))