# in: set of bits
# out: parity value true or false
def x_or(a, b):
    if a == 0 and b == 1 or a == 1 and b == 0:
        return 1
    else:
        return 0


class ParityCheck:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def parity_check(x_output):
        """checks if parity of the output is 0"""
        parity = True
        for i in x_output:
            if i == -1:
                return False

        if x_or(x_or(x_output[0], x_output[2]), x_output[3]) != 0:
            parity = False
        if x_or(x_output[1], x_output[2]) != 0:
            parity = False
        if x_or(x_output[0], x_output[4]) != 0:
            parity = False
        if x_or(x_output[1], x_output[5]) != 0:
            parity = False
        # print(parity)
        return parity


def main():
    pc = ParityCheck
    for i in range(0,100):
        par = pc.parity_check([1, 0, 0, 1, 1, 0])
        print(par)
        # if par == False:
        #    print('fail')


if __name__ == '__main__':
    main()