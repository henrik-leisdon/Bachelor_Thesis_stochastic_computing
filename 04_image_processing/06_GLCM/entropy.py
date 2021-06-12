import math
import random

import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

from skimage.filters.rank import entropy
from skimage.morphology import disk


def save_img(img_mat, img_name, img_num):
    result = Image.fromarray(img_mat)
    r = result.convert("L")
    r.save(str(img_name) + str(img_num) + ".png")


def calc_entropy(img):
    """shannon entropy: attempt 1"""
    # image = Image.open('c16.png').convert('L')
    # img = np.array(image)
    # print(img)
    # probability for every bit
    p_k = [0]*256
    for i in range(0, len(img)):
        for j in range(0, len(img[0])):
            p_k[int(img[i, j])] += 1

    # print(p_k)

    img_size = len(img)*len(img[0])

    H = 0
    normalize = 0
    # calculate shannon entropy
    for i in range(0, len(p_k)):

        if p_k[i] == 0:
            x = 0
        else:
            x = (p_k[i]/img_size)*math.log((p_k[i]/img_size), 2)
            normalize += 1
        H += x
    H = -H
    # H = H/normalize
    # print(H)
    return H


def calc_GLCM_entropy(img):
    """entropy of GLCM matrix"""
    # image = Image.open('cm_sp_original.jpg').convert('L')
    # img = np.array(image)

    glcm = np.zeros((256, 256))

    for i in range(0, len(img)-1):
        for j in range(0, len(img[0])):
            x = img[i, j]
            y = img[i+1, j]
            glcm[x, y] += 1

    H = 0
    normalize = 0
    num_pairs = (len(glcm[0])-1) * len(glcm)
    length = 0
    for i in range(0, len(glcm)):
        for j in range(0, len(glcm[0])):
            if glcm[i, j] == 0:
                x = 0
            else:
                x = (glcm[i, j]/num_pairs)*math.log((glcm[i, j]/num_pairs), 2)
                normalize += 1
            H += x
            length += 1
    H = -H
    # print(H)
    return H


def blocks(img):
    """method to split entropy into blocks
    :return: matrix of entropy blocks. The higher the entropy, the lower the weighting"""

    # imgplot2 = plt.imshow(img)
    # plt.show()
    e_list = []
    img = np.array(img)
    entr = np.zeros((len(img), len(img[0])))

    for i in range(0, len(img)-16, 16):
        for j in range(0, len(img[i])-16, 16):
            submat = img[i:i+16, j:j+16]
            entropy_e = calc_GLCM_entropy(submat)
            entrpy = entropy_e
            print(entrpy)
            e_list.append(entrpy)

    e_list = nomalize(e_list)

    it = 0
    for i in range(0, len(img) - 16, 16):
        for j in range(0, len(img[i]) - 16, 16):
            # print(entropy)
            for x in range(0, 16):
                for y in range(0, 16):
                    # print('i{}, j{}, x{}, y{} '.format(i, j, x, y))
                    entr[i+x, j+y] = e_list[it]*255
            it += 1

    save_img(entr, 'entropy_sh_gauss_', 0)
    # imgplot = plt.imshow(entr)
    # plt.show()
    # print(entr)
    return entr


def block8(img):
    """method to split entropy into blocks
    :return: matrix of entropy blocks. The higher the entropy, the lower the weighting"""

    # imgplot2 = plt.imshow(img)
    # plt.show()
    e_list = []
    img = np.array(img)
    entr = np.zeros((len(img), len(img[0])))

    for i in range(0, len(img)-8, 8):
        for j in range(0, len(img[i])-8, 8):
            submat = img[i:i+8, j:j+8]
            entropy_e = calc_GLCM_entropy(submat)
            entrpy = entropy_e
            # print(entrpy)
            e_list.append(entrpy)

    e_list = nomalize(e_list)

    it = 0
    for i in range(0, len(img) - 8, 8):
        for j in range(0, len(img[i]) - 8, 8):
            # print(entropy)
            for x in range(0, 8):
                for y in range(0, 8):
                    # print('i{}, j{}, x{}, y{} '.format(i, j, x, y))
                    entr[i+x, j+y] = e_list[it]*255
            it += 1

    save_img(entr, 'block8_', 0)
    # imgplot = plt.imshow(entr)
    # plt.show()
    # print(entr)
    return entr


def block_offset(img):
    """method to split entropy into blocks
    :return: matrix of entropy blocks. The higher the entropy, the lower the weighting"""

    # imgplot2 = plt.imshow(img)
    # plt.show()
    e_list = []
    img = np.array(img)
    entr = np.zeros((len(img), len(img[0])))

    for i in range(8, len(img)-24, 16):
        for j in range(8, len(img[i])-24, 16):
            submat = img[i:i+16, j:j+16]
            entropy_e = calc_GLCM_entropy(submat)
            entrpy = entropy_e
            # print(entrpy)
            e_list.append(entrpy)

    e_list = nomalize(e_list)

    it = 0
    for i in range(8, len(img) - 24, 16):
        for j in range(8, len(img[i]) - 24, 16):
            # print(entropy)
            for x in range(0, 16):
                for y in range(0, 16):
                    # print('i{}, j{}, x{}, y{} '.format(i, j, x, y))
                    entr[i+x, j+y] = e_list[it]*255
            it += 1

    # save_img(entr, 'offset_', 0)
    # imgplot = plt.imshow(entr)
    # plt.show()
    # print(entr)
    return entr


def combine_entr(img):
    img1 = blocks(img)
    img2 = block_offset(img)
    img = np.add(img1, img2)/2
    save_img(img, "combine_", 1)
    return img


def nomalize(e_list):
    max_val = max(e_list)
    min_val = min(e_list)

    normalized = []

    for element in e_list:
        # normal = (pow(element-min_val, 2))/pow(max_val-min_val, 2) # powered
        normal = (element - min_val) / (max_val - min_val)  # not powered

        print(normal)
        normalized.append(normal)

    return normalized


def main():
    image = Image.open('cm_sp_original.jpg').convert('L')
    # image = ImageOps.invert(image)
    # img = np.array(image)
    # blocks(image)
    block8(image)
    # combine_entr(image)
    # block_offset(image)
    # entropy_library()
    # entropy_copy()

if __name__ == '__main__':
    main()
