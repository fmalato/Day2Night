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


paths = [x[0] for x in os.walk('/home/federico/Scrivania/KAIST/')]
#paths = [x[0] for x in os.walk('/Users/federico/fmalato/KAIST/')]
# Erasing all leaves
paths = [x for x in paths if x.endswith(('visible'))]
night = ['set03', 'set04', 'set05', 'set09', 'set10', 'set11']
destination = 'datasets/Day2Night/trainB/'
num_path = 1
count = 0

for path in paths:
    for folder in night:
        if folder in path:
            print('Current path: %s    Destination: %s' % (path, destination))
            num_path += 1
            files = os.listdir(path)
            if '.DS_Store' in files:
                files.remove('.DS_Store')
            for f in files:
                img = imread(path + '/' + f)
                # Useless, gets resized anyway
                # img = imresize(img, (128, 160, 3))
                imsave(destination + '{x}.jpg'.format(x=count), img)
                count += 1
                if count+1 % 100 == 0:
                    print('Processed: %d/%d' % (count, len(files)))
