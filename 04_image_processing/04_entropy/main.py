import random

import numpy as np
from PIL import Image, ImageOps
import SNG
import MSC
import time
import concurrent.futures


class EdgeDetect:

    def __init__(self):
        self.msc = MSC.Circuit('msc')
        self.it = 0

    def processImage(self, image):
        num_ops = 0
        img = np.array(image)
        img_sto = np.zeros((len(img), len(img[0])))
        img_edg = np.zeros((len(img), len(img[0])))
        self.msc.gen_rc()

        # for loop generate stochastic image
        r_num = random.randint(0, 255)
        for i in range(0, len(img)):
            for j in range(0, len(img[i])):
                r_bit = SNG.gen_bit_const(img[i][j], r_num)
                img_sto[i][j] = r_bit
            num_ops += 1

        # loop for roberts cross operator
        for i in range(0, len(img_sto) - 1):
            for j in range(0, len(img_sto[i]) - 1):
                # run MSC
                sc = self.msc.run_rc([img_sto[i][j], img_sto[i + 1][j + 1], img_sto[i + 1][j], img_sto[i][j + 1]])
                img_edg[i][j] = sc
                num_ops += 1 + 16  # for msc interations

        # print('process img: {}'.format(num_ops))
        return img_edg

    def gen_seq(self, length):
        # import image
        img_name = 'cm_'
        num_ops = 0
        image = Image.open('camera_man.png').convert('L')


        # gen first image
        im1 = self.processImage(image)
        print(im1)
        result = Image.fromarray(im1 * 255)
        r = result.convert("L")
        r.save(img_name + str(0) + ".png")
        sc_mat = im1

        start_time = 0
        # for loop for every frame
        for im_num in range(0, length):
            start_time = time.time()
            bin_image = self.processImage(image)

            # add matrix, then divide by number of frames and resize to grayscale image
            sc_mat = np.add(sc_mat, bin_image)
            self.save_img((sc_mat/(im_num+2))*255, img_name, im_num)

            print("done im: " + str(im_num))
            print("--- %s seconds ---" % (time.time() - start_time))
            # print('generate seq: {}'.format(num_ops))  # number of operations

    def save_img(self, img_mat, img_name, img_num):
        result = Image.fromarray(img_mat)
        r = result.convert("L")
        r.save(str(img_name) + str(img_num + 1) + ".png")


def main():
    ed = EdgeDetect()
    ed.gen_seq(20)


if __name__ == '__main__':
    main()
