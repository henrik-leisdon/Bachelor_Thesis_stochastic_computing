def main(input):

    # row 1
    y_0_p = input[2] * (1 - input[3]) + input[3] * (1 - input[2])
    y_2_p = input[0] * (1 - input[3]) + input[3] * (1 - input[0])
    y_3_p = input[0] * (1 - input[2]) + input[2] * (1 - input[0])

    # row 2
    y_1_p = input[2]
    y_2_p2 = input[1]

    # row 3
    y_0_p2 = input[4]
    y_4_p = input[0]

    # row 4
    y_1_p2 = input[5]
    y_5_p = input[1]

    y_0 = (y_0_p * y_0_p2) / ((y_0_p * y_0_p2) + (1 - y_0_p) * (1 - y_0_p2))
    y_1 = (y_1_p * y_1_p2) / ((y_1_p * y_1_p2) + (1 - y_1_p) * (1 - y_1_p2))
    y_2 = (y_2_p * y_2_p2) / ((y_2_p * y_2_p2) + (1 - y_2_p) * (1 - y_2_p2))

    print("y_0' = {0} * (1 - {1}) + {1} * (1 - {0}) = {2}".format(input[2], input[3], round(y_0_p, 2)))
    print("y_2' = {0} * (1 - {1}) + {1} * (1 - {0}) = {2}".format(input[1], input[3], round(y_2_p, 2)))
    print("y_3' = {0} * (1 - {1}) + {1} * (1 - {0}) = {2}\n".format(input[1], input[2], round(y_3_p, 2)))

    print("y_0 = ({0} * {1}) / ({0} * {1}) + (1 - {0}) * (1 - {1})= {2}".format(round(y_0_p, 2), round(y_0_p2, 2),
                                                                                round(y_0, 2)))
    print("y_1 = ({0} * {1}) / ({0} * {1}) + (1 - {0}) * (1 - {1})= {2}".format(round(y_1_p, 2), round(y_1_p2, 2),
                                                                                round(y_1, 2)))
    print("y_2 = ({0} * {1}) / ({0} * {1}) + (1 - {0}) * (1 - {1})= {2}\n".format(round(y_2_p, 2), round(y_2_p2, 2),
                                                                                round(y_2, 2)))

    print('y_0 = {}'.format(round(y_0, 2)))
    print('y_1 = {}'.format(round(y_1, 2)))
    print('y_2 = {}'.format(round(y_2, 2)))
    print('y_3 = {}'.format(round(y_3_p, 2)))
    print('y_4 = {}'.format(round(y_4_p, 2)))
    print('y_5 = {}'.format(round(y_5_p, 2)))

    print('[{0}, {1}, {2}, {3}, {4}, {5}]'.format(round(y_0, 2), round(y_1, 2), round(y_2, 2), round(y_3_p, 2),
          round(y_4_p, 2), round(y_5_p, 2)))


if __name__ == '__main__':
    input1 = [0, 0, 0, 1, 1, 1]

    it = 0
    for item in input1:
        y_i = item * (1 - 0.1) + (1 - item) * 0.1
        # print(y_i)
        input1[it] = y_i
        it += 1

    input2 = [0.07, 0.05, 0.81, 0.65, 0.98, 0.5]

    main(input2)
