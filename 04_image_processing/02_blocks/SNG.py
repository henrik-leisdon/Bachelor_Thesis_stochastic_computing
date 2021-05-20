import random


def gen_bit_const(input_gradient, r_num):
    """generates (pseudo) stochastic bit
    @:param input_bit: bit to generate a bitstream
    @:param r_num: random bit for every
    @:return: stochastic bistream for input bit"""
    # print('{}, {}'.format(r_num, input_gradient))
    if input_gradient == 255:
        return 1
    elif input_gradient == 0:
        return 0
    elif r_num < input_gradient:
        return 1
    else:
        return 0


def gen_bit(input_gradient):
    """generates (pseudo) stochastic bit
    @:param input_bit: bit to generate a bitstream for
    @:return: stochastic bistream for input bit"""
    r_num = random.randint(0, 255)
    # print('{}, {}'.format(r_num, input_gradient))
    if input_gradient == 255:
        return 1
    elif input_gradient == 0:
        return 0
    elif r_num < input_gradient:
        return 1
    else:
        return 0


class SngCompare:
    """simulates a stochastic number generator using a comperator
    """

    def __init__(self, name):
        self.name = name
