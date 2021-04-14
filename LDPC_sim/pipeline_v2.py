import copy

import SNG
import PC
import STB
import MSC
import Data


class PipelineV2:
    def __init__(self):
        self.sng = SNG.SngHandler('sng', 0.1)
        self.msc = MSC.MscHandler('circuit')
        self.stb = STB.StochToBin('stb')
        self.pc = PC.ParityCheck('pc')
        self.data = Data.Data('data')
        self.sc = MSC.Circuit('sub_circuit_1')

        # link
        self.stb.msc_link = self.msc
        self.msc.sng_link = self.sng
        self.msc.stb_link = self.stb

    def pipeline(self, input, bitlength, tau):
        """
        sng = new bits
        msc = main core
        stb = back to binary
        pc = parity check
        if parity check = wrong
            request new bits
        """

        self.data.generation_method = 0
        self.data.x_in = input
        self.data.bitlength = bitlength
        self.data.tau = tau
        data = self.pipe(self.data)
        stop = 0

        if self.pc.parity_check(data.x_out) == False and stop < 10:
            print(self.pc.parity_check(data.x_out))

            data_new = Data.Data('data_pc')
            data_new.x_in = input
            data_new.bitlength = 4
            data_new.tau = tau
            data_new = self.pipe(data_new)
            data.append_y_out(data_new.y_out)
            data.x_out = self.stb.convert(data.y_out)
            print(data.x_out)
            stop += 1

        data.to_String()
        return data

    def pipe(self, data):
        tmp_data = self.sng.generate(copy.deepcopy(data))
        y_out = [[], [], [], [], [], []]
        for i in range(0, tmp_data.bitlength):
            y = self.parse(tmp_data.y_in)
            self.sc.generate()
            y_out_bit = self.sc.run_circuit(y)
            y_out = self.append_y_out(y_out_bit, y_out)

        tmp_data.y_out = y_out

        x_out = self.stb.convert(y_out)
        tmp_data.x_out = x_out

        # print(tmp_data)
        return tmp_data

    def parse(self, y_in):
        y_out = [y_in[0].pop(0), y_in[1].pop(0), y_in[2].pop(0), y_in[3].pop(0),
                 y_in[4].pop(0), y_in[5].pop(0)]

        return y_out

    def append_y_out(self, y, y_out):
        y_out[0].append(y[0])
        y_out[1].append(y[1])
        y_out[2].append(y[2])
        y_out[3].append(y[3])
        y_out[4].append(y[4])
        y_out[5].append(y[5])

        return y_out


def main():
    p = PipelineV2()
    p.pipeline([1, 0, 0, 1, 1, 1], 10, 0)


if __name__ == '__main__':
    main()
