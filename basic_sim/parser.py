from LDPC_sim import MSC
import json

class Parser:
    def __init__(self):
        self.name = 'parser'
        self.gatelist = []

    def parse(self):

        with open("circuit.json", 'r') as json_file:
            y = json.load(json_file)

        # object_dict: name:gate object
        obj_dict = {}
        # for every gate
        for key, value in y.items():
            # in every gate print subvalues/keys
            for subkey, subval in value.items():

                if subkey == 'type' and subval == 'input':
                    gate = MSC.Input(key)
                    obj_dict[key] = gate

                if subkey == 'type' and subval == 'xor':
                    gate = MSC.Input(key)
                    obj_dict[key] = gate

                if subkey == 'type' and subval == 'and':
                    gate = MSC.Input(key)
                    obj_dict[key] = gate

                if subkey == 'type' and subval == 'Update':
                    gate = MSC.Input(key)
                    obj_dict[key] = gate

        print(obj_dict)

        # con dict: name:connections
        con_dict = {}
        for key, value in y.items():
            for subkey, subvalue in value.items():
                if subkey == 'connection':
                    con_dict[key] = subvalue

        print(con_dict)

        for key, val in con_dict.items():
            #print(type(con_dict))
            # print(key, val)
            if len(val) != 0:
                print(val)
                for k in val:
                    print(k)
                    print(type(k))
                    print(k.items())
                    for subkey, subval in k.items():
                        print(subkey, subval)
                        obj_dict[val[1]].connect(getattr(obj_dict[key], val[0]))




            # print(getattr(obj_dict[key], 'name'))
            # print(getattr(obj_dict[key], 'in_1'))
            # obj_dict[key].connect()









def main():
    parser = Parser()
    parser.parse()


if __name__ == '__main__':
    main()





