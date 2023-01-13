import file_io as fio


def run():

    file_contents = fio.read_input(3, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    all_bags = file_contents
    bags = all_bags.split("\n")

    # part 1
    sum_priority = 0
    for i in range(0, len(bags)):
        contents = bags[i]
        num_items = int(len(contents)/2)

        pouch1 = set(contents[0:num_items])
        pouch2 = set(contents[num_items:(num_items*2)])

        item_type = pouch1.intersection(pouch2)

        priority = ord(item_type.pop())-ord('a')+1
        # 'A'-'Z' have lower ASCII values than 'a'-'z', the absolute offset is 32 + another 26 to reach 27-52
        if priority < 0:
            priority = priority + 32+26

        sum_priority = sum_priority+priority

    # part 2
    sum_priority2 = 0
    for i in range(0, int(len(bags)/3)):
        contents1 = set(bags[0+i*3])
        contents2 = set(bags[1+i*3])
        contents3 = set(bags[2+i*3])

        badge = contents1.intersection(contents2)
        badge = badge.intersection(contents3)

        priority = ord(badge.pop()) - ord('a') + 1
        if priority < 0:
            priority = priority + 32 + 26

        sum_priority2 = sum_priority2 + priority

    part1 = sum_priority
    part2 = sum_priority2

    return [part1, part2]
