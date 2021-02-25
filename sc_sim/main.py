from fractions import Fraction
import random

# https://www.collindelker.com/2014/08/29/electrical-schematic-drawing-python.html for drawing circuits

# 1. build gates


class XOR:
    def __init__(self, tau, x, y):  # tau is the limit for iterations
        self.__tau = tau
        self.__x = x
        self.__y = y

    def get_tau(self):
        return self.__tau

    def l_xor(self):  # l_xor for logical xor
        if self.__x == 1 and self.__y == 1 or self.__x == 0 and self.__y == 0:
            return 0
        else:
            return 1


class AND:
    def __init__(self, tau):  # tau is the limit for iterations
        self.__tau = tau

    def get_tau(self):
        return self.__tau

    def set_tau(self, tau):
        self.__tau = tau

    @staticmethod
    def l_and(x, y):  # l_and for logical and
        if x == 1 and y == 1:
            return 1
        else:
            return 0


class NOR:
    def __init__(self, tau):  # tau is the limit for iterations
        self.__tau = tau

    def get_tau(self):
        return self.__tau

    def set_tau(self, tau):
        self.__tau = tau

    @staticmethod
    def l_nor(x, y):  # l_nor for logical nor
        if x == 0 and y == 0:
            return 1
        else:
            return 0


def l_not(x):
    if x == 0:
        return 1
    else:
        return 0


# 1.1 build stochastic main core
# 1.2 stochastic number generator

class InitialProbabilityCalculator:
    def __int__(self, p_e):
        self.__p_e = p_e


class StochasticNumberGenerator:
    def __init__(self, tau, input_y, stream_length):  # tau is the limit for iterations
        self.__tau = tau
        self.__input_y = input_y
        self.__bitstream = []
        self.__stream_length = stream_length

    def generate(self):
        frac = Fraction(self.__input_y)
        for i in range(0, self.__stream_length):
            m = random.randint(0, frac.denominator)
            if m < frac.numerator:
                self.__bitstream.append(1)
            else:
                self.__bitstream.append(0)
        return self.__bitstream


class WeightedStochasticNumberGenerator:    # in probability y_i
    def __init__(self, tau, input_y):  # tau is the limit for iterations
        self.__tau = tau
        self.__input_y = input_y

    def generate(self):
        probability = self.__input_y
        frac = Fraction(probability)
        list(bin(frac.numerator)[2:])
    # (probability).as_integer_ratio()
    # randbytes
    # from fractions import Fraction
    # Fraction(probability)

    # to binary: bin(number)

    # random numbers l_n:  0,1
    # n weight functions
    # w_n-1 = and(not(w_n), l_n-1)


class MainStochasticCore:
    def __init__(self, tau, bitlist_y):
        self.__tau = tau
        self.__bitlist_y = bitlist_y

    def calculate_core(self):
        xor_1 = XOR(self.__tau, self.__bitlist_y[2], self.__bitlist_y[3])
        xor_2 = XOR(self.__tau,y_o, y_3)
        xor_3 = XOR(self.__tau, y_0,y_2)
# 2. build queue

# 3. hardcode algorithm
