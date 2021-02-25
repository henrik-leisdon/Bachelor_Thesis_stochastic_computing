# test queue algorithm

class Connector:
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
            print(str(self.referred_gate.name)+ ' input ' + str(self.name) + ', value = ' + str(value))

        for connection in self.connects:
            connection.set(value)


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


class Circuit(Gate):
    def __init__(self, name, tau):
        Gate.__init__(self, name, tau)
        # set input + output wire
        self.in_a = Connector(self, 'in_a', 1, monitor=1)
        self.in_b = Connector(self, 'in_b', 1, monitor=1)
        self.in_c = Connector(self, 'in_c', 1, monitor=1)

        self.out = Connector(self, 'out', monitor=1)

        # set gates

        self.A1 = AND('A1', 2)
        self.Or1 = OR('Or1', 2)
        self.A2 = AND('A2', 2)

        # set connections:
        self.in_a.connect([self.A1.in1])
        self.in_b.connect([self.A1.in2])
        self.in_c.connect([self.Or1.in2])
        self.A1.out.connect([self.Or1.in1, self.A2.in2])
        self.Or1.out.connect([self.A2.in1])
        self.A2.out.connect([self.out])


def main(a, b, c):
    c1 = Circuit('C1', 2)
    c1.in_a.set(a)
    c1.in_b.set(b)
    c1.in_c.set(c)


if __name__ == "__main__":
    main(0, 1, 0)

