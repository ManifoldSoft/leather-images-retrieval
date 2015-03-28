# -*- coding: utf-8 -*-
from pylab import *

from skimage.feature import local_binary_pattern
from PIL import Image

import os

# settings for LBP
METHOD = 'uniform'
radius = 2
n_points = 8 * radius


imgQuery = np.asarray(Image.open('testImg.png').convert('L'))

lbp = local_binary_pattern(imgQuery, n_points, radius, METHOD)

n_bins = lbp.max() + 1
hist, _ = np.histogram(lbp, normed=True, bins=n_bins, range=(0, n_bins))

figure()
gray()
subplot(1, 2, 1)
imshow(imgQuery, interpolation='nearest')
axis('off')

subplot(1, 2, 2)
imshow(lbp, interpolation='nearest')
axis('off')
    
show()

print ("lbp max %d \n" %lbp.max())
print ("Normalization hist is:")
print hist