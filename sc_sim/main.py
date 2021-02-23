# 1. build gates

class XOR:
    def __init__(self, tau):  # tau is the limit for iterations
        self.__tau = tau

    def get_tau(self):
        return self.__tau

    def set_tau(self, tau):
        self.__tau = tau

    @staticmethod
    def l_xor(x, y):  # l_xor for logical xor
        if x == 1 and y == 1 or x == 0 and y == 0:
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

class StochasticNumberGenerator:    # in probability y_i
    def __init__(self, tau):  # tau is the limit for iterations
        self.__tau = tau

    # (probability).as_integer_ratio()
    # from fractions import Fraction
    # Fraction(probability)

    # to binary: bin(number)

    # random numbers l_n:  0,1
    # n weight functions
    # w_n-1 = and(not(w_n), l_n-1)

    #





# 2. build queue

# 3. hardcode algorithm
