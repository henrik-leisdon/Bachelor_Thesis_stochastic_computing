from LDPC_sim import SNG
from LDPC_sim import PC
from LDPC_sim import STB
from LDPC_sim import sc_queue
from LDPC_sim import Data

import math
import time


def test_compare(probability, bit_length, test_size, tolerance):
    """generate 10/100/1000 n bit strings and test if the result is in the error tolerance"""
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
        equal = math.isclose(1 - probability, pr, rel_tol=tolerance)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))

    """---------------- ZEROS------------------------- """
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
        equal = math.isclose(probability, pr, rel_tol=tolerance+0.1)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))


# sng scale

def test_scale(probability, bit_length, test_size, tolerance):
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
        equal = math.isclose(1 - probability, pr, rel_tol=tolerance)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))

    """---------------- ZEROS------------------------- """
    print('\n0s:')
    error_number = 0
    for i in range(0, test_size):
        sn = sng_c.gen_bit(0, bit_length)

        bit_count = 0
        for bit in sn:
            if bit == 1:
                bit_count += 1
        pr = bit_count / bit_length
        print(str(sn) + ' ' + str(pr))
        equal = pr < 0.1  #math.isclose(probability, pr, rel_tol=tolerance+0.2)
        if not equal:
            error_number += 1

    print('number of errors:' + str(error_number))
    print('error frequency: ' + str(error_number / test_size))


def test_correlation():
    pass


class TestPipeline:
    def __init__(self):
        self.sng = SNG.SngHandler('sng', 0.1)
        self.msc = sc_queue.MscHandler('circuit')
        self.stb = STB.StochToBin('stb')
        self.pc = PC.ParityCheck('pc')
        self.data = Data.Data('data')
        self.output = []

        # link
        self.stb.msc_link = self.msc
        self.msc.sng_link = self.sng
        self.msc.stb_link = self.stb

    def pipeline(self, input, bitlength, tau):

        self.data.generation_method = 0
        self.data.x_in = input
        self.data.bitlength = bitlength
        self.data.tau = tau
        self.data = self.stb.request_bits(self.data)
        self.output.extend(self.data.y_out)
        # print(self.data.x_out)
        # print(self.pc.parity_check(self.data.x_out))
        # return self.pc.parity_check(self.data.x_out)

    def run(self, input, bitlength, probability):
        fail_count = 0
        error_rate = 0
        for i in range(0, 100):
            time.sleep(0.01)
            self.pipeline(input, bitlength, 0)
            time.sleep(0.1)
            print(self.data.y_in)
            print(self.data.y_out)
            print(self.data.x_out)
            parity = self.pc.parity_check(self.data.x_out)
            print(parity)
            y_in = self.data.y_in

            if parity == False:
                fail_count += 1
                it = 0

                for inputs in y_in:

                    rate = 0

                    for bits in inputs:
                        if bits == 1:
                            rate += 1

                    pr = rate/len(inputs)

                    prob = self.data.x_in[it] * (1 - probability) + probability * (1 - self.data.x_in[it])
                    # print(prob)
                    if pr != prob:
                        error_rate += 1
                    it += 1

        print('fail count:' + str(fail_count))
        print('error rate in fails:' + str(error_rate))

            # count bits, get probability
            # if pr = x_in * (1 - self.p_e) + self.p_e * (1 - input_x)


def test1():
    print('compare')
    test_compare(0.1, 10, 1000, 0.1)
    print('-----------------------------------------------')
    test_compare(0.1, 100, 1000, 0.1)
    print('-----------------------------------------------')
    test_compare(0.1, 1000, 1000, 0.1)
    print('-----------------------------------------------')
    print('-----------------------------------------------')
    print('scale')
    test_scale(0.1, 10, 1000, 0.1)
    print('-----------------------------------------------')
    test_scale(0.1, 100, 1000, 0.1)
    print('-----------------------------------------------')
    test_scale(0.1, 1000, 1000, 0.1)
    print('-----------------------------------------------')


def test2():
    p = TestPipeline()
    p.run([1, 0, 0, 1, 1, 1], 10, 0.1)


if __name__ == '__main__':
    # test1()
    test1()

