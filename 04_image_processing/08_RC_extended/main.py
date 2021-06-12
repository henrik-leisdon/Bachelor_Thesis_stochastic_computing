import random

import numpy as np
from PIL import Image, ImageOps
import SNG
import MSC
import time
import entropy


"""
IDEA: 
    generate the normal diagonal roberts cross operator and a version with the linear operator
    add them up and take the average of both
    -> thats the result
"""

class EdgeDetect:

    def __init__(self):
        self.msc = MSC.Circuit('msc')
        self.it = 0

    def processImage(self, image, method):
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
                sc = 0
                # run MSC
                # diagonal roberts cross
                if method == 1:
                    sc = self.msc.run_rc([img_sto[i][j], img_sto[i + 1][j + 1], img_sto[i + 1][j], img_sto[i][j + 1]])
                # linear roberts cross
                if method == 2:
                    sc = self.msc.run_rc([img_sto[i][j], img_sto[i + 1][j], img_sto[i][j], img_sto[i][j + 1]])
                img_edg[i][j] = sc

        # print('process img: {}'.format(num_ops))
        return img_edg

    def gen_seq(self, length, img_pow):
        start_time = 0
        # import image
        img_name = 'bau2_dl_'
        num_ops = 0
        img = Image.open('rsz_bauhaus2.jpg').convert('L')

        # Image.Image.show(img_r)
        # Image.Image.show(img_g)
        # Image.Image.show(img_b)

        entr = entropy.combine_entr(img, img_pow)/255

        self.save_img(entr * 255, "entropy", 0)

        sc_mat_d = self.processImage(img, 1)
        sc_mat_l = self.processImage(img, 2)

        d_out = np.multiply(sc_mat_d, entr)
        l_out = np.multiply(sc_mat_l, entr)

        self.save_img(d_out * 255, "bau_diagonal_", 0)
        self.save_img(l_out * 255, "bau_linear_", 0)

        #  self.save_img(np.add(sc_mat_r, np.add(sc_mat_g, sc_mat_b)) / 3 * 255, img_name, 0)

        self.save_img(np.add(l_out, d_out) / 2 * 255, img_name, 0)

        print("done im: " + str(0))
        print("--- %s seconds ---" % (time.time() - start_time))

        # compute entropy for 3 images

        # for every frame:
        for im_num in range(1, length):
            start_time = time.time()

            sc_mat_d = np.add(sc_mat_d, self.processImage(img, 1))
            sc_mat_l = np.add(sc_mat_l, self.processImage(img, 2))

            d_out = np.multiply(sc_mat_d, entr)
            l_out = np.multiply(sc_mat_l, entr)
            if im_num % 5 == 0 or im_num < 10:
                self.save_img(d_out/(im_num+1) * 255, "bau_diagonal_", im_num)
                self.save_img(l_out/(im_num+1) * 255, "bau_linear_", im_num)

                self.save_img(np.add(d_out, l_out) / (im_num+1) / 2 * 255, img_name, im_num)
            # self.save_img(np.add(sc_mat_r, np.add(sc_mat_g, sc_mat_b))/im_num / 3 * 255, img_name, im_num)

            print("done im: " + str(im_num))
            print("--- %s seconds ---" % (time.time() - start_time))
    # def gen_frame(self, ):

    def save_img(self, img_mat, img_name, img_num):
        result = Image.fromarray(img_mat)
        r = result.convert("L")
        r.save(str(img_name) + str(img_num) + ".png")

def main():
    # get_best_theshold()
    ed = EdgeDetect()
    ed.gen_seq(30, 1)


if __name__ == '__main__':
    main()
