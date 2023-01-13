import numpy as np
import file_io as fio


def run():
    file_contents = fio.read_input(1, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    calorie_list = file_contents
    calorie_list_split = calorie_list.split("\n\n")
    num_elves = len(calorie_list_split)
    elf_count = [0] * num_elves
    for i in range(0, num_elves):
        calorie_array = calorie_list_split[i].split("\n")
        num_items = len(calorie_array)
        calorie_sum = 0
        for j in range(0, num_items):
            calorie_sum = calorie_sum + int(calorie_array[j])
        elf_count[i] = calorie_sum

    top_elf = max(elf_count)
    combined_three = top_elf
    heaviest_elf = np.argmax(elf_count)
    elf_count[heaviest_elf] = 0
    combined_three = combined_three + max(elf_count)
    heaviest_elf = np.argmax(elf_count)
    elf_count[heaviest_elf] = 0
    combined_three = combined_three + max(elf_count)

    part1 = top_elf
    part2 = combined_three

    return [part1, part2]
