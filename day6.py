import file_io as fio


def run():
    file_contents = fio.read_input(6, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    code = file_contents
    code_length = len(code)

    # part 1
    for i in range(4, code_length):
        test_set = code[(i-4):(i)]
        test = set(test_set)
        if len(test) == 4:
            marker = i
            break

    # part 2
    for i in range(14, code_length):
        test_set = code[(i-14):(i)]
        test = set(test_set)
        if len(test) == 14:
            marker2 = i
            break

    part1 = marker
    part2 = marker2

    return [part1, part2]