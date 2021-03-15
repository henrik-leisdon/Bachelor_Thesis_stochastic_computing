class Data:
    def __init__(self, name):
        self.name = name
        self.x_in = []
        self.y_in = [[], [], [], [], [], []]
        self.x_out = []
        self.y_out = [[], [], [], [], [], []]
        self.bitlength = 0
        self.tau = 0

    def set(self, y_in):
        self.y_in = y_in