import SNG


# https://www.collindelker.com/2014/08/29/electrical-schematic-drawing-python.html for drawing circuits


class Connector:
    """Connector connects inputs with gates, gates with gates and gates with output
        sets values and monitors connection"""

    def __init__(self, referred_gate, name, activates=0, monitor=0):

        self.value = None
        self.referred_gate = referred_gate
        self.name = name
        self.monitor = monitor
        self.connects = []
        self.activates = activates

    def connect(self, inputs):
        if not isinstance(inputs, list):
            inputs = [inputs]
        for input in inputs:
            self.connects.append(input)

    def set(self, value):
        if self.value == value:
            return
        self.value = value
        if self.activates:
            self.referred_gate.evaluate()
        if self.monitor:
            print(str(self.referred_gate.name) + ' ' + str(self.name) + ', value = ' + str(value))

        for connection in self.connects:
            connection.set(value)


# --------------- Gates ---------------------------------------------

class Gate:
    def __init__(self, name, tau):
        self.name = name
        self.tau = tau

    def evaluate(self):
        return


class Gate2(Gate):
    def __init__(self, name, tau):
        Gate.__init__(self, name, tau)
        self.in1 = Connector(self, 'in_1', activates=1)
        self.in2 = Connector(self, 'in_2', activates=1)
        self.out = Connector(self, 'out')


class Gate3(Gate):
    def __init__(self, name, tau):
        Gate.__init__(self, name, tau)
        self.in1 = Connector(self, 'in_1', activates=1)
        self.in2 = Connector(self, 'in_2', activates=1)
        self.in3 = Connector(self, 'in_3', activates=1)
        self.out = Connector(self, 'out')


class AND(Gate2):
    def __init__(self, name, tau):
        Gate2.__init__(self, name, tau)

    def evaluate(self):
        self.out.set(self.in1.value and self.in2.value)


class OR(Gate2):
    def __init__(self, name, tau):
        Gate2.__init__(self, name, tau)

    def evaluate(self):
        self.out.set(self.in1.value or self.in2.value)


class NOR(Gate2):
    def __init__(self, name, tau):
        Gate2.__init__(self, name, tau)

    def evaluate(self):
        if self.in1.value == 0 and self.in2.value == 0:
            self.out.set(1)
        else:
            self.out.set(0)


class XOR(Gate2):
    def __init__(self, name, tau):
        Gate2.__init__(self, name, tau)

    def evaluate(self):
        if self.in1.value == 1 and self.in2.value == 0 or self.in1.value == 0 and self.in2.value == 1:
            self.out.set(1)
        else:
            self.out.set(0)


class Update(Gate3):
    def __init__(self, name, tau):
        Gate3.__init__(self, name, tau)  # input for unsure 01/10

    def evaluate(self):
        if self.in1.value == 1 and self.in2.value == 1:
            self.out.set(1)
        elif self.in1.value == 0 and self.in2.value == 0:
            self.out.set(0)
        else:
            self.out.set(self.in3.value)
            print('in update ' + str(self.in3.value))


# --------------- Circuit components ---------------------------------------------


class MainStochasticCore(Gate):
    def __init__(self, name, tau):
        Gate.__init__(self, name, tau)

        # set input
        self.y_0 = Connector(self, 'y_0', 1, monitor=1)
        self.y_1 = Connector(self, 'y_1', 1, monitor=1)
        self.y_2 = Connector(self, 'y_2', 1, monitor=1)
        self.y_3 = Connector(self, 'y_3', 1, monitor=1)
        self.y_4 = Connector(self, 'y_4', 1, monitor=1)
        self.y_5 = Connector(self, 'y_5', 1, monitor=1)

        # set output

        self.y_0_out = Connector(self, 'y_0_out', monitor=1)
        self.y_1_out = Connector(self, 'y_1_out', monitor=1)
        self.y_2_out = Connector(self, 'y_2_out', monitor=1)
        self.y_3_out = Connector(self, 'y_3_out', monitor=1)
        self.y_4_out = Connector(self, 'y_4_out', monitor=1)
        self.y_5_out = Connector(self, 'y_5_out', monitor=1)

        # gates
        self.XOR_0 = XOR('XOR_0', tau)
        self.XOR_1 = XOR('XOR_1', tau)
        self.XOR_2 = XOR('XOR_2', tau)

        self.Update_0 = Update('Update_0', tau)
        self.Update_1 = Update('Update_1', tau)
        self.Update_2 = Update('Update_2', tau)

        self.y_0.connect([self.XOR_1.in1, self.XOR_2.in1, self.y_4_out, self.Update_0.in3])
        self.y_1.connect([self.Update_2.in2, self.y_5_out, self.Update_1.in3])
        self.y_2.connect([self.XOR_0.in1, self.Update_1.in1, self.XOR_2.in2, self.Update_2.in3])
        self.y_3.connect([self.XOR_0.in2, self.XOR_1.in2])
        self.y_4.connect([self.Update_0.in2])
        self.y_5.connect([self.Update_1.in2])

        self.XOR_0.out.connect([self.Update_0.in1])
        self.XOR_1.out.connect([self.Update_2.in1])

        self.Update_0.out.connect([self.y_0_out])
        self.Update_1.out.connect([self.y_1_out])
        self.Update_2.out.connect([self.y_2_out])
        self.XOR_2.out.connect([self.y_3_out])


def main(tau, y_in):
    y = y_in
    y_out = [[], [], [], [], [], []]
    print('y = ' + str(y))
    MSC = MainStochasticCore('MSC', tau)

    for i in range(0, len(y[0])):
        MSC.y_0.set(y[0][i])
        MSC.y_1.set(y[1][i])
        MSC.y_2.set(y[2][i])
        MSC.y_3.set(y[3][i])
        MSC.y_4.set(y[4][i])
        MSC.y_5.set(y[5][i])

        y_out[0].append(MSC.y_0_out.value)
        y_out[1].append(MSC.y_1_out.value)
        y_out[2].append(MSC.y_2_out.value)
        y_out[3].append(MSC.y_3_out.value)
        y_out[4].append(MSC.y_4_out.value)
        y_out[5].append(MSC.y_5_out.value)

    print('round done ' + str(y_out))


if __name__ == '__main__':
    input = [1, 0, 0, 1, 1, 1]
    sng = SNG.StochasticNumberGenerator('sng', 0.1, 10, input)
    y_in = sng.generate_stochastic_bitstream()
    print('yin = ' + str(y_in))
    y_in2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    main(2, y_in)
