def convert(prob_bitsteam):
    one_counter = 0

    for i in range(0, prob_bitsteam.length):
        if prob_bitsteam[i] == 1:
            one_counter += 1

    return one_counter/prob_bitsteam.length


class ParityCheck:
    def __init__(self, name):
        self.name = name


