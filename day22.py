import file_io as fio


class Sprite:
    def __init__(self, map_grid):
        self.loc_x = 0
        self.loc_y = 1  # we added a line at the top of the map, so start on "2nd" row
        self.facing = 0
        self.map = map_grid
        self.part = 1

    def report(self):
        print('Current State: x =', self.loc_x, ', y =', self.loc_y, ', facing =', self.facing)
        return

    def turn_left(self):
        self.facing -= 1
        self.facing %= 4
        return

    def turn_right(self):
        self.facing += 1
        self.facing %= 4
        return

    def walk(self):
        if self.facing == 0:
            return self.go_right()
        elif self.facing == 1:
            return self.go_down()
        elif self.facing == 2:
            return self.go_left()
        elif self.facing == 3:
            return self.go_up()
        return 0

    def go_right(self):
        new_x = self.loc_x + 1
        check = self.map[self.loc_y][new_x]
        if check == 1:  # this is a valid location to step
            self.loc_x = new_x
            return 1
        elif not check:  # we hit a void, need to warp around, if possible
            return self.pick_tp(new_x, self.loc_y)
        return 0

    def go_left(self):
        new_x = self.loc_x - 1
        check = self.map[self.loc_y][new_x]
        if check == 1:  # this is a valid location to step
            self.loc_x = new_x
            return 1
        elif not check:  # we hit a void, need to warp around, if possible
            return self.pick_tp(new_x, self.loc_y)
        return 0

    def go_up(self):
        new_y = self.loc_y - 1
        check = self.map[new_y][self.loc_x]
        if check == 1:  # this is a valid location to step
            self.loc_y = new_y
            return 1
        elif not check:  # we hit a void, need to warp around, if possible
            return self.pick_tp(self.loc_x, new_y)
        return 0

    def go_down(self):
        new_y = self.loc_y + 1
        check = self.map[new_y][self.loc_x]
        if check == 1:  # this is a valid location to step
            self.loc_y = new_y
            return 1
        elif not check:  # we hit a void, need to warp around, if possible
            return self.pick_tp(self.loc_x, new_y)
        return 0

    def pick_tp(self, x, y):
        if self.part == 1:
            return self.teleporter(x, y)
        elif self.part == 2:
            return self.teleporter2(x, y)
        return 0

    def teleporter(self, x, y):
        # TP cases are not exhaustive -- assuming teleporter only gets called on valid void edges

        # check all the top / bottom edges first
        if y == 0 and self.facing == 3:  # this only occurs if going up from squares "A" and "B"
            if 51 <= x <= 100:  # up from square A
                if self.map[150][x] == 1:  # new position is valid, go there
                    self.loc_y = 150
                    # self.loc_x = x
                    return 1
            elif 101 <= x <= 150:  # up from square B
                if self.map[50][x] == 1:  # new position is valid, go there
                    self.loc_y = 50
                    # self.loc_x = x
                    return 1

        elif y == 100 and self.facing == 3:  # this only occurs if going up from square "E"
            if 1 <= x <= 50:  # up from square E
                if self.map[200][x] == 1:  # new position is valid, go there
                    self.loc_y = 200
                    # self.loc_x = x
                    return 1

        elif y == 51 and self.facing == 1:  # this only occurs if going down from square "B"
            if 101 <= x <= 150:  # down from square B
                if self.map[1][x] == 1:  # new position is valid, go there
                    self.loc_y = 1
                    # self.loc_x = x
                    return 1

        elif y == 151 and self.facing == 1:  # this only occurs if going down from square "D"
            if 51 <= x <= 101:  # down from square D
                if self.map[1][x] == 1:  # new position is valid, go there
                    self.loc_y = 1
                    # self.loc_x = x
                    return 1

        elif y == 201 and self.facing == 1:  # this only occurs if going down from square "F"
            if 1 <= x <= 50:  # down from square F
                if self.map[101][x] == 1:  # new position is valid, go there
                    self.loc_y = 101
                    # self.loc_x = x
                    return 1

        # check all the left / right edges
        elif x == 50 and self.facing == 2:  # this only occurs if going left from squares "A" and "C"
            if 1 <= y <= 50:  # left from square A
                if self.map[y][150] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 150
                    return 1
            elif 51 <= y <= 100:  # left from square C
                if self.map[y][100] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 100
                    return 1

        elif x == 0 and self.facing == 2:  # this only occurs if going left from squares "E" and "F"
            if 101 <= y <= 150:  # left from square E
                if self.map[y][100] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 100
                    return 1
            elif 151 <= y <= 200:  # left from square F
                if self.map[y][50] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 50
                    return 1

        elif x == 151 and self.facing == 0:  # this only occurs if going right from square "B"
            if 1 <= y <= 50:  # right from square B
                if self.map[y][51] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 51
                    return 1

        elif x == 101 and self.facing == 0:  # this only occurs if going right from squares "C" and "D"
            if 51 <= y <= 100:  # right from square C
                if self.map[y][51] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 51
                    return 1
            elif 101 <= y <= 150:  # right from square D
                if self.map[y][1] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 1
                    return 1

        elif x == 51 and self.facing == 0:  # this only occurs if going right from square "F"
            if 151 <= y <= 200:  # right from square F
                if self.map[y][1] == 1:  # new position is valid, go there
                    # self.loc_y = y
                    self.loc_x = 1
                    return 1

        return 0

    def teleporter2(self, x, y):
        # TP cases are not exhaustive -- assuming teleporter only gets called on valid void edges
        # check all the top / bottom edges first
        if y == 0 and self.facing == 3:  # this only occurs if going up from squares "A" and "B"
            if 51 <= x <= 100:  # up from square A
                new_x = 1
                new_y = x + 100
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 0
                    return 1
            elif 101 <= x <= 150:  # up from square B
                new_x = x - 100
                new_y = 200
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    # same facing
                    return 1

        elif y == 100 and self.facing == 3:  # this only occurs if going up from square "E"
            if 1 <= x <= 50:  # up from square E
                new_x = 51
                new_y = x + 50
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 0
                    return 1

        elif y == 51 and self.facing == 1:  # this only occurs if going down from square "B"
            if 101 <= x <= 150:  # down from square B
                new_x = 100
                new_y = x - 50
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 2
                    return 1

        elif y == 151 and self.facing == 1:  # this only occurs if going down from square "D"
            if 51 <= x <= 101:  # down from square D
                new_x = 50
                new_y = x + 100
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 2
                    return 1

        elif y == 201 and self.facing == 1:  # this only occurs if going down from square "F"
            if 1 <= x <= 50:  # down from square F
                new_x = x + 100
                new_y = 1
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    # same facing
                    return 1

        # check all the left / right edges
        elif x == 50 and self.facing == 2:  # this only occurs if going left from squares "A" and "C"
            if 1 <= y <= 50:  # left from square A
                new_x = 1
                new_y = 151 - y
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 0
                    return 1
            elif 51 <= y <= 100:  # left from square C
                new_x = y - 50
                new_y = 101
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 1
                    return 1

        elif x == 0 and self.facing == 2:  # this only occurs if going left from squares "E" and "F"
            if 101 <= y <= 150:  # left from square E
                new_x = 51
                new_y = 151 - y
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 0
                    return 1
            elif 151 <= y <= 200:  # left from square F
                new_x = y - 100
                new_y = 1
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 1
                    return 1

        elif x == 151 and self.facing == 0:  # this only occurs if going right from square "B"
            if 1 <= y <= 50:  # right from square B
                new_x = 100
                new_y = 151 - y
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 2
                    return 1

        elif x == 101 and self.facing == 0:  # this only occurs if going right from squares "C" and "D"
            if 51 <= y <= 100:  # right from square C
                new_x = y + 50
                new_y = 50
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 3
                    return 1
            elif 101 <= y <= 150:  # right from square D
                new_x = 150
                new_y = 151 - y
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 2
                    return 1

        elif x == 51 and self.facing == 0:  # this only occurs if going right from square "F"
            if 151 <= y <= 200:  # right from square F
                new_x = y - 100
                new_y = 150
                if self.map[new_y][new_x] == 1:  # new position is valid, go there
                    self.loc_y = new_y
                    self.loc_x = new_x
                    self.facing = 3
                    return 1

        return 0


def build_map(map_lines):
    num_lines = len(map_lines)

    map_width = 0
    for line_i in range(0, len(map_lines)):
        line_width = len(map_lines[line_i])
        if line_width > map_width:
            map_width = line_width

    # expand the map by 1 on each edge -- this guarantees we hit a void/teleport instead of hitting map edge
    map_width += 2
    num_lines += 2
    # this also means that the map is effectively 1-referenced, instead of 0-referenced
    # for the puzzle solution, we can read row/column directly

    # build up an empty 2D map -- do this explicitly to avoid python referencing behavior
    map_data = []
    line_data = []
    for coord_i in range(0, map_width):
        line_data.append(0)
    for line_i in range(0, num_lines):
        map_data.append(line_data.copy())

    # add the map data -- remember that we skip row/column 0, so all coordinates + 1
    for line_i in range(0, len(map_lines)):
        line = map_lines[line_i]
        for coord_i in range(0, len(line)):
            if line[coord_i] == '.':
                map_data[line_i+1][coord_i+1] = 1
            elif line[coord_i] == '#':
                map_data[line_i+1][coord_i+1] = 2

    return map_data


def show_map(map_data):
    for i in range(0, len(map_data)):
        print(map_data[i])
    return


def show_map_with_sprite(map_data, agent):
    x = agent.loc_x
    y = agent.loc_y
    map_data[y][x] = 7
    for i in range(0, len(map_data)):
        line = []
        for j in range(0, len(map_data[i])):
            if map_data[i][j] == 0:
                line.append(' ')
            elif map_data[i][j] == 1:
                line.append('.')
            elif map_data[i][j] == 2:
                line.append('#')
            elif map_data[i][j] == 7:
                line.append('A')
        print(''.join(line))

    # for i in range(0, len(map_data)):
    #     print(map_data[i])
    map_data[y][x] = 1  # if we're standing there, it must have been a valid square
    return


def read_instructions(instructions):
    # turn this into a csv by inserting commas before letters, because it's easier to parse that way
    num_chars = len(instructions)
    new_list = ['R']  # we're starting with a R to maintain consistency -- Turn then number (need to pre-turn left)
    for char_i in range(0, num_chars):
        if instructions[char_i] == 'R' or instructions[char_i] == 'L':
            new_list.append(',')
        new_list.append(instructions[char_i])
    new_list = ''.join(new_list)
    instruction_list = new_list.split(',')
    return instruction_list


def run():
    file_contents = fio.read_input(22, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    all_things = file_contents.split('\n\n')
    the_map = all_things[0]
    instructions_txt = all_things[1]

    map_lines = the_map.split('\n')
    # num_lines = len(map_lines)
    map_data = build_map(map_lines)
    start_index = map_data[1].index(1)
    # show_map(map_data)

    instructions = read_instructions(instructions_txt)
    num_instructions = len(instructions)

    # create our sprite to store state
    agent = Sprite(map_data)
    agent.loc_x = start_index  # default start
    agent.loc_y = 1  # default start
    agent.facing = 0  # default facing
    agent.part = 1

    print('Starting State:')
    agent.report()

    agent.turn_left()  # corrects for the fact that we appended a right turn to the first instruction
    for instruction_i in range(0, num_instructions):
        next_instruction = instructions[instruction_i]
        direction = next_instruction[0]
        counter = int(next_instruction[1:])
        # print(direction, counter)
        if direction == 'L':
            agent.turn_left()
        elif direction == 'R':
            agent.turn_right()
        for i in range(0, counter):
            if not agent.walk():
                break
        # agent.report()

    print('Final State:')
    agent.report()
    # show_map_with_sprite(map_data, agent)

    # print(direction, counter)
    part1_score = 1000 * agent.loc_y + 4 * agent.loc_x + agent.facing

    # create our sprite to store state (part 2)
    agent = Sprite(map_data)
    agent.loc_x = start_index  # default start
    agent.loc_y = 1  # default start
    agent.facing = 0  # default facing
    agent.part = 2

    print('Starting State (part 2):')
    agent.report()

    agent.turn_left()  # corrects for the fact that we appended a right turn to the first instruction
    for instruction_i in range(0, num_instructions):
        next_instruction = instructions[instruction_i]
        direction = next_instruction[0]
        counter = int(next_instruction[1:])
        # print(direction, counter)
        if direction == 'L':
            agent.turn_left()
        elif direction == 'R':
            agent.turn_right()
        for i in range(0, counter):
            if not agent.walk():
                break
        # agent.report()

    print('Final State (part 2):')
    agent.report()
    # show_map_with_sprite(map_data, agent)

    # print(direction, counter)
    part2_score = 1000 * agent.loc_y + 4 * agent.loc_x + agent.facing

    part1 = part1_score
    part2 = part2_score

    return [part1, part2]
