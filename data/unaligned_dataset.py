import os.path
import torchvision.transforms as transforms
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import PIL
import random
import cv2
import imageio
import numpy as np
import torch


class UnalignedDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.dir_A = os.path.join(opt.dataroot, opt.phase + 'A')
        self.dir_B = os.path.join(opt.dataroot, opt.phase + 'B')
        self.no_input = opt.no_input
        self.A_paths = make_dataset(self.dir_A)
        self.B_paths = make_dataset(self.dir_B)

        self.A_paths = sorted(self.A_paths)
        self.B_paths = sorted(self.B_paths)
        self.A_size = len(self.A_paths)
        self.B_size = len(self.B_paths)
        self.transform = get_transform(opt)

        osize = [opt.loadSize, opt.loadSize * self.opt.input_nc]
        opt.fineSize * self.no_input * self.opt.input_nc
        self.transformA = []
        self.transformA.append(transforms.Resize((opt.fineSize * 2, opt.fineSize), Image.BICUBIC))
        self.transformA += [transforms.ToTensor(),
                            transforms.Normalize((0.5, 0.5, 0.5),
                                                 (0.5, 0.5, 0.5))]
        # self.transformA.append(transforms.RandomCrop((opt.fineSize,opt.fineSize*self.opt.input_nc) ))
        self.transformA = transforms.Compose(self.transformA)

    def __getitem__(self, index):
        A_path = self.A_paths[index % self.A_size]
        index_A = index % self.A_size
        index_B = random.randint(0, self.B_size - 1)
        B_path = self.B_paths[index_B]

        A_img = Image.open(A_path).convert('RGB') # A image is a no_input*3 collection of images
        A_img = (self.transformA(A_img))
        # I suppose this is for controlling the data size
        if self.no_input == 1:
            # Introducing a little redundancy to avoid changing the whole code
            # In case of a single input, the image is not splitted into two but simply copied
            # Also, given the dataset, 0:256 is RGB image while 256:512 is the IR image
            # To test day2nightOrig, it is necessary to set A_img[0] as 1 in the floowing lines
            A1 = A_img[:, 0:256, :]
            A2 = A_img[:, 0:256, :]
        else:
            A1 = A_img[:, 256:512, :]
            A2 = A_img[:, 256:512, :]

        A1 = A1.unsqueeze(0).numpy()
        A2 = A2.unsqueeze(0).numpy()
        A1 = np.squeeze(A1, axis=0)
        A2 = np.squeeze(A2, axis=0)
        B_img = Image.open(B_path)  # .convert('RGB')
        B = self.transform(B_img)
        if self.opt.which_direction == 'BtoA':
            input_nc = self.opt.output_nc
            output_nc = self.opt.input_nc
        else:
            input_nc = self.opt.input_nc
            output_nc = self.opt.output_nc

        # For now only support RGB
        # if input_nc == 1:  # RGB to gray
        #    tmp = A[0, ...] * 0.299 + A[1, ...] * 0.587 + A[2, ...] * 0.114
        #    A = tmp.unsqueeze(0)

        # if output_nc == 1:  # RGB to gray
        #    tmp = B[0, ...] * 0.299 + B[1, ...] * 0.587 + B[2, ...] * 0.114
        #    B = tmp.unsqueeze(0)
        return {'A1': A1, 'A2': A2, 'B': B,
                'A_paths': A_path, 'B_paths': B_path}

    def __len__(self):
        return max(self.A_size, self.B_size)

    def name(self):
        return 'UnalignedDataset'
