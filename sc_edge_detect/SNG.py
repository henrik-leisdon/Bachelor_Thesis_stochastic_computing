import random


def gen_bit(input_gradient):
    """generates (pseudo) stochastic bitstream
    @:param input_bit: bit to generate a bitstream for
    @:return: stochastic bistream for input bit"""
    r_num = random.randint(0, 255)
    if r_num < input_gradient:
        return 1
    else:
        return 0


class SngCompare:
    """simulates a stochastic number generator using a comperator
    """

    def __init__(self, name):
        self.name = name
