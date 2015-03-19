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

# prepare filter bank kernels
kernels = []
for theta in range(4):
    theta = theta / 4. * np.pi
    for sigma in (1, 3):
        for frequency in (0.05, 0.25):
            kernel = np.real(gabor_kernel(frequency, theta=theta,
                                          sigma_x=sigma, sigma_y=sigma))
            kernels.append(kernel)

#imlist = get_imlist('./leatherImgs/')
imlist = get_imlist('./corel1k-thumbnails/')

shrink = (slice(0, None, 3), slice(0, None, 3))

imName = imlist[0]

print ("processing %s" % imName)
img = img_as_float(np.asarray(Image.open(imName).convert('L')))[shrink]
#img = img_as_float(io.imread(imName, as_grey=True))[shrink]
feats = np.zeros((len(kernels), 2), dtype=np.double)
for k, kernel in enumerate(kernels):
    filtered = nd.convolve(img, kernel, mode='wrap')
    plt.imshow(filtered)
    plt.gray()
    feats[k, 0] = filtered.mean()
    feats[k, 1] = filtered.var()
    print("--- the filtered image has %s mean, var is %s ---" % (feats[k, 0], feats[k, 1]))
    plt.show()
