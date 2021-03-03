# stochastic to binary + parity check
# input n bit bitream
# out 1 bit

def convert_all(prob_y):
    """convert for all 6 evaluated bistreams"""
    x_out = []
    for i in range(0, len(prob_y)):
        x_out.append(convert(prob_y[i]))
    return x_out


def convert(prob_bitstream):
    """convert bitstream to probability and rounds it to 1 or 0"""
    one_counter = 0

    for i in range(0, len(prob_bitstream)):
        if prob_bitstream[i] == 1:
            one_counter += 1

    return round(one_counter / len(prob_bitstream))


def round(probability):
    """round probability to 1, 0 or -1"""
    if probability > 0.75:
        return 1
    elif probability < 0.25:
        return 0
    else:
        return -1


def x_or(a, b):
    if a == 0 and b == 1 or a == 1 and b == 0:
        return 1
    else:
        return 0


def main():
    par = parity_check([1, 0, 0, 1, 1, 0])
    print(par)


if __name__ == '__main__':
    main()
