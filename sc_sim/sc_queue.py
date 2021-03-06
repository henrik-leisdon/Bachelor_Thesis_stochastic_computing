class Connection:
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
    def __init__(self, name):
        self.name = name


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
    def __init__(self, name):
        Gate.__init__(self, name)
        self.in_1 = Connection('in')
        self.value = None

    def is_evaluatable(self):
        return True

    def evaluate(self):
        pass

    def update(self):
        pass


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
        print('xor evaluate ' + str(self.in_1.value))
        if self.in_1.value == 1 and self.in_2.value == 0 or self.in_1.value == 0 and self.in_2.value == 1:
            self.value = 1
        else:
            self.value = 0


class AND(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')

    def is_evaluatable(self):
        if self.in_1.value is None or self.in_2.value is None:
            return False
        else:
            return True

    def evaluate(self):
        if self.in_1.value == 0 or self.in_2.value == 0:
            self.value = 0
        elif self.in_1.value == 1 and self.in_2.value == 1:
            self.value = 1
        else:
            self.value = 0


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
        if self.in_1.value == 1 and self.in_2.value == 1:
            self.value = 1
        elif self.in_1.value == 0 and self.in_2.value == 0:
            self.value = 0
        else:
            self.value = self.in_3.value


class Circuit(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.gate_list = []
        self.y_0 = Input('y_0')
        self.y_1 = Input('y_1')
        self.y_2 = Input('y_2')
        self.y_3 = Input('y_3')
        self.y_4 = Input('y_4')
        self.y_5 = Input('y_5')

        self.y_0_out = Output('y_0_out')
        self.y_1_out = Output('y_1_out')
        self.y_2_out = Output('y_2_out')
        self.y_3_out = Output('y_3_out')
        self.y_4_out = Output('y_4_out')
        self.y_5_out = Output('y_5_out')

    def generate(self):
        print('circuit initialized')
        # set input

        xor_0 = XOR('XOR_0')
        xor_1 = XOR('XOR_1')
        xor_2 = XOR('XOR_2')

        update_0 = Update('Update_0')
        update_1 = Update('Update_1')
        update_2 = Update('Update_2')

        self.y_0.connect([xor_1.in_1, xor_2.in_1, update_0.in_3, self.y_4_out])
        self.y_1.connect([update_2.in_2, self.y_5_out,update_1.in_3])
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

    def run_circuit(self, input):
        print('run circuit')
        self.y_0.value = input[0]
        self.y_1.value = input[1]
        self.y_2.value = input[2]
        self.y_3.value = input[3]
        self.y_4.value = input[4]
        self.y_5.value = input[5]

        while self.gate_list:
            gate = self.gate_list.pop(0)
            if gate.is_evaluatable:
                print('in evaluatable')
                gate.evaluate()
                print(gate.name + ' evaluated: ' + str(gate.value))
                gate.update()
            else:
                self.gate_list.append(gate)

        print('end')
        y_out = []
        y_out.extend([self.y_0_out.value, self.y_1_out.value, self.y_2_out.value, self.y_3_out.value,
                      self.y_4_out.value, self.y_5_out.value])
        return y_out


def main():
    c = Circuit('c')
    c.generate()
    y = c.run_circuit([1, 0, 0, 1, 1, 1])
    print(y)


if __name__ == '__main__':
    main()
