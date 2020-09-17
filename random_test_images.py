import random
import os

from PIL import Image
from scipy.misc import imsave


def select_images(num_test_images=50, path_imagesA='datasets/Day2Night/trainA/', path_imagesB='datasets/Day2Night/trainB/'):

    data_imagesA = os.listdir(path_imagesA)
    num_imagesA = len(data_imagesA) - 1
    data_imagesB = os.listdir(path_imagesB)
    num_imagesB = len(data_imagesB) - 1

    for x in range(num_test_images):
        imsave('test_images/testA/{x}.jpg'.format(x=x),
               Image.open('datasets/Day2Night/trainA/{img}'.format(img=data_imagesA[random.randint(0, num_imagesA)]))
               )
        imsave('test_images/testB/{x}.jpg'.format(x=x),
               Image.open('datasets/Day2Night/trainB/{img}'.format(img=data_imagesB[random.randint(0, num_imagesB)]))
               )


def move_images(results_folder, dst_folder):
    # Yes, it's hard coded.
    imgs = os.listdir('results/{rf}/test_latest/images/'.format(rf=results_folder))
    # Checking if the destination path exists: if it doesn't, generates it
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
        os.mkdir(dst_folder + '/AtoB')
        os.mkdir(dst_folder + '/BtoA')
        os.mkdir(dst_folder + '/AtoB/generated')
        os.mkdir(dst_folder + '/BtoA/generated')
        os.mkdir(dst_folder + '/AtoB/true')
        os.mkdir(dst_folder + '/BtoA/true')

    if results_folder == 'day2nightSoloIR' or results_folder == 'day2nightSoloRGB':
        # AtoB saving process
        print('Starting A to B saving process...')
        imgsAB = [x for x in imgs if 'real_A1' in x or 'fake_B' in x]
        for img in imgsAB:
            if 'real_A1' in img:
                imsave('{df}/AtoB/true/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
            else:
                imsave('{df}/AtoB/generated/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
        # BtoA saving process
        print('Starting B to A saving process...')
        imgsBA = [x for x in imgs if 'fake_A1' in x or 'real_B' in x]
        for img in imgsBA:
            if 'fake_A1' in img:
                imsave('{df}/BtoA/generated/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
            else:
                imsave('{df}/BtoA/true/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )

    elif results_folder == 'day2nightStd':
        # AtoB saving process
        print('Starting A to B saving process...')
        imgsAB = [x for x in imgs if 'real_A1' in x or 'real_A2' in x or 'fake_B' in x]
        for img in imgsAB:
            if 'real_A1' in img or 'real_A2' in img:
                imsave('{df}/AtoB/true/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
            else:
                imsave('{df}/AtoB/generated/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
        # BtoA saving process
        print('Starting B to A saving process...')
        imgsBA = [x for x in imgs if 'fake_A1' in x or 'fake_A2' or 'real_B' in x]
        for img in imgsBA:
            if 'fake_A1' in img or 'fake_A2' in img:
                imsave('{df}/BtoA/generated/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )
            elif 'real_B' in img:
                imsave('{df}/BtoA/true/{img}'.format(df=dst_folder, img=img),
                       Image.open('results/{rf}/test_latest/images/{img}'.format(rf=results_folder, img=img))
                       )


move_images('day2nightStd', 'FID/Std')
