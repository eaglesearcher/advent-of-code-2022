import file_io as fio


def run():
    file_contents = fio.read_input(4, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    all_assignments = file_contents
    pairs = all_assignments.split('\n')

    # part 1
    score = 0
    for i in range(0,len(pairs)):
        elves = pairs[i].split(',')

        first = elves[0].split('-')
        second = elves[1].split('-')

        elf1 = set(range(int(first[0]),int(first[1])+1))
        elf2 = set(range(int(second[0]), int(second[1]) + 1))

        redundant_test_1 = elf1.issubset(elf2)
        redundant_test_2 = elf2.issubset(elf1)

        fully_contained = redundant_test_1 or redundant_test_2
        score = score + fully_contained

    # part 2
    score2 = 0
    for i in range(0,len(pairs)):
        elves = pairs[i].split(',')

        first = elves[0].split('-')
        second = elves[1].split('-')

        elf1 = set(range(int(first[0]),int(first[1])+1))
        elf2 = set(range(int(second[0]), int(second[1]) + 1))

        overlap_test = elf1.intersection(elf2)

        overlapped = (len(overlap_test)>0)
        score2 = score2 + overlapped*1

    part1 = score
    part2 = score2

    return [part1, part2]