import random

import numpy as np
from PIL import Image, ImageOps
import SNG
import MSC
import time
import entropy

"""
IDEA:
    split color image to RGB values, apply RC to every image
    add them up and divide by 3
"""
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

    def gen_seq(self, length, img_pow):
        start_time = 0
        # import image
        img_name = 'bau1_'
        num_ops = 0
        image = Image.open('bauhaus1_small.jpg')

        # entr_image = entropy.combine_entr(image, img_pow)/255

        img = Image.Image.split(image)

        img_r = img[0]
        img_g = img[1]
        img_b = img[2]

        # Image.Image.show(img_r)
        # Image.Image.show(img_g)
        # Image.Image.show(img_b)

        entr_r = entropy.combine_entr(img_r, img_pow)/255
        entr_g = entropy.combine_entr(img_g, img_pow) / 255
        entr_b = entropy.combine_entr(img_b, img_pow) / 255

        self.save_img(entr_r * 255, "entropy_r_", 0)
        self.save_img(entr_g * 255, "entropy_g_", 0)
        self.save_img(entr_b * 255, "entropy_b_", 0)

        sc_mat_r = self.processImage(img_r)
        sc_mat_g = self.processImage(img_g)
        sc_mat_b = self.processImage(img_b)

        r_out = np.multiply(sc_mat_r, entr_r)
        g_out = np.multiply(sc_mat_g, entr_g)
        b_out = np.multiply(sc_mat_b, entr_b)

        self.save_img(r_out * 255, "bau_red_", 0)
        self.save_img(g_out * 255, "bau_green_", 0)
        self.save_img(b_out * 255, "bau_blue_", 0)

        #  self.save_img(np.add(sc_mat_r, np.add(sc_mat_g, sc_mat_b)) / 3 * 255, img_name, 0)

        self.save_img(np.add(r_out, np.add(g_out, b_out)) / 3 * 255, img_name, 0)

        print("done im: " + str(0))
        print("--- %s seconds ---" % (time.time() - start_time))

        # compute entropy for 3 images

        # for every frame:
        for im_num in range(1, length):
            start_time = time.time()

            sc_mat_r = np.add(sc_mat_r, self.processImage(img_r))
            sc_mat_g = np.add(sc_mat_g, self.processImage(img_g))
            sc_mat_b = np.add(sc_mat_b, self.processImage(img_b))

            r_out = np.multiply(sc_mat_r, entr_r)
            g_out = np.multiply(sc_mat_g, entr_g)
            b_out = np.multiply(sc_mat_b, entr_b)

            self.save_img(r_out/(im_num+1) * 255, "bau_red_", im_num)
            self.save_img(g_out/(im_num+1) * 255, "bau_green_", im_num)
            self.save_img(b_out/(im_num+1) * 255, "bau_blue_", im_num)

            self.save_img(np.add(r_out, np.add(g_out, b_out))/(im_num+1) / 3 * 255, img_name, im_num)
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
