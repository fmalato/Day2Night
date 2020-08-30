import glob
from scipy.misc import imread
from scipy.misc import imsave
from scipy.misc import toimage
from scipy.misc import imresize
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import os
"""paths = [x[0] for x in os.walk('/home/fmalato/KAIST/')]
# Erasing all leaves
paths = [x for x in paths if not x.endswith(('lwir', 'visible', 'labels'))]
# Erasing parent folders
paths = [x for x in paths if 'V0' in x]"""
#paths = ['/home/fmalato/KAIST/set01/V000/']
# Test
paths = ['imgs']
# Separating folders that contain daily images from the nightly ones
day = ['set00', 'set01', 'set02', 'set06', 'set07', 'set08']
num_path = 1
for path in paths:
    datasetA = path + '/visible/*.jpg'
    datasetB = path + '/lwir/*.jpg'
    # Choosing the right destination based on the current path
    if any(folder in path for folder in day):
        destination = 'datasets/Day2Night/trainA/'
    else:
        destination = 'datasets/Day2Night/trainA/'
    print('%d/%d - Current path: %s    Destination: %s' % (num_path, len(paths), path, destination))
    num_path += 1
    dataA = glob.glob(datasetA)
    dataA = sorted(dataA)
    dataB = glob.glob(datasetB)
    dataB = sorted(dataB)
    frames = len(os.listdir(datasetA.split('*')[0]))
    count = len(os.listdir(destination))
    count_proc = 0
    for i, j in zip(dataA, dataB):
        count += 1
        count_proc += 1
        img_A = imread(j)
        img_B = imread(i)
        img_A = imresize(img_A, size=(128, 160, 3))
        img_B = imresize(img_B, size=(128, 160, 3))
        line = img_A
        """out = np.zeros((np.shape(img_B)[0], np.shape(img_B)[1] * 2, 3))
        out[:, 0:np.shape(img_B)[1], 0] = img_B[:, :, 0]
        out[:, 0:np.shape(img_B)[1], 1] = img_B[:, :, 1]
        out[:, 0:np.shape(img_B)[1], 2] = img_B[:, :, 2]
        out[:, np.shape(img_B)[1]:2 * np.shape(img_B)[1], 0] = line[:, :, 0]
        out[:, np.shape(img_B)[1]:2 * np.shape(img_B)[1], 1] = line[:, :, 1]
        out[:, np.shape(img_B)[1]:2 * np.shape(img_B)[1], 2] = line[:, :, 2]"""
        out = np.zeros((np.shape(img_B)[0] * 2, np.shape(img_B)[1], 3))
        out[0:np.shape(img_B)[0], :, 0] = img_B[:, :, 0]
        out[0:np.shape(img_B)[0], :, 1] = img_B[:, :, 1]
        out[0:np.shape(img_B)[0], :, 2] = img_B[:, :, 2]
        out[np.shape(img_B)[0]:2 * np.shape(img_B)[0], :, 0] = line[:, :, 0]
        out[np.shape(img_B)[0]:2 * np.shape(img_B)[0], :, 1] = line[:, :, 1]
        out[np.shape(img_B)[0]:2 * np.shape(img_B)[0], :, 2] = line[:, :, 2]
        toimage(out, cmin=0, cmax=255).save(destination + str(count) + '.jpg')
        if count_proc % 100 == 0:
            print('    Processed: %d/%d' % (count_proc, frames))
    print('    Processed: %d/%d' % (count_proc, frames))
