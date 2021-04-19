from LDPC_sim import MSC
import json

class Parser:
    def __init__(self):
        self.name = 'parser'
        self.gatelist = []

    def parse(self):

        with open("circuit.json", 'r') as json_file:
            y = json.load(json_file)

        # for every gate
        for key, value in y.items():
            print(key, value)

            # in every gate print subvalues/keys
            for subkey, subval in value.items():
                print(subkey, subval)
                if subkey == 'type' and subval == 'input':
                    gate = MSC.Input(str(key))
                    self.gatelist.append(gate)

                if subkey == 'type' and subval == 'xor':
                    gate = MSC.XOR(str(key))
                    self.gatelist.append(gate)

        print(str(self.gatelist))


        """with open('circuit.json', 'r') as circuit:
            matrix = [line.split() for line in circuit]
            # print(matrix)

            for it in range(0, len(matrix)):
                row = matrix[it]
                # print(row)
                if row[0] == 'define':
                    if row[1] == 'input':
                        input = MSC.Input(row[2])
                        self.gatelist.append(input)
                    if row[1] == 'output':
                        output = MSC.Output(row[2])
                        self.gatelist.append(output)
                    if row[1] == 'XOR':
                        xor = MSC.XOR(row[2])
                        self.gatelist.append(xor)
                    if row[1] == 'connect':
                        num_of_connections = len(row) - 3  # define, connect and gate name
                        gate = MSC.Gate
                        for g in self.gatelist:
                            if g.name == row[2]:
                                gate = g
                        for i in range(3, num_of_connections, 2):
                            for gatecon in self.gatelist:
                                if gatecon.name == row[i]:
                                    gate.connect(gatecon)
"""



def main():
    parser = Parser()
    parser.parse()


if __name__ == '__main__':
    main()





