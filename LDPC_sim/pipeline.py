import copy

import SNG
import PC
import STB
import sc_circuit
import sc_queue
import Data


class Pipeline:
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

        self.data.generation_method = 1
        self.data.x_in = input
        self.data.bitlength = bitlength
        self.data.tau = tau
        self.data = self.stb.request_bits(self.data)
        self.output.extend(self.data.y_out)

        # print(self.pc.parity_check(self.data.x_out))

        while tau < 5 and self.pc.parity_check(self.data.x_out) == False:
            self.data.tau += 0
            prev_data = self.data

            # print('y in while: ' + str(self.data.y_out))
            self.data = self.stb.request_bits(self.data)

            self.append_y_out(copy.deepcopy(self.data.y_out))

            if self.data.y_out == prev_data.y_out:
                print('in if')

                data = self.sng.generate(self.data)
                self.data.y_in = data.y_in
            print('x_out {}'.format(self.data.x_out))
            tau += 1

        output = self.stb.convert(self.output)
        print(output)
        print(' ')
        print('{}, {}'.format(len(self.output[0]), self.output))
        print(self.stb.x_out)
        print('---------------------------------------------------')

    def append_y_out(self, y_out):
        while len(y_out[0]) > 0:
            self.output[0].append(y_out[0].pop(0))
            self.output[1].append(y_out[1].pop(0))
            self.output[2].append(y_out[2].pop(0))
            self.output[3].append(y_out[3].pop(0))
            self.output[4].append(y_out[4].pop(0))
            self.output[5].append(y_out[5].pop(0))


def main():
    p = Pipeline()
    p.pipeline([1, 0, 0, 1, 1, 1], 10, 0)


if __name__ == '__main__':
    main()
