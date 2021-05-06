import copy
from fractions import Fraction

import numpy as np
from PIL import Image
import SNG
import MSC


def processImage(image):
    img = np.array(image)
    img_sto = np.zeros((len(img), len(img[0])))
    img_edg = np.zeros((len(img), len(img[0])))
    msc = MSC.Circuit('msc')

    # for loop generate stochastic image
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            r_bit = SNG.gen_bit(img[i][j])
            img_sto[i][j] = r_bit

    msc.gen_rc()
    # loop for roberts cross operator
    for i in range(0, len(img_sto) - 1):
        for j in range(0, len(img_sto[i]) - 1):
            # run MSC
            sc = msc.run_rc([img_sto[i][j], img_sto[i + 1][j + 1], img_sto[i + 1][j], img_sto[i][j + 1]])
            img_edg[i][j] = sc

    # output = binary rc mask
    return img_edg


def gen_seq(length):
    # import image
    img_name = 'ls_'
    image = Image.open('09 600x600_landscape/landscape_600.png').convert('L')

    # gen first image
    im1 = processImage(image)
    print(im1)
    result = Image.fromarray(im1*255)
    r = result.convert("L")
    r.save(img_name + str(0) + ".png")
    seq = [im1]

    out_image = np.zeros((len(im1), len(im1[0])))
    # generate n images
    for im_num in range(0, length):
        bin_image = processImage(image)
        seq.append(bin_image)

    # parallelize!
        for i in range(0, len(im1)):
            for j in range(0, len(im1[i])):
                one_ctr = 0
                for k in range(0, len(seq)):
                    if seq[k][i][j] == 1:
                        one_ctr += 1
                out_image[i][j] = (one_ctr / len(seq)) * 255
        print('img done')
        # if im_num == 30:
            # print(out_image)
        print("done im: " + str(im_num))
        save_img(out_image, img_name, im_num)


def save_img(img_mat, img_name, img_num):
    result = Image.fromarray(img_mat)
    r = result.convert("L")
    r.save(str(img_name) + str(img_num + 1) + ".png")


def main():
    gen_seq(30)


if __name__ == '__main__':
    main()

