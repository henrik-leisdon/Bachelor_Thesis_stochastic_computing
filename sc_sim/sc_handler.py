import SNG
import PC
import STB
import sc_circuit
import sc_queue


class Pipeline:
    def __init__(self):
        self.sng = SNG.WeightedStochasticNumberGenerator('sng', 0.1)
        self.stb = None  # stb needs to be a class
        self.msc = sc_queue.Circuit('circuit')

    def pipeline(self, input, precision):
        y_in = self.sng.generate_weighted_number(input)
        self.msc.generate()