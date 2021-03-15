# stochastic to binary + parity check
# input n bit bitream
# out 1 bit
def x_or(a, b):
    if a == 0 and b == 1 or a == 1 and b == 0:
        return 1
    else:
        return 0


def prob_round(probability):
    """round probability to 1, 0 or -1"""
    if probability > 0.75:
        return 1
    elif probability < 0.25:
        return 0
    else:
        return -1


class StochToBin:
    def __init__(self, name):
        self.name = name
        self.prob_bitstream = [[], [], [], [], [], []]
        self.x_out = []
        self.msc_link = None

    def convert(self, prob_bitstream):
        self.x_out = []
        """convert bitstream to probability and rounds it to 1 or 0"""
        for y in range(0, len(prob_bitstream)):
            one_counter = 0
            stream = prob_bitstream[y]
            for bit in range(0, len(stream)):

                if stream[bit] == 1:
                    one_counter += 1

            self.x_out.append(prob_round(one_counter / len(stream)))

    def request_bits(self, data):
        self.x_out = []
        data = self.msc_link.msc_to_sng(data)
        self.convert(data.y_out)
        print('converted x: ' + str(self.x_out))

        data.x_out = self.x_out

        return data


# call_from_stb(20) bits
# link to main_stochastic_core
#


def main():
    # s = StochToBin('stb')
    # s.prob_bitstream = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #                    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 1]]

    # s.convert()
    # print(s.x_out)
    s = StochToBin('stb')
    s.request_bits([1, 0, 0, 1, 1, 1], 10)
    print(s.x_out)


if __name__ == '__main__':
    main()
