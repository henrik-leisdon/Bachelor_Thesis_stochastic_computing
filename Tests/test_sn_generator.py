import math

from sc_sim import SNG


def test_compare(probability, bit_length, test_size):
    # sng_compare
    print('1s:')

    sng_c = SNG.SngCompare('sng_c', probability)
    error_number = 0
    for i in range(0, test_size):
        sn = sng_c.gen_bit(1, bit_length)
        bit_count = 0
        for bit in sn:
            if bit == 1:
                bit_count += 1
        pr = bit_count / bit_length
        equal = math.isclose(1 - probability, pr, rel_tol=0.15)
        if not equal:
            error_number+=1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number/test_size))

    print('\n0s:')
    # sng_c = SNG.SngScale('sng_c', probability)
    error_number = 0
    for i in range(0, test_size):
        sn = sng_c.gen_bit(0, bit_length)
        bit_count = 0
        for bit in sn:
            if bit == 1:
                bit_count += 1
        pr = bit_count / bit_length
        equal = math.isclose(probability, pr, rel_tol=0.15)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))


# sng scale

def test_scale(probability, bit_length, test_size):
    # sng_compare
    print('1s:')

    sng_c = SNG.SngScale('sng_s', probability)
    error_number = 0
    for i in range(0, test_size):
        sn = sng_c.gen_bit(1, bit_length)
        bit_count = 0
        for bit in sn:
            if bit == 1:
                bit_count += 1
        pr = bit_count / bit_length
        equal = math.isclose(1 - probability, pr, rel_tol=0.15)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))

    print('\n0s:')
    error_number = 0
    for i in range(0, test_size):
        sn = sng_c.gen_bit(0, bit_length)
        bit_count = 0
        for bit in sn:
            if bit == 1:
                bit_count += 1
        pr = bit_count / bit_length
        equal = math.isclose(probability, pr, rel_tol=0.15)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))

    # sng scale

def test_correlation():
    pass


def main():
    print('compare')
    test_compare(0.1, 10, 100)
    test_compare(0.1, 100, 100)
    test_compare(0.1, 1000, 100)
    print('scale')
    test_scale(0.1, 10, 100)
    test_scale(0.1, 100, 100)
    test_scale(0.1, 1000, 100)


if __name__ == '__main__':
    main()
