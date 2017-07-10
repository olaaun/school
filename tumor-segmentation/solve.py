#!/usr/bin/env python
# Martin Kersner, 2016/01/13

from __future__ import division
import numpy as np

# make a bilinear interpolation kernel
# credit @longjon
def upsample_filt(size):
    factor = (size + 1) // 2
    if size % 2 == 1:
        center = factor - 1
    else:
        center = factor - 0.5
    og = np.ogrid[:size, :size]
    return (1 - abs(og[0] - center) / factor) * \
           (1 - abs(og[1] - center) / factor)

# set parameters s.t. deconvolutional layers compute bilinear interpolation
# N.B. this is for deconvolution without groups
def interp_surgery(net, layers):
    for l in layers:
        m, k, h, w = net.params[l][0].data.shape
        if m != k:
            print 'input + output channels need to be the same'
            raise
        if h != w:
            print 'filters need to be square'
            raise
        filt = upsample_filt(h)
        net.params[l][0].data[range(m), range(k), :, :] = filt

# init path
import os
import os.path as osp
#Note: Change address to your caffe build
caffe_root = '/home/olaaun/crfasrnn/crfasrnn/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)




# base net -- the learned coarser model
base_weights = 'TVG_CRFRNN_COCO_VOC.caffemodel'
solver = caffe.SGDSolver('solver.prototxt')

# do net surgery to set the deconvolution weights for bilinear interpolation
interp_layers = [k for k in solver.net.params.keys() if 'up' in k or 'score2' in k or 'score4' in k]
interp_surgery(solver.net, interp_layers)

# copy base weights for fine-tuning
solver.net.copy_from(base_weights)

#Uncomment if you wish to run in GPU mode
#solver.net.set_mode_gpu()
#solver.net.set_device(0)

for i in xrange(80000):
    solver.step(1)
