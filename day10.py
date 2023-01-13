import file_io as fio


def run():
    file_contents = fio.read_input(10, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    instruction_list = file_contents
    instructions = instruction_list.split('\n')
    num_instructions = len(instructions)
    # print(instructions)

    X = [0,1]
    t = [0,1]

    current_x = 1
    current_t = 1

    for i in range(0, num_instructions):
        command = instructions[i].split(' ')
        if command[0] == 'noop':
            current_t = current_t + 1
            X.append(current_x)
            t.append(current_t)
        if command[0] == 'addx':
            current_t = current_t + 1
            t.append(current_t)
            X.append(current_x)

            current_t = current_t + 1
            t.append(current_t)
            current_x = current_x + int(command[1])
            X.append(current_x)


    score = 0
    cycles = [20, 60, 100, 140, 180, 220]
    for i in cycles:
        score = score + i*X[i]

    draw = ['']*240
    for i in range(0,240):
        draw_position = i%40
        sprite_center = X[i+1]
        if draw_position >= sprite_center - 1:
            if draw_position <= sprite_center + 1:
                draw[i] = '#'
            else:
                draw[i] = '.'
        else:
            draw[i] = '.'

    for i in range(0, 6):
        str_draw = draw[(40*(i)):(40*(i+1))]
        print(''.join(str_draw))


    part1 = score
    part2 = 0

    return [part1, part2]