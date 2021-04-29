import copy
from fractions import Fraction

import numpy as np
from PIL import Image
import SNG
import MSC


# how to start:
# read image


def processImage(image):
    img = np.array(image)
    img_sto = np.zeros((16, 16))
    img_edg = np.zeros((16, 16))
    img_res = np.zeros((16, 16))
    msc = MSC.Circuit('msc')

    # for loop generate stochastic image
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            r_bit = SNG.gen_bit(img[i][j])
            img_sto[i][j] = r_bit

    # loop for edge detection

    for i in range(0, len(img_sto) - 1):
        for j in range(0, len(img_sto[i]) - 1):
            # run MSC
            msc.generate()
            sc = msc.run_circuit([img_sto[i][j], img_sto[i + 1][j + 1], img_sto[i + 1][j], img_sto[i][j + 1]])
            img_edg[i][j] = sc

    # TODO: loop convert sc image back to decimal values
    for i in range(0, len(img_edg)):
        for j in range(0, len(img_edg[i])):
            one_ctr = 0
            if img_edg[i][j] == 1:
                one_ctr += 1
            img_res[i][j] = one_ctr / len(img_edg[j]) * 255

    return img_edg


# image to probability

# probability to Stochastic binary string

# roberts cross operator

# convert back to binary/probability and scale back to image

def gen_seq(length):
    image = Image.open('seq_bw2/bw_2.png').convert('L')

    im1 = processImage(image)

    print(im1)
    result = Image.fromarray(im1*255)
    r = result.convert("L")
    r.save("seq" + str(0) + ".png")

    seq = [im1]
    for im_num in range(0, length):
        bin_image = processImage(image)
        seq.append(bin_image)

        out_image = np.zeros((16, 16))
        for i in range(0, len(im1)):
            for j in range(0, len(im1[i])):
                one_ctr = 0
                for k in range(0, len(seq)):
                    if seq[k][i][j] == 1:
                        one_ctr += 1
                out_image[i][j] = (one_ctr / len(seq)) * 255

        if im_num == 49:
            # print(out_image)
            print("done")
            result = Image.fromarray(out_image)
            r = result.convert("L")
            r.save("bw2_"+str(im_num+1)+".png")


def main():
    gen_seq(51)


if __name__ == '__main__':
    main()

"""
    image = Image.open('c16.png').convert('L')
    im1 = processImage(image)

    print(im1)
    result = Image.fromarray(im1*255)
    r = result.convert("L")
    r.save("sc_im0.png")

    im2 = processImage(image)

    im3 = [im1, im2]

    im_res = np.zeros((16, 16))
    for i in range(0, len(im1)):
        for j in range(0, len(im1[i])):

            one_ctr = 0
            for k in range(0, len(im3)):

                if im3[k][i][j] == 1:
                    one_ctr += 1
            im_res[i][j] = (one_ctr / 2) * 255

    print(im_res)
    result = Image.fromarray(im_res)
    r = result.convert("L")
    r.save("sc_im2.png")
"""