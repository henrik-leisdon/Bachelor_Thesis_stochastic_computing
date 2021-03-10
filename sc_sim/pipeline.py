import SNG
import PC
import STB
import sc_circuit
import sc_queue


class Pipeline:
    def __init__(self):
        self.sng = SNG.WeightedStochasticNumberGenerator('sng', 0.1)
        self.msc = sc_queue.MscHandler('circuit')
        self.stb = STB.StochToBin('stb')


        # link
        self.stb.msc_link = self.msc
        self.msc.sng_link = self.sng
        self.msc.stb_link = self.stb

    def pipeline(self, input, bitlength):
        # request n bits with STB
        # stb.call(20) 20 bits called

        y_bit = self.stb.request_bits(input, bitlength)
        out = self.stb.x_out




