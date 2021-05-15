import copy
import random


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

    def reset(self):
        # self.value = None
        pass


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

    def reset(self):
        self.value = None


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

    def reset(self):
        self.value = None


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

    def reset(self):
        self.in_1.value = None
        self.in_2.value = None
        self.value = None


class Multiplexer2(Gate2):
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
        r_bit = random.uniform(0, 1)
        self.in_3.value = r_bit
        if self.in_3 == 0:
            self.value = self.in_1.value
        else:
            self.value = self.in_2.value

        if self.monitor == 1 and tmp_val != self.value:
            print(str(self.name) + ' ' + str(self.value))

    def reset(self):
        self.in_1.value = None
        self.in_2.value = None
        self.in_3.value = None
        self.value = None


class Multiplexer4(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        # input
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')
        self.in_3 = Connection('in_3')
        self.in_4 = Connection('in_4')
        # control bits
        self.in_5 = Connection('in_5')
        self.in_6 = Connection('in_6')

    def is_evaluatable(self):
        if self.in_1.value is None or self.in_2.value is None or self.in_3.value is None or self.in_4.value is None:
            return False
        else:
            return True

    def evaluate(self):
        tmp_val = self.value
        r_bit1 = random.uniform(0, 1)
        r_bit2 = random.uniform(0, 1)
        self.in_5.value = r_bit1
        self.in_6.value = r_bit2
        if self.in_5 == 0 and self.in_6 == 0:
            self.value = self.in_1.value
        elif self.in_5 == 0 and self.in_6 == 1:
            self.value = self.in_2.value
        elif self.in_5 == 1 and self.in_6 == 0:
            self.value = self.in_3.value
        else:
            self.value = self.in_4.value

        if self.monitor == 1 and tmp_val != self.value:
            print(str(self.name) + ' ' + str(self.value))

    def reset(self):
        self.in_1.value = None
        self.in_2.value = None
        self.in_3.value = None
        self.in_4.value = None
        self.in_5.value = None
        self.in_6.value = None
        self.value = None

        # tag with evaluated or not


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

        self.y_0_out = Output('y_0_out', monitor=0)

    def gen_rc(self):
        # print('circuit initialized')
        # set input

        self.xor_0 = XOR('XOR_0')
        self.xor_1 = XOR('XOR_1')

        self.mult = Multiplexer2('M_1')

        self.y_0.connect([self.xor_0.in_1])
        self.y_1.connect([self.xor_0.in_2])
        self.y_2.connect([self.xor_1.in_1])
        self.y_3.connect([self.xor_1.in_2])

        self.xor_0.connect([self.mult.in_1])
        self.xor_1.connect([self.mult.in_2])

        self.mult.connect([self.y_0_out])

        self.gate_list.append(self.y_0)
        self.gate_list.extend([self.y_1, self.y_2, self.y_3, self.xor_0, self.xor_1, self.mult, self.y_0_out])
        self.full_list = copy.deepcopy(self.gate_list)

    def gen_adaptive_rc(self):
        self.xor_0 = XOR('XOR_0')
        self.xor_1 = XOR('XOR_1')
        self.xor_2 = XOR('XOR_2')
        self.xor_3 = XOR('XOR_3')

        self.mult = Multiplexer4('M_1')

        self.y_0.connect([self.xor_0.in_1, self.xor_2.in_1, self.xor_3.in_1])
        self.y_1.connect([self.xor_0.in_2, self.xor_2.in_2])
        self.y_2.connect([self.xor_1.in_1, self.xor_3.in_2])
        self.y_3.connect([self.xor_1.in_2])

        self.xor_0.connect([self.mult.in_1])
        self.xor_1.connect([self.mult.in_2])
        self.xor_2.connect([self.mult.in_3])
        self.xor_3.connect([self.mult.in_4])

        self.mult.connect([self.y_0_out])

        self.gate_list.append(self.y_0)
        self.gate_list.extend([self.y_1, self.y_2, self.y_3, self.xor_0, self.xor_1, self.xor_2, self.xor_3, self.mult,
                               self.y_0_out])

    def run_rc(self, input, gen_method):
        num_op = 0
        """run circuit
        @:param input: 1 input bit from every stocastic bitstream"""

        self.y_0.value = int(input[0])
        self.y_1.value = int(input[1])
        self.y_2.value = int(input[2])
        self.y_3.value = int(input[3])

        while self.gate_list:
            gate = self.gate_list.pop(0)

            if gate.is_evaluatable:
                gate.evaluate()
                gate.update()
                # print('{}: {}'.format(gate.name, gate.value))  # LEAVE FOR DEBUGGING!!

            else:
                gate.tau += 1
                if gate.tau < 5:
                    self.gate_list.append(gate)
            num_op += 1

        output = self.y_0_out.value

        # clean up

        if gen_method == 1:
            self.gate_list.append(self.y_0)
            self.gate_list.extend(
                [self.y_1, self.y_2, self.y_3, self.xor_0, self.xor_1, self.xor_2, self.xor_3, self.mult,
                 self.y_0_out])
        else:   # gen method == 0
            self.gate_list.append(self.y_0)
            self.gate_list.extend([self.y_1, self.y_2, self.y_3, self.xor_0, self.xor_1, self.mult, self.y_0_out])

        for gate in self.gate_list:
            gate.reset()
            num_op += 1

        # print(num_comp)
        return output
