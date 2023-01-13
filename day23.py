import file_io as fio


class Elf:
    def __init__(self, x, y):
        self.location = (x, y)
        self.proposed = (-1, -1)
        self.passed = 0

    def report(self):
        print('Elf at', self.location)
        return


def build_empty_map(map_lines, extra):
    map_height = len(map_lines)
    map_width = len(map_lines[0])

    # build up an empty 2D map -- do this explicitly to avoid python referencing behavior
    # the empty map also has an extra 10 squares on each side to allow growth
    map_data = []
    line_data = []
    for coord_i in range(0, map_width+extra*2):
        line_data.append(0)
    for line_i in range(0, map_height+extra*2):
        map_data.append(line_data.copy())

    return map_data


def build_map(map_lines, extra):
    input_map_height = len(map_lines)
    input_map_width = len(map_lines[0])

    # create map spaces to work in
    elf_map = build_empty_map(map_lines, extra)  # build up an empty map

    # parse the input data, and also build elves while we're at it
    elf_list = []

    for row_i in range(0, input_map_height):
        line = map_lines[row_i]
        for item_i in range(0, input_map_width):
            if line[item_i] == '#':
                elf_map[row_i + extra][item_i + extra] = 1
                new_elf = Elf(item_i + extra, row_i + extra)  # accounts for extra map width added in base map
                elf_list.append(new_elf)

    return elf_map, elf_list


def show_map(elf_map):
    for row_i in range(0, len(elf_map)):
        line = []
        row = elf_map[row_i]
        for item_i in range(0, len(row)):
            if row[item_i] == 1:
                line.append('#')
            else:
                line.append('.')
        print(''.join(line))
    return


def show_proposal_map(elf_map):
    for row_i in range(0, len(elf_map)):
        line = []
        row = elf_map[row_i]
        for item_i in range(0, len(row)):
            if row[item_i]:
                line.append(str(row[item_i]))
            else:
                line.append('.')
        print(''.join(line))
    return


def count_neighbors(elf, elf_map):
    x = elf.location[0]
    y = elf.location[1]

    # start at the count at -1, because the elf will check himself
    count = -1
    for i in range(0, 3):
        for j in range(0, 3):
            count += elf_map[y - 1 + i][x - 1 + j]

    return count


def check_positions(elf, elf_map, proposal_pointer):
    x = elf.location[0]
    y = elf.location[1]
    ptr = proposal_pointer % 4
    checks = []
    result = (0, 0)
    if ptr == 0:  # N (check NW, N, NE) [N is going towards row 0]
        checks = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        result = (x, y - 1)
    elif ptr == 1:  # S (check SW, S, SE) [S is going away from row 0]
        checks = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        result = (x, y + 1)
    elif ptr == 2:  # W (check SW, W, NW) [W is going towards col 0]
        checks = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        result = (x - 1, y)
    elif ptr == 3:  # E (check SE, E, NE) [E is going away from col 0]
        checks = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        result = (x + 1, y)

    count = 0
    for check_i in range(0, 3):
        check_x = checks[check_i][0]
        check_y = checks[check_i][1]
        count += elf_map[check_y][check_x]

    return count, result


def run():
    file_contents = fio.read_input(23, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    raw_map = file_contents
    map_lines = raw_map.split('\n')
    grid_extra = 200
    elf_map, elf_list = build_map(map_lines, grid_extra)
    num_elves = len(elf_list)
    proposal_pointer = 0
    for round_i in range(0, 1050):
        # print('Round #', round_i+1)
        # step 1: scout & propose movement
        proposal_map = build_empty_map(map_lines, grid_extra)  # build up an empty map
        for elf_i in range(0, num_elves):
        # for elf_i in range(0, 3):
            current_elf = elf_list[elf_i]
            current_elf.passed = 0  # doing the reset action first, no elves should be passed at this point
            # check if elf in empty field
            if not count_neighbors(current_elf, elf_map): # elf has no neighbors, so not moving
                current_elf.passed = 1
                continue
            success = 0
            for proposal_i in range(0, 4):  # elf will make 4 checks for proposals before giving up
                count, result = check_positions(current_elf, elf_map, proposal_pointer + proposal_i)
                # print('check direction', proposal_pointer+proposal_i, 'returns count', count)
                if not count: # nobody in the current direction, so successful proposal
                    current_elf.proposed = result
                    proposal_map[result[1]][result[0]] += 1
                    success = 1
                    break
            if not success:
                current_elf.passed = 1
                continue
            # print(elf_i, '-', elf_list[elf_i].location, '->', elf_list[elf_i].proposed)

        # step 2: process proposals & build new elf map along the way
        pass_counter = 0
        elf_map = build_empty_map(map_lines, grid_extra)  # build up an empty map
        for elf_i in range(0, num_elves):
            current_elf = elf_list[elf_i]
            location_x = current_elf.location[0]
            location_y = current_elf.location[1]
            if current_elf.passed:  # this elf already decided not to move; add to new map & skip
                pass_counter += 1
                elf_map[location_y][location_x] = 1
                continue
            proposed_x = current_elf.proposed[0]
            proposed_y = current_elf.proposed[1]
            if proposal_map[proposed_y][proposed_x] > 1: # more than 1 elf tried to move here; add to new map & abort move
                elf_map[location_y][location_x] = 1
                pass_counter += 1  # technically this counts as not moving
                continue
            else:
                current_elf.location = (proposed_x, proposed_y)  # move elf to new location
                elf_map[proposed_y][proposed_x] = 1  # update elf map

        # step 3: clean up
        proposal_pointer = (proposal_pointer + 1) % 4
        # show_map(elf_map)
        if pass_counter == num_elves:
            print('No elves moved on Round', round_i+1)
            break

    # show_map(elf_map)
    # show_proposal_map(proposal_map)

    max_x = 0
    min_x = 100
    max_y = 0
    min_y = 100
    # find the box
    for line_i in range(0, len(elf_map)):
        line = elf_map[line_i]
        for item_i in range(0, len(line)):
            if line[item_i] == 1:
                if item_i < min_x:
                    min_x = item_i
                if item_i > max_x:
                    max_x = item_i
                if line_i < min_y:
                    min_y = line_i
                if line_i > max_y:
                    max_y = line_i

    # print(min_x, max_x, min_y, max_y)

    empty_count = 0
    for line_i in range(min_y, max_y+1):
        line = elf_map[line_i]
        for item_i in range(min_x, max_x+1):
            if line[item_i] == 0:
                empty_count += 1

    # 73 x 73 = 5329
    # 6642 -- too high????

    part1 = empty_count
    part2 = round_i+1

    return [part1, part2]
