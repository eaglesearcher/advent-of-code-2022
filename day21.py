import file_io as fio


def find_monkey(text, monkey_list, num_monkeys):
    for monkey_i in range(0, num_monkeys):
        if monkey_list[monkey_i][0:4] == text:
            return monkey_i
    return -1


def parse_monkey(index, monkeys, num_monkeys, human):
    segments = monkeys[index].split(' ')
    yell = 0
    if len(segments) > 2:  # need to process an operation, do recursion for number
        # get monkey 1 value
        monkey1_label = segments[1]
        monkey1_index = find_monkey(monkey1_label,monkeys, num_monkeys)
        # print(monkey_list[monkey1_index])
        monkey1_yell = parse_monkey(monkey1_index, monkeys, num_monkeys, human)
        # monkey1_yell = 0
        # print(monkey1_index, monkey_list[monkey1_index])

        # get monkey 2 value
        monkey2_label = segments[3]
        monkey2_index = find_monkey(monkey2_label, monkeys, num_monkeys)
        # print(monkey_list[monkey2_index])
        monkey2_yell = parse_monkey(monkey2_index, monkeys, num_monkeys, human)
        # monkey2_yell = 0
        # print(monkey2_index, monkey_list[monkey2_index])

        ops = segments[2]
        # do operation
        if ops == '+':
            # print('did a +')
            yell = monkey1_yell + monkey2_yell
        elif ops == '-':
            # print('did a -')
            yell = monkey1_yell - monkey2_yell
        elif ops == '*':
            # print('did a *')
            yell = monkey1_yell * monkey2_yell
        elif ops == '/':
            # print('did a /')
            yell = monkey1_yell / monkey2_yell
    else:  # returns a number
        if segments[0] == 'humn:':
            yell = human
        else:
            yell = int(segments[1])

    return yell


def contains_human(index, monkeys, num_monkeys):
    segments = monkeys[index].split(' ')
    if len(segments) == 2:  # this is a number monkey, does not contain humn
        return 0
    else:
        monkey1_label = segments[1]
        monkey2_label = segments[3]
        if monkey1_label == 'humn' or monkey2_label == 'humn':
            return 1
        else:
            monkey1_index = find_monkey(monkey1_label, monkeys, num_monkeys)
            monkey1_recursive = contains_human(monkey1_index, monkeys, num_monkeys)
            monkey2_index = find_monkey(monkey2_label, monkeys, num_monkeys)
            monkey2_recursive = contains_human(monkey2_index, monkeys, num_monkeys)
            if monkey1_recursive or monkey2_recursive: # humn is nested below
                return 1
    return 0


def run():
    file_contents = fio.read_input(21, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    monkey_list = file_contents.split('\n')
    num_monkeys = len(monkey_list)

    human_index = find_monkey('humn', monkey_list, num_monkeys)
    default_human = int(monkey_list[human_index].split(' ')[1])
    print('default human', default_human)


    root_index = find_monkey('root', monkey_list, num_monkeys)
    output_part1 = parse_monkey(root_index, monkey_list, num_monkeys, default_human)
    # print(int(output_part1))

    monkeys = monkey_list[root_index].split(' ')
    print(monkeys[1], monkeys[3])

    # trial 1
    human = 5

    second_index = find_monkey(monkeys[1], monkey_list, num_monkeys)
    output1 = parse_monkey(second_index, monkey_list, num_monkeys, human)
    # print(output1)
    second_index = find_monkey(monkeys[3], monkey_list, num_monkeys)
    output2 = parse_monkey(second_index, monkey_list, num_monkeys, human)
    # print(output2)

    # print(output2-output1)
    old_out = output2-output1

    old_x = 5
    new_x = 2*old_x

    for x_i in range(0, 4):
        human = new_x
        second_index = find_monkey(monkeys[1], monkey_list, num_monkeys)
        output1 = parse_monkey(second_index, monkey_list, num_monkeys, human)
        second_index = find_monkey(monkeys[3], monkey_list, num_monkeys)
        output2 = parse_monkey(second_index, monkey_list, num_monkeys, human)

        # print(output2-output1)
        new_out = output2 - output1

        if new_out == 0:
            break

        # newton's method -- find derivative and calculate new x
        slope = (new_out - old_out) / (new_x - old_x)
        old_x = new_x
        old_out = new_out
        new_x = old_x - (old_out / slope)  # actually the current / last iteration

    print('For human =', new_x, 'input monkeys are', output1, 'and', output2)


    part1 = output_part1
    part2 = 3848301405790

    return [part1, part2]
