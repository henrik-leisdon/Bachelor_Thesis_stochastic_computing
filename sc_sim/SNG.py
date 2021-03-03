from fractions import Fraction
from decimal import Decimal
import random

# in: set of n bits
# out set of n bitstreams


def bit_not(a):
    if a == 1:
        return 0
    else:
        return 1


def weight_gen(random_list):
    """weight generator for weighted SNG
    @:param random_list: list of random bits
    @:return: weights for random list"""
    w_0 = random_list[0]
    w_1 = bit_not(random_list[0]) and random_list[1]
    w_2 = bit_not(random_list[0]) and bit_not(random_list[1]) and random_list[2]
    w_3 = bit_not(random_list[0]) and bit_not(random_list[1]) and bit_not(random_list[2]) and random_list[3]
    return [w_0, w_1, w_2, w_3]


class StochasticNumberGenerator:
    """simulates a stochastic number generator using a comperator
    @:param name: name of the generator
    @:param p_e: probability of the channel/probability for stochastic number
    @:param stream_length:  length of the bitstream
    @:param input: recieved input"""
    def __init__(self, name, p_e, stream_length, input):
        self.name = name
        self.p_e = p_e
        self.stream_length = stream_length
        self.input = input

    def generate_stochastic_number(self, input_bit):
        """generates (pseudo) stochastic bitstream
        @:param input_bit: bit to generate a bitstream for
        @:return: stochastic bistream for input bit"""
        bitstream = []
        probability = input_bit * (1 - self.p_e) + self.p_e * (1 - input_bit)
        frac = Fraction(Decimal(probability))
        for i in range(0, self.stream_length):
            r = random.randint(0, frac.denominator)
            if r < frac.numerator:
                bitstream.append(1)
            else:
                bitstream.append(0)
        return bitstream

    def generate_stochastic_bitstream(self):
        """generate for every input bit a stochastic bitstream
        @:return: list of stochastic bitstreams"""
        stoch_num_list = []
        for i in range(0, 6):
            b = self.generate_stochastic_number(self.input[i])
            stoch_num_list.append(b)
        return stoch_num_list


class WeightedStochasticNumberGenerator:  # in probability y_i
    """generates a stochastic number with weighting the bits of the binary number"""
    def __init__(self, name, p_e):
        self.name = name
        self.p_e = p_e

    @staticmethod
    def init_sn():
        stochastic_number = []
        for i in range(0, 4):
            r = random.randrange(0, 2)
            stochastic_number.append(r)
        return stochastic_number

    def generate(self, input_x):
        """generates (pseudo) stochastic bitstream with weights
        @:param input_bit: bit to generate a bitstream for
        @:return: stochastic bistream for input bit"""
        probability = input_x * (1 - self.p_e) + self.p_e * (1 - input_x)

        frac = Fraction(Decimal(str(probability)))
        print(frac)
        binary_list = list(bin(frac.numerator)[2:].zfill(4))
        print(binary_list)

        random_list = WeightedStochasticNumberGenerator.init_sn()
        stochastic_number = []

        for i in range(0, frac.denominator):

            weight = weight_gen(random_list)
            print('r: ' + str(random_list))
            print('w: ' + str(weight))
            n = weight[0] and binary_list[0] or weight[1] and binary_list[1] or \
                weight[2] and binary_list[2] or weight[3] and binary_list[3]
            stochastic_number.append(n)

            random_list.pop(0)
            random_list.append(random.randrange(0, 2))

        print(stochastic_number)


def main():
    #sng = StochasticNumberGenerator('sng', 0.1, 10)
    # stoch_num_list = []
    # input = [1, 0, 0, 1, 1, 1]
    # for i in range(0, 6):
    #     stoch_num_list.append(sng.generate_stochastic_number(input[i]))
    # print(stoch_num_list)

    wsng = WeightedStochasticNumberGenerator('wsng', 0.1)
    wsng.generate(1)


if __name__ == '__main__':
    main()
