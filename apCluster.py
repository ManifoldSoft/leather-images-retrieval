# -*- coding: utf-8 -*-
# Ref:http://scikit-learn.org/stable/auto_examples/cluster/plot_affinity_propagation.html

from tools.imtools import get_imlist
from pylab import *
import pickle
import numpy as np
from sklearn.cluster import AffinityPropagation

imlist = get_imlist('./leatherImgs/')

inputFeature = open('lbpFeature.pkl', 'rb')
feats = pickle.load(inputFeature)
inputFeature.close()

maxBins = []
for index, ref in enumerate(feats):
    tmp = ref.max()
    maxBins = maxBins + [tmp]

n_bins = max(maxBins) + 1
hists, _ = np.histogram(feats[0], normed=True, bins=n_bins, range=(0, n_bins))

for feat in feats[1::]:
    ref_hist, _ = np.histogram(feat, normed=True, bins=n_bins, range=(0, n_bins))
    hists = np.vstack((hists, ref_hist))

# Compute Affinity Propagation
af = AffinityPropagation(preference=0.5).fit(hists)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

for k in range(n_clusters_):
    class_members = labels == k
    cluster_center = hists[cluster_centers_indices[k]]
    print ("class members:%s,cluster center:%s" % (class_members, cluster_center))