# import SNG
import copy


class Connection:
    """Input/connector for every gate"""

    def __init__(self, name):
        self.name = name
        self.value = None
        self.connection = []

    def connect(self, connections):
        if not isinstance(connections, list):
            connections = [connections]
        for con in connections:
            self.connection.append(con)


class Gate:
    def __init__(self, name, monitor=0):
        self.name = name
        self.tau = 0
        self.monitor = monitor


class Input(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.connection = []

    def set_input(self, input):
        self.value = input

    def is_evaluatable(self):
        return True

    def evaluate(self):
        pass

    def update(self):
        if self.value is not None:
            for con in self.connection:
                con.value = self.value

    def connect(self, connections):
        if not isinstance(connections, list):
            connections = [connections]
        for con in connections:
            self.connection.append(con)


class Output(Gate):
    def __init__(self, name, monitor=0):
        Gate.__init__(self, name)
        self.monitor = monitor
        self.in_1 = Connection('in')
        self.value = None
        self.connection = []

    def is_evaluatable(self):
        return True

    def evaluate(self):
        if self.monitor == 1:
            print(str(self.name) + ' ' + str(self.value))

    def update(self):
        pass

class Gate2(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.connection = []

    def update(self):
        if self.value is not None:
            for con in self.connection:
                con.value = self.value

    def connect(self, connections):
        if not isinstance(connections, list):
            connections = [connections]
        for con in connections:
            self.connection.append(con)





class XOR(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')

    def is_evaluatable(self):
        if self.in_1.value is None or self.in_2.value is None:
            return False
        else:
            return True

    def evaluate(self):
        tmp_val = self.value
        if self.in_1.value == 1 and self.in_2.value == 0 or self.in_1.value == 0 and self.in_2.value == 1:
            self.value = 1
        else:
            self.value = 0
        if self.monitor == 1 and tmp_val != self.value:
            print(str(self.name) + ' ' + str(self.value))


class AND(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        self.value = None
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')

    def is_evaluatable(self):
        if self.in_1.value is None or self.in_2.value is None:
            return False
        else:
            return True

    def evaluate(self):
        tmp_val = self.value
        if self.in_1.value == 0 or self.in_2.value == 0:
            self.value = 0
        elif self.in_1.value == 1 and self.in_2.value == 1:
            self.value = 1
        else:
            self.value = 0
        if self.monitor == 1 and tmp_val != self.value:
            print(str(self.name) + ' ' + str(self.value))


class Update(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')
        self.in_3 = Connection('in_3')

    def is_evaluatable(self):
        if self.in_1.value is None or self.in_2.value is None or self.in_3.value is None:
            return False
        else:
            return True

    def evaluate(self):
        tmp_val = self.value
        if self.in_1.value == 1 and self.in_2.value == 1:
            self.value = 1
        elif self.in_1.value == 0 and self.in_2.value == 0:
            self.value = 0
        else:
            self.value = self.in_3.value

        if self.monitor == 1 and tmp_val != self.value:
            print(str(self.name) + ' ' + str(self.value))


# ---------------------------------------------------------------------------------------------------
class Circuit(Gate):
    """Cirucit class, initilaize the circuit model"""

    def __init__(self, name):
        Gate.__init__(self, name)
        self.gate_list = []
        self.full_list = []
        self.y_0 = Input('y_0')
        self.y_1 = Input('y_1')
        self.y_2 = Input('y_2')
        self.y_3 = Input('y_3')
        self.y_4 = Input('y_4')
        self.y_5 = Input('y_5')

        self.y_0_out = Output('y_0_out', monitor=0)
        self.y_1_out = Output('y_1_out', monitor=0)
        self.y_2_out = Output('y_2_out', monitor=0)
        self.y_3_out = Output('y_3_out', monitor=0)
        self.y_4_out = Output('y_4_out', monitor=0)
        self.y_5_out = Output('y_5_out', monitor=0)

    def generate(self):
        # print('circuit initialized')
        # set input

        xor_0 = XOR('XOR_0')
        xor_1 = XOR('XOR_1')
        xor_2 = XOR('XOR_2')

        update_0 = Update('Update_0')
        update_1 = Update('Update_1')
        update_2 = Update('Update_2')

        self.y_0.connect([xor_1.in_1, xor_2.in_1, update_0.in_3, self.y_4_out])
        self.y_1.connect([update_2.in_2, self.y_5_out, update_1.in_3])
        self.y_2.connect([xor_0.in_1, update_1.in_1, xor_2.in_2, update_2.in_3])
        self.y_3.connect([xor_0.in_2, xor_1.in_2])
        self.y_4.connect([update_0.in_2])
        self.y_5.connect([update_1.in_2])

        xor_0.connect([update_0.in_1])
        xor_1.connect([update_2.in_1])
        xor_2.connect([self.y_3_out])

        update_0.connect([self.y_0_out])
        update_1.connect([self.y_1_out])
        update_2.connect([self.y_2_out])

        self.gate_list.append(self.y_0)
        self.gate_list.extend([self.y_1, self.y_2, self.y_3, self.y_4, self.y_5, xor_0, xor_1, xor_2, update_0,
                               update_1, update_2, self.y_0_out, self.y_1_out, self.y_2_out, self.y_3_out,
                               self.y_4_out, self.y_5_out])
        self.full_list = copy.deepcopy(self.gate_list)

    def run_circuit(self, input):
        """run circuit
        @:param input: 1 input bit from every stocastic bitstream"""
        self.y_0.value = input[0]
        self.y_1.value = input[1]
        self.y_2.value = input[2]
        self.y_3.value = input[3]
        self.y_4.value = input[4]
        self.y_5.value = input[5]

        while self.gate_list:
            gate = self.gate_list.pop(0)
            if gate.is_evaluatable:
                gate.evaluate()
                gate.update()

            else:
                gate.tau += 1
                if gate.tau < 5:
                    self.gate_list.append(gate)

        y_out = []
        y_out.extend([self.y_0_out.value, self.y_1_out.value, self.y_2_out.value, self.y_3_out.value,
                      self.y_4_out.value, self.y_5_out.value])
        # print('cir y_out {}'.format(y_out))
        return y_out


# ---------------------------------------------------------------------------------------------------
class MscHandler:
    def __init__(self, name):
        self.name = name
        self.stb_link = None
        self.sng_link = None
        self.sc = Circuit('sub_circuit_1')
        self.sc.generate()
        self.y_in = []
        self.y_out = [[], [], [], [], [], []]
        self.clock = 0

    def msc_to_sng(self, data):
        """request n bits from the sng to compute and return
            y_in = 6 n bit bitstreams"""
        self.y_out = [[], [], [], [], [], []]

        # always generate a new 10 bit bitstream
        data = self.sng_link.generate(data)
        self.y_in = copy.deepcopy(data.y_in)

        for i in range(0, data.bitlength):
            self.sc.generate()
            bit_y_in = self.parse_y_in(copy.deepcopy(self.y_in))
            y_out = self.sc.run_circuit(bit_y_in)
            self.append_y_out(y_out)

            """if self.clock == 0:
                bit_y_in = self.parse_y_in(self.y_in)
                y_out = self.sc.run_circuit(bit_y_in)
                self.append_y_out(y_out)
                y_out_tmp = y_out.copy()
                self.clock = 1
            else:
                y_out = self.sc.run_circuit(y_out_tmp)
                self.append_y_out(y_out)
                y_out_tmp = y_out.copy
                self.clock = 0"""

        data.y_out = self.y_out.copy()
        # data.to_String()


        return data

    def parse_y_in(self, y_in):
        """parse from the n bit bitstream one bit for each y variable (sc just can handle 1 bit)"""
        sc_bit_list = [y_in[0].pop(0), y_in[1].pop(0), y_in[2].pop(0), y_in[3].pop(0),
                       y_in[4].pop(0), y_in[5].pop(0)]
        return sc_bit_list

    def append_y_out(self, y_out):
        self.y_out[0].append(y_out[0])
        self.y_out[1].append(y_out[1])
        self.y_out[2].append(y_out[2])
        self.y_out[3].append(y_out[3])
        self.y_out[4].append(y_out[4])
        self.y_out[5].append(y_out[5])


# ---------------------------------------------------------------------------------------------------
def parse_y_in(y_in):
    """parse from the n bit bitstream one bit for each y variable (sc just can handle 1 bit)"""
    sc_bit_list = [y_in[0].pop(0), y_in[1].pop(0), y_in[2].pop(0), y_in[3].pop(0),
                   y_in[4].pop(0), y_in[5].pop(0)]
    return sc_bit_list


def main():
    # print(m.msc_to_sng([0, 0, 0, 1, 1, 1], 10))
    sc = Circuit('sub_circuit_1')
    sc.generate()
    sc.run_circuit([1, 0, 0, 1, 1, 1])

    # y_in = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    # while len(y_in[0]) > 0:
    #    y = parse_y_in(y_in)
    #    i = sc.run_circuit(y)
    #    print('{}'.format(i))


if __name__ == '__main__':
    main()
