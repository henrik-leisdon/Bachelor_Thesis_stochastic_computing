class Connection:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.connection = []

    def set_value(self, value):
        self.value = value

    def connect(self, connections):
        if not isinstance(connections, list):
            connections = [connections]
        for connection in connections:
            self.connections.append(connection)

class Gate:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.connections = []

    def connect(self, connections):
        if not isinstance(connections, list):
            connections = [connections]
        for connection in connections:
            self.connections.append(connection)

    def update(self):
        if self.value is not None:
            for connection in self.connections:
                connection.set_input(self.value)

class Gate2(Gate):
    def __init__(self,name):
        Gate.__init__(self,name)


class Input(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)

    def set_input(self, input):
        self.value = input

    def evaluate(self):
            pass


class Output(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)

    def set_output(self, input):
        self.value = input


class XOR(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.in_1 = Connection('in_1')
        self.in_2 = Connection('in_2')
        self.out = Connection('out')

    def is_evaluatable(self):
        if self.input_1 is None or self.input_2 is None:
            return False
        else:
            return True

    def evaluate(self):
        if self.in_1.value == 1 and self.in_2.value == 0 or self.in_1.value == 0 and self.in_2.value == 1:
            self.value = 1
        else:
            self.value = 0

    def set_input(self, value):
        if self.input_1 is None:
            self.input_1 = value
        elif self.input_2 is None:
            self.input_2 = value
        else:
            print('Error in Gate' + self.name + ', too many inputs assigned')

class AND(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.input_1 = None
        self.input_2 = None

    def is_evaluatable(self):
        if self.input_1 is None or self.input_2 is None:
            return False
        else:
            return True

    def evaluate(self):
        if self.input_1 == 0 or self.input_2 == 0:
            self.value = 0
        elif self.input_1 == 1 and self.input_2 == 1:
            self.value = 1
        else:
            self.value = 0

    def set_input(self, value):
        if self.input_1 is None:
            self.input_1 = value
        elif self.input_2 is None:
            self.input_2 = value
        else:
            print('Error in Gate' + Gate.__name__ + ', too many inputs assigned')


class Update(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
        self.value = None
        self.input_1 = None
        self.input_2 = None
        self.input_3 = None

    def is_evaluatable(self):
        if self.input_1 is None or self.input_2 is None or self.input_3 is None:
            return False
        else:
            return True

    def evaluate(self):
        if self.input_1 == 1 and self.input_2 == 1:
            self.value = 1
        elif self.input_1 == 0 and self.input_2 == 0:
            self.value = 0
        else:
            self.value = self.input_3

    def set_input(self, value):
        if self.input_1 is None:
            self.input_1 = value
        elif self.input_2 is None:
            self.input_2 = value
        elif self.input_3 is None:
            self.input_3 = value
        else:
            print('Error in Gate' + Gate.__name__ + ', too many inputs assigned')

class Circuit(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)


    def generate(self):
        # set input
        y_0 = Input('y_0')
        y_1 = Input('y_1')
        y_2 = Input('y_2')
        y_3 = Input('y_3')
        y_4 = Input('y_4')
        y_5 = Input('y_5')

        y_0_out = Output('y_0_out')
        y_1_out = Output('y_1_out')
        y_2_out = Output('y_2_out')
        y_3_out = Output('y_3_out')
        y_4_out = Output('y_4_out')
        y_5_out = Output('y_5_out')

        xor_0 = XOR('XOR_0')
        xor_1 = XOR('XOR_1')
        xor_2 = XOR('XOR_2')

        update_0 = Update('Update_0')
        update_1 = Update('Update_1')
        update_2 = Update('Update_2')

        y_0.connect([xor_1, xor_2, update_0, y_4_out])
        y_1.connect([update_2, y_5_out,update_1])
        y_2.connect([xor_0, update_1, xor_2, update_2])



        self.gate_list.append()

    def run_circuit(self, input):

