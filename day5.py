import file_io as fio


class Stack:
    def __init__(self):
        self.crates = []

    def add_crate(self,new_crate):
        self.crates.append(new_crate)

    def remove_crate(self):
        self.crates.pop(-1)


def run():
    file_contents = fio.read_input(5, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    manifest = file_contents
    manifest = manifest.split('\n\n')
    full_stacks = manifest[0]
    instructions = manifest[1]

    layers = full_stacks.split('\n')
    num_layers_init = len(layers) - 1

    labels = layers[-1]
    num_stacks = int(max(list(labels)))


    # part 1

    all_stacks = [Stack()]*num_stacks
    for i in range(0,num_stacks):
        all_stacks[i] = Stack()

    for i in range(num_layers_init, 0, -1):
        layer_parse = list(layers[i-1])
        for j in range(0, num_stacks):
            new_crate = layer_parse[4*j+1]
            if new_crate != ' ':
                all_stacks[j].add_crate(new_crate)

    instruction_lines = instructions.split('\n')
    num_instructions = len(instruction_lines)

    for i in range(0, num_instructions):
        detail = instruction_lines[i].split(' ')
        move_count = int(detail[1])
        source = int(detail[3])-1
        destination = int(detail[5])-1

        for j in range(0, move_count):
            new_crate = all_stacks[source].crates[-1]
            # print(new_crate)
            all_stacks[source].remove_crate()
            all_stacks[destination].add_crate(new_crate)

    top = ''
    for i in range(0, num_stacks):
        # print(all_stacks[i].crates)
        top = top+all_stacks[i].crates[-1]

    # part 2

    all_stacks = [Stack()]*num_stacks
    for i in range(0,num_stacks):
        all_stacks[i] = Stack()

    for i in range(num_layers_init, 0, -1):
        layer_parse = list(layers[i-1])
        for j in range(0, num_stacks):
            new_crate = layer_parse[4*j+1]
            if new_crate != ' ':
                all_stacks[j].add_crate(new_crate)

    instruction_lines = instructions.split('\n')
    num_instructions = len(instruction_lines)

    for i in range(0, num_instructions):
        detail = instruction_lines[i].split(' ')
        move_count = int(detail[1])
        source = int(detail[3])-1
        destination = int(detail[5])-1

        temp_stack = Stack()
        for j in range(0, move_count):
            new_crate = all_stacks[source].crates[-1]
            # print(new_crate)
            all_stacks[source].remove_crate()
            temp_stack.add_crate(new_crate)

        for j in range(0, move_count):
            new_crate = temp_stack.crates[-1]
            # print(new_crate)
            temp_stack.remove_crate()
            all_stacks[destination].add_crate(new_crate)

    top2 = ''
    for i in range(0, num_stacks):
        # print(all_stacks[i].crates)
        top2 = top2+all_stacks[i].crates[-1]

    # print(top2)

    part1 = top
    part2 = top2

    return [part1, part2]