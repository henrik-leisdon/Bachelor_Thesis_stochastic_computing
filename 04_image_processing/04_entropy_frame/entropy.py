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
            # print('x {}, y {}'.format(x,y))
            glcm[x, y] += 1
            # print(glcm[x, y])

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
    print(H)
    return H


def blocks():
    """method to split entropy into blocks
    :return: matrix of entropy blocks. The higher the entropy, the lower the weighting"""
    image = Image.open('cm_sp_original.jpg').convert('L')
    image = ImageOps.invert(image)
    img = np.array(image)
    # imgplot2 = plt.imshow(img)
    # plt.show()
    e_list = []

    entr = np.zeros((len(img), len(img[0])))

    for i in range(0, len(img)-16, 16):
        for j in range(0, len(img[i])-16, 16):
            submat = img[i:i+16, j:j+16]
            entropy_e = calc_entropy(submat)
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



    save_img(entr, 'entropy_sh_', 3)
    # imgplot = plt.imshow(entr)
    # plt.show()
    return entr

def nomalize(e_list):
    max_val = max(e_list)
    min_val = min(e_list)

    normalized = []

    for element in e_list:
        normal = (element-min_val)/(max_val-min_val)
        # print(normal)
        normalized.append(normal)

    return normalized



def entropy_library():
    """usage of the scikit library (best entropy results)"""
    image = Image.open('cm_sp_original.jpg').convert('L')
    image = ImageOps.invert(image)
    img = np.array(image)

    entr_img = entropy(img, disk(10))
    print(entr_img)
    imgplot2 = plt.imshow(entr_img, cmap='viridis')
    plt.show()


def entropy_copy():
    """copy from the internet"""
    # code from: https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/basicFunctions.html
    colorIm = Image.open('cm_sp_original.jpg')
    greyIm = colorIm.convert('L')
    colorIm = np.array(colorIm)
    greyIm = np.array(greyIm)

    N = 5
    S = greyIm.shape
    E = np.array(greyIm)
    for row in range(S[0]):
        for col in range(S[1]):
            Lx = np.max([0, col - N])
            Ux = np.min([S[1], col + N])
            Ly = np.max([0, row - N])
            Uy = np.min([S[0], row + N])
            region = greyIm[Ly:Uy, Lx:Ux].flatten()
            E[row, col] = entropy_c(region)

    plt.subplot(1, 3, 1)
    plt.imshow(colorIm)

    plt.subplot(1, 3, 2)
    plt.imshow(greyIm, cmap=plt.cm.gray)

    plt.subplot(1, 3, 3)
    plt.imshow(E, cmap=plt.cm.jet)
    plt.xlabel('Entropy in 10x10 neighbourhood')
    plt.colorbar()

    plt.show()


def entropy_c(signal):
    '''
    function returns entropy of a signal
    signal must be a 1-D numpy array
    '''
    lensig = signal.size
    symset = list(set(signal))
    numsym = len(symset)
    propab = [np.size(signal[signal == i]) / (1.0 * lensig) for i in symset]
    ent = np.sum([p * np.log2(1.0 / p) for p in propab])
    return ent


def main():
    blocks()
    # entropy_library()
    # entropy_copy()

if __name__ == '__main__':
    main()
