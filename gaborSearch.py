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

shrink = (slice(0, None, 3), slice(0, None, 3))
#brick = img_as_float(data.load('brick.png'))[shrink] # numpy.ndarray类型
#grass = img_as_float(data.load('grass.png'))[shrink] # img_as_float为用255归一化到0-1
#wall = img_as_float(data.load('rough-wall.png'))[shrink]
#image_names = ('brick', 'grass', 'wall')
#images = (brick, grass, wall) # tuple类型
images = ()
for index,imName in enumerate(imlist):
    img = img_as_float(io.imread(imName, as_grey=True))[shrink]
    images = images+(img,)

# prepare reference features
#ref_feats = np.zeros((3, len(kernels), 2), dtype=np.double)
#ref_feats[0, :, :] = compute_feats(brick, kernels) # ref_feats numpy.ndarray
#ref_feats[1, :, :] = compute_feats(grass, kernels)
#ref_feats[2, :, :] = compute_feats(wall, kernels)
ref_feats = np.zeros((len(images), len(kernels), 2), dtype=np.double)
for index,im in enumerate(images):
    ref_feats[index, :, :] = compute_feats(im, kernels) # ref_feats numpy.ndarray

print('original: brick, match result: ', end='')
feats = compute_feats(images[1], kernels)
rankRes = rank(feats, ref_feats)

# Plot search result images

figure()
nbr_results = len(rankRes)
i = 1
for index in rankRes:
    subplot(5,floor(nbr_results/4),i)
    rgbImg = io.imread(imlist[index])
    imshow(rgbImg)
    axis('off')
    i = i+1
show()