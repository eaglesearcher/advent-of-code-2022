import file_io as fio
# import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics import tsaplots
import matplotlib.pyplot as plt


class Wind:
    def __init__(self, pattern):
        self.id = 0
        self.pattern = parse_pattern(pattern)
        self.length = len(self.pattern)

    def get_next(self):
        new = self.pattern[self.id]
        self.id = (self.id + 1) % self.length
        return new


def parse_pattern(pattern):
    num_array = []
    for item_i in range(0, len(pattern)):
        direction = pattern[item_i]
        if direction == '<':
            # print('go left')
            num_array.append(0)
        if direction == '>':
            # print('go right')
            num_array.append(1)
    return num_array


class Shape:
    def __init__(self, identifier, row_num):
        self.id = identifier
        self.blocks = [0]
        self.num_blocks = 0
        self.row_num = row_num
        self.check_id = 0
        self.set_blocks()

    def get_height(self):
        return self.row_num+self.num_blocks-1

    def set_blocks(self):
        if self.id == 0:  # flat block ID 0
            self.blocks = [120]
            self.num_blocks = 1
            self.check_id = 0
        elif self.id == 1:  # plus block ID 1
            self.blocks = [16, 56, 16]
            self.num_blocks = 3
            self.check_id = 1
        elif self.id == 2:  # L block ID 2
            self.blocks = [56, 32, 32]
            self.num_blocks = 3
            self.check_id = 0
        elif self.id == 3:  # tall block ID 3
            self.blocks = [8, 8, 8, 8]
            self.num_blocks = 4
            self.check_id = 0
        elif self.id == 4:  # square block ID 4
            self.blocks = [24, 24]
            self.num_blocks = 2
            self.check_id = 0

    def next_shape(self, height):
        self.id = (self.id + 1) % 5
        self.row_num = height
        self.set_blocks()
        return


def drop(shape, grid):
    # only need to check the bottom layer, except plus block ID 1
    if shape.blocks[0] & grid[shape.row_num - 1]:
        return 0
    if shape.check_id == 1 and shape.blocks[1] & grid[shape.row_num]:
        return
    shape.row_num -= 1
    return 1


def drop_easy(shape):
    # first 3 drops, no check required
    shape.row_num -= 1
    return


def slide(shape, grid, wind):
    new_blocks = []
    direction = wind.get_next()
    if direction:  # 1 == right (shift away from 0 <<), 0 == left (shift towards 0 >>)
        for block_i in range(0, shape.num_blocks):
            block_layer = shape.blocks[block_i] << 1
            if block_layer & grid[shape.row_num + block_i]:
                return
            new_blocks.append(block_layer)
    else:
        for block_i in range(0, shape.num_blocks):
            block_layer = shape.blocks[block_i] >> 1
            if block_layer & grid[shape.row_num + block_i]:
                return
            new_blocks.append(block_layer)
    shape.blocks = new_blocks
    return


def slide_easy(shape, wind):
    # always checking against empty layers
    # only need to check bottom layer, except for plus block which is 2nd layer
    direction = wind.get_next()
    check = shape.blocks[shape.check_id]
    if direction and not check > 127:  # 1 == right (shift away from 0 <<), 0 == left (shift towards 0 >>)
        for block_i in range(0, shape.num_blocks):
            shape.blocks[block_i] <<= 1
    elif not direction and not check % 4 == 2:
        for block_i in range(0, shape.num_blocks):
            shape.blocks[block_i] >>= 1
    return


def travel3(shape, wind):
    net = 0
    check = shape.blocks[shape.check_id]
    # 1 == right (shift away from 0 <<), 0 == left (shift towards 0 >>)

    direction = wind.get_next()
    if direction and not(net > -1 and check > (127 >> net)):
        net += 1
    elif not direction and not(net < 1 and (check >> -net) % 4 == 2):
        net -= 1

    direction = wind.get_next()
    if direction and not (net > -1 and check > (127 >> net)):
        net += 1
    elif not direction and not (net < 1 and (check >> -net) % 4 == 2):
        net -= 1

    direction = wind.get_next()
    if direction and not (net > -1 and check > (127 >> net)):
        net += 1
    elif not direction and not (net < 1 and (check >> -net) % 4 == 2):
        net -= 1

    direction = wind.get_next()
    if direction and not (net > -1 and check > (127 >> net)):
        net += 1
    elif not direction and not (net < 1 and (check >> -net) % 4 == 2):
        net -= 1

    if net > 0:
        for block_i in range(0, shape.num_blocks):
            shape.blocks[block_i] <<= net
    if net < 0:
        for block_i in range(0, shape.num_blocks):
            shape.blocks[block_i] >>= -net

    shape.row_num -= 3
    return


def create_base_grid(h):
    grid_bool = [0] * h
    for i in range(1, h):
        grid_bool[i] = 257
    grid_bool[0] = 511
    return grid_bool


def update_grid(shape, grid):
    row = shape.row_num
    for block_i in range(0, shape.num_blocks):
        grid[row+block_i] = shape.blocks[block_i] | grid[row+block_i]
        # x = shape.blocks_x[block_i]
        # y = shape.blocks_y[block_i]
        # grid_bool[y][x] = 1
    return


def roll_grid(grid_bool, half_max, running_wall):
    for row_i in range(0, half_max):
        running_wall.append(grid_bool[row_i])
        grid_bool[row_i] = grid_bool[row_i + half_max]
        grid_bool[row_i + half_max] = 257
    return


def run():
    file_contents = fio.read_input(17, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    pattern = file_contents
    windy = Wind(pattern)
    max_height = 0
    cheat = 0
    max_grid = 200
    half_max = int(max_grid/2)
    grid_bool = create_base_grid(max_grid)

    tetris = Shape(0, max_height + 4)
    block_counter = 1
    travel3(tetris, windy)
    running_wall = []
    running2 = [0]

    # while block_counter != 2023:
    # while block_counter != 10001:  # 10K
    # while block_counter != 100000:  # 100K
    while block_counter != 1000000:  # 1M
    # for loop_i in range(0, 19):
        x = drop(tetris, grid_bool)
        if not x:
            update_grid(tetris, grid_bool)
            test_height = tetris.get_height()
            if test_height > max_height:
                max_height = test_height
            # roll the grid if the spawning could be getting too close
            # if block_counter == block_max:
            #     break
            if test_height > max_grid - 5:
                roll_grid(grid_bool, half_max, running_wall)
                tetris.row_num -= half_max
                max_height -= half_max
                cheat += half_max
            tetris.next_shape(max_height + 4)
            running2.append(max_height + cheat)
            block_counter += 1
            # get three easy moves each for new block
            travel3(tetris, windy)
            continue
        slide(tetris, grid_bool, windy)


    # for row_i in range(0, 60):
    #     print(bin(grid_bool[row_i]))

    # # autocorrelation for height
    # for row_i in range(0, max_grid):
    #     running_wall.append(grid_bool[row_i])
    # x = sm.tsa.acf(running_wall, nlags=100000)
    # # plt.plot(x)
    #
    # for i in range(1, len(x)):
    #     if x[i] > 0.95:
    #         print('Best fit lag:', i, 'correlation', x[i])
    #         # break
    #
    # # plt.show()

    # # autocorrelation for height delta
    # running3 = [0]
    # for i in range(1, len(running2)):
    #     running3.append(running2[i]-running2[i-1])
    #
    # x = sm.tsa.acf(running3, nlags=10000)
    # for i in range(1, len(x)):
    #     if x[i] > 0.95:
    #         print('Best fit lag:', i, 'correlation', x[i])
    #         break
    # plt.plot(x)
    # plt.show()

    # for i in range(1, len(running_wall)):
    #     if running_wall[-1] == 257:
    #         running_wall.pop(-1)
    #     else:
    #         break
    # running_wall.pop(0)


    big_b = 1000000000000

    # # test puzzle input
    # f = 35
    # ref = 100
    # ref2 = ref + f
    # print('2nd ref - ', ref2)
    # ref_result = 157  # reference = 100
    # ref_result2 = 210  # ref = 135
    # delta_ref = ref_result2 - ref_result
    # remainder = (big_b - ref) % f
    # print('remainder is', remainder, 'test at ', ref+remainder)
    # ref_result3 = 184
    # result = ref_result + int((big_b - ref) / f) * delta_ref + (ref_result3-ref_result)
    # print('result', result, 'error', result-1514285714288)


    # real puzzle input
    f = 1755
    ref = 300000
    ref2 = ref + f
    print('2nd ref - ', ref2)
    ref_result = 469534  # reference = 30K
    ref_result2 = 472281  # ref = 30K+1755
    delta_ref = ref_result2 - ref_result
    print('delta height', delta_ref)
    remainder = (big_b - ref) % f
    print('remainder is', remainder, 'test at ', ref + remainder)
    ref_result3 = 471895
    result = ref_result + int((big_b - ref) / f) * delta_ref + (ref_result3 - ref_result)
    print('result', result)
    print('--')

    # 1570440480460 -- too high
    # 1565344011499 -- too high
    # 1565242165201
    # 1558427375492 -- too low


    # ref_result = 4649 # reference = 3000
    # ref_result2 = 8963 # ref = 6K
    # delta_ref = ref_result2 - ref_result
    # result = ref_result + int((big_b - 3000)/f)*delta_ref

    # print(delta_ref)

    print('Last block landed: #', block_counter-1)
    print('Max height:', max_height+cheat)
    # print('Max height (backup):', len(running_wall))
    # print('2023 max height:', 3068, '/', 3144, ', error: ', 3144 - max_height - cheat)
    # print('10K max height:', 15147, ', error: ', 15147 - max_height - cheat)
    # print('100K max height:', 156491, ', error: ', 156491-max_height-cheat)
    # print('1M max height:', 1565199, ', error: ', 1565199 - max_height - cheat)

    part1 = 3144
    part2 = 1565242165201

    return [part1, part2]
