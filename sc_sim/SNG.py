from fractions import Fraction
from decimal import Decimal
import random


def bit_not(a):
    if a == 1:
        return 0
    else:
        return 1


def weight_gen(random_list):
    w_0 = random_list[0]
    w_1 = bit_not(random_list[0]) and random_list[1]
    w_2 = bit_not(random_list[0]) and bit_not(random_list[1]) and random_list[2]
    w_3 = bit_not(random_list[0]) and bit_not(random_list[1]) and bit_not(random_list[2]) and random_list[3]
    return [w_0, w_1, w_2, w_3]


class StochasticNumberGenerator:
    def __init__(self, name, p_e, stream_length, input):
        self.name = name
        self.p_e = p_e
        self.stream_length = stream_length
        self.input = input

    def generate_stochastic_number(self, input_bit):
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
        stoch_num_list = []
        for i in range(0, 6):
            b = self.generate_stochastic_number(self.input[i])
            stoch_num_list.append(b)
        return stoch_num_list


class WeightedStochasticNumberGenerator:  # in probability y_i
    def __init__(self, name, p_e):
        self.name = name
        self.p_e = p_e

    def generate(self, input_x):
        probability = input_x * (1 - self.p_e) + self.p_e * (1 - input_x)

        frac = Fraction(Decimal(str(probability)))
        binary_list = list(bin(frac.numerator)[2:].zfill(4))
        print(binary_list)
        stochastic_number = []

        for i in range(0, frac.denominator):
            random_list = []
            for j in binary_list:
                r = random.randrange(0, 2)
                random_list.append(r)
            weight = weight_gen(random_list)
            print(random_list)
            print('weight: ' + str(weight))
            n = weight[0] and binary_list[0] or weight[1] and binary_list[1] or \
                weight[2] and binary_list[2] or weight[3] and binary_list[3]
            stochastic_number.append(n)

        print(stochastic_number)


def main():
    sng = StochasticNumberGenerator('sng', 0.1, 10)
    stoch_num_list = []
    input = [1, 0, 0, 1, 1, 1]
    for i in range(0, 6):
        stoch_num_list.append(sng.generate_stochastic_number(input[i]))
    print(stoch_num_list)

    # wsng = WeightedStochasticNumberGenerator('wsng', 0.1)
    # wsng.generate(0)


if __name__ == '__main__':
    main()
