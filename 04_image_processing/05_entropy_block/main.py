import random

import numpy as np
from PIL import Image, ImageOps
import SNG
import MSC
import time
import entropy


class EdgeDetect:

    def __init__(self):
        self.msc = MSC.Circuit('msc')
        self.it = 0

    def processImage(self, image):
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

        # loop for roberts cross operator
        for i in range(0, len(img_sto) - 1):
            for j in range(0, len(img_sto[i]) - 1):
                # run MSC
                sc = self.msc.run_rc([img_sto[i][j], img_sto[i + 1][j + 1], img_sto[i + 1][j], img_sto[i][j + 1]])
                img_edg[i][j] = sc

        # print('process img: {}'.format(num_ops))
        return img_edg

    def gen_seq(self, length):
        # import image
        img_name = 'gauss_c_'
        num_ops = 0
        image = Image.open('gauss_noise_crop.png').convert('L')

        entr_image = entropy.blocks(image)/255

        # gen first image
        im1 = self.processImage(image)
        print(im1)
        result = Image.fromarray(im1 * 255)
        r = result.convert("L")
        r.save(img_name + str(0) + ".png")
        seq = [im1]

        start_time = 0

        out_image = np.zeros((len(im1), len(im1[0])))

        for im_num in range(0, length):
            start_time = time.time()
            bin_image = self.processImage(image)
            seq.append(bin_image)

            # convert stochastic matrices to greyscale image
            for i in range(0, len(im1)):
                for j in range(0, len(im1[i])):
                    one_ctr = 0
                    for k in range(0, len(seq)):
                        num_ops += 1
                        if seq[k][i][j] == 1:
                            one_ctr += 1

                    out_image[i][j] = (one_ctr / len(seq)) * 255
            out_image = np.multiply(out_image, entr_image)
            if im_num % 5 == 0:
                self.save_img(out_image, img_name, im_num)
            print("done im: " + str(im_num))
            print("--- %s seconds ---" % (time.time() - start_time))

    def save_img(self, img_mat, img_name, img_num):
        result = Image.fromarray(img_mat)
        r = result.convert("L")
        r.save(str(img_name) + str(img_num + 1) + ".png")


def main():
    ed = EdgeDetect()
    ed.gen_seq(50)


if __name__ == '__main__':
    main()
