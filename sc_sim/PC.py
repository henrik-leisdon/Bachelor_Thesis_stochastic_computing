# in: set of bits
# out: parity value true or false
def x_or(a, b):
    if a == 0 and b == 1 or a == 1 and b == 0:
        return 1
    else:
        return 0


def parity_check(x_output):
    """checks if parity of the output is 0"""
    print('x_out: ' + str(x_output))
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

    return parity
