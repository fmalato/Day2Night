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


paths = [x[0] for x in os.walk('/home/fmalato/KAIST/')]
# Erasing all leaves
paths = [x for x in paths if x.endswith(('visible'))]
night = ['set03', 'set04', 'set05', 'set09', 'set10', 'set11']
paths = [x for x in paths if any(folder in paths for folder in night]
destination = 'datasets/Day2Night/trainB/'

for path in paths:
    print('%d/%d - Current path: %s    Destination: %s' % (num_path, len(paths), path, destination))
    num_path += 1
    files = os.listdir(path)
    count = 0
    for f in files:
        img = imread(f)
        img = imresize(img, (128, 160, 3))
        imsave(destination, img)
        if count+1 % 100 == 0:
            print('Processed: %d/%d' % (count, len(files)))
