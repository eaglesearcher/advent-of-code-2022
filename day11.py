import file_io as fio

class Monkey:
    def __init__(self,items,num,divider,tp,fp,input):
        self.items = items
        self.monkey_num = num
        self.divider = divider
        self.true_pass = tp
        self.false_pass = fp
        self.business = 0
        self.input = input

    def add_item(self,new_item):
        self.items.append(new_item)

    def inspect_item(self):
        shiny_object = self.items[0]
        self.items.pop(0)
        self.business = self.business + 1
        new_worry = monkey_function(self.monkey_num, shiny_object, self.input)
        # new_worry = int(new_worry/3)
        # new_worry = new_worry%96577
        return new_worry


def monkey_function(monkey_num, worry, input):
    if input == 0:
        if monkey_num == 0:
            worry = worry * 19
        elif monkey_num == 1:
            worry = worry + 6
        elif monkey_num == 2:
            worry = worry * worry
        elif monkey_num == 3:
            worry = worry + 3
    if input == 1:
        if monkey_num == 0:
            worry = worry * 3
        elif monkey_num == 1:
            worry = worry * 11
        elif monkey_num == 2:
            worry = worry + 6
        elif monkey_num == 3:
            worry = worry + 4
        elif monkey_num == 4:
            worry = worry + 8
        elif monkey_num == 5:
            worry = worry + 2
        elif monkey_num == 6:
            worry = worry * worry
        elif monkey_num == 7:
            worry = worry + 5
    return worry


def run():

    input = 1
    file_contents = fio.read_input(11, input)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    monkey_list = file_contents
    monkey_stats = monkey_list.split('\n\n')
    number_of_monkeys = len(monkey_stats)

    monkeys = [Monkey('','','','','','')]*number_of_monkeys
    worry_divider = 1
    for i in range(0, number_of_monkeys):
        statlines = monkey_stats[i].split('\n')

        tmp = statlines[1].split(': ')
        starter_items = tmp[1].split(', ')
        num_items = len(starter_items)
        items = [0]*num_items
        for j in range(0, num_items):
            items[j] = int(starter_items[j])

        tmp = statlines[3].split(' ')
        divider = int(tmp[-1])

        tmp = statlines[4].split(' ')
        true_pass = int(tmp[-1])

        tmp = statlines[5].split(' ')
        false_pass = int(tmp[-1])

        monkeys[i] = Monkey(items, i, divider, true_pass, false_pass,input)
        worry_divider = worry_divider * divider

    for i in range(0, 10000):

        for j in range(0, number_of_monkeys):
            # j = 0  # monkey rotater
            num_items = len(monkeys[j].items)
            for k in range(0, num_items):  # item looper
                shiny = monkeys[j].inspect_item()
                shiny = shiny%worry_divider
                test = shiny%monkeys[j].divider
                if test == 0:
                    pass_to = monkeys[j].true_pass
                else:
                    pass_to = monkeys[j].false_pass
                monkeys[pass_to].add_item(shiny)

    snoops = [0]*number_of_monkeys
    for i in range(0, number_of_monkeys):
        # print('Monkey ', i, ' - ', monkeys[i].items, ' - MB: ', monkeys[i].business)
        print('Monkey', i, ': ', monkeys[i].business)
        snoops[i] = monkeys[i].business
    snoops.sort()
    monkey_business = snoops[-1]*snoops[-2]

    part1 = monkey_business
    part2 = 0

    return [part1, part2]