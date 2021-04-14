import SNG
import PC
import STB
import sc_circuit
import sc_queue


def main():
    input = [1, 0, 0, 1, 1, 1]

    # sng = SNG.StochasticNumberGenerator('sng', 0.1, 10)
    # y_in = sng.generate_stochastic_bitstream(input)

    wsng = SNG.WeightedStochasticNumberGenerator('sng', 0.1)
    y_in = wsng.generate_stochastic_bitstream(input)
    circuit = sc_queue.Circuit('queue_circuit')
    circuit.generate()

    parity = False
    i = 0

    threshold = 10
    while parity == False and i < threshold:
        print('yin = ' + str(y_in))
        y_out = circuit.run_circuit(y_in)
        x_out = STB.convert_all(y_out)
        parity = PC.parity_check(x_out)
        print(parity)
        y_in = y_out
        i += 1


if __name__ == '__main__':
    main()
