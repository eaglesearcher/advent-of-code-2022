import file_io as fio


def move_right_n(index, num_shifts, value_list):
    num_values = len(value_list)
    old_value = value_list[index]
    new_index = index
    for shift_i in range(1, num_shifts+1):
        new_index += 1
        new_index %= num_values
        value_list[new_index-1] = value_list[new_index]
    value_list[new_index] = old_value
    return


def move_left_n(index, num_shifts, value_list):
    num_values = len(value_list)
    old_value = value_list[index]
    new_index = index
    for shift_i in range(1, num_shifts+1):
        new_index -= 1
        value_list[new_index+1] = value_list[new_index]
        new_index %= num_values
    value_list[new_index] = old_value
    return


def run():
    file_contents = fio.read_input(20, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    encryption_list = file_contents.split('\n')
    num_values = len(encryption_list)
    # print(num_values)

    values = [(0,0)]*num_values
    for value_i in range(0, num_values):
        values[value_i] = (int(encryption_list[value_i])*811589153, value_i)
        if int(encryption_list[value_i]) == 0:
            zero_ref = value_i
    instructions = values.copy()
    # print(values)
    for mix_i in range(0, 10):
        for instruction_i in range(0, num_values):
            ref = instructions[instruction_i]
            shift = ref[0]
            new_index = values.index(ref)
            shift = shift % (num_values - 1)
            # print('Move', shift, ', value is at index =', new_index)
            if shift > 0:
                move_right_n(new_index, shift, values)
            elif shift < 0:
                move_left_n(new_index, -shift, values)
            # print(values)
        # print(values)
    #
    # print(values)
    zero_index = values.index((0, zero_ref))
    print('zero index', zero_index)
    sum = 0
    for i in range(1, 4):
        search_index = (i*1000+zero_index) % num_values
        search_value = values[search_index][0]
        print('at', search_index, 'value =', search_value)
        sum += search_value

    print('sum is', sum)

    # move_right_n(0, 1, values) # 1
    # print('move 1', values)
    # move_right_n(0, 2, values) # 2
    # print('move 2', values)
    # move_right_n(1, -3 % 6, values)  # -3
    # print('move -3', values)
    # move_right_n(2, 3, values)  # 3
    # print('move 3', values)
    # move_right_n(2, -2 % 6, values) # -2
    # print('move -2', values)
    # print('move 0', values) # 4
    # move_left_n(5, -4 % 6, values)
    # print('move 4', values)


    # -3397 - "not correct"
    # 11460 - too low

    # 20832 - too high

    part1 = 13883
    part2 = 19185967576920

    return [part1, part2]
