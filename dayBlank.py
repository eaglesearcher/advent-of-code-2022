import file_io as fio


def run():
    file_contents = fio.read_input(0, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    new_thing = file_contents

    part1 = 0
    part2 = 0

    return [part1, part2]
