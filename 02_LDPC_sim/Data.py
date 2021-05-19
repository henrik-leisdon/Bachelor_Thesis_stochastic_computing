class Data:
    def __init__(self, name):
        self.name = name
        self.x_in = []
        self.y_in = [[], [], [], [], [], []]
        self.x_out = []
        self.y_out = [[], [], [], [], [], []]
        self.bitlength = 0
        self.tau = 0
        self.generation_method = 0

    def to_String(self):
        print(str(self.name) + ' x_in:' + str(self.x_in) + '\nx_out: ' + str(self.x_out))
        print('y_in:' + str(self.y_in) + '\ny_out: ' + str(self.y_out))
        print(' ')

    def reset(self):
        self.y_in = [[], [], [], [], [], []]
        self.x_out = []
        self.y_out = [[], [], [], [], [], []]

    def append_y_out(self, y):
        self.y_out[0].extend(y[0])
        self.y_out[1].extend(y[1])
        self.y_out[2].extend(y[2])
        self.y_out[3].extend(y[3])
        self.y_out[4].extend(y[4])
        self.y_out[5].extend(y[5])
