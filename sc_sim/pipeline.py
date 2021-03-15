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
        # request n bits with STB
        # stb.call(20) 20 bits called
        self.data.x_in = input
        self.data.bitlength = bitlength
        self.data.tau = tau
        self.data = self.stb.request_bits(self.data)
        self.output.extend(self.data.y_out)
        # print(self.pc.parity_check(self.data.x_out))

        while tau < 5 and self.pc.parity_check(self.data.x_out) == False:
            self.data.tau += 1
            print('y in while: ' + str(self.data.y_out))
            self.data = self.stb.request_bits(self.data)
            self.output.extend(self.data.y_out)
            tau += 1

        self.stb.convert(self.output)
        print(' ')
        print(self.output)
        print(self.stb.x_out)


def main():
    p = Pipeline()
    p.pipeline([1, 0, 0, 1, 1, 1], 10, 0)


if __name__ == '__main__':
    main()
