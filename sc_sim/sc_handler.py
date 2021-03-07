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
        self.msc.generate()
        self.y_in = None
        self.y_out = [[], [], [], [], [], []]
        self.y_stb = [[], [], [], [], [], []]
        self.ctr = 0

    def pipeline(self, input):
        self.y_in = self.sng.generate_stochastic_bitstream(input)

        print(self.y_in)

        y_sc = [self.y_in[0].pop(0), self.y_in[1].pop(0), self.y_in[2].pop(0), self.y_in[3].pop(0), self.y_in[4].pop(0),
                self.y_in[5].pop(0)]
        y_out = self.msc.run_circuit(y_sc)
        self.y_out[0].append(y_out[0])
        self.y_out[1].append(y_out[1])
        self.y_out[2].append(y_out[2])
        self.y_out[3].append(y_out[3])
        self.y_out[4].append(y_out[4])
        self.y_out[5].append(y_out[5])
        print(y_out)
        print(self.y_out)
        self.ctr += 1
        if self.ctr < 10:
            self.pipeline(input)


def main():
    p = Pipeline()
    p.pipeline([1, 0, 0, 1, 1, 1])


if __name__ == '__main__':
    main()
