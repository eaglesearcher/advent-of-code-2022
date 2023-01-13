import file_io as fio


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
            num_array.append(-1)
        if direction == '>':
            # print('go right')
            num_array.append(1)
    return num_array


class Shape:
    def __init__(self, identifier, spawn_height):
        self.id = identifier
        # first block == left-most (or tied)
        # second block == right-most (or tied)
        # third block is top (or tied)
        # fourth block is bottom (or tied)
        # fifth block only used for 5-block arrays
        self.blocks_x = [0]
        self.blocks_y = [0]
        self.num_blocks = 0
        self.set_blocks(spawn_height)

    def get_height(self):
        # third element is always the highest block
        return self.blocks_y[2]

    def set_blocks(self, y):
        if self.id == 0:  # flat block ID 0
            # self.blocks = [(2, y), (5, y), (3, y), (4, y)]
            self.blocks_x = [2, 5, 3, 4]
            self.blocks_y = [y, y, y, y]
            self.num_blocks = 4
        elif self.id == 1:  # plus block ID 1
            # self.blocks = [(2, y + 1), (4, y + 1), (3, y + 1), (3, y + 2), (3, y)]
            self.blocks_x = [2, 4, 3, 3, 3]
            self.blocks_y = [y + 1, y + 1, y + 2, y, y + 1]
            self.num_blocks = 5
        elif self.id == 2:  # L block ID 2
            # self.blocks = [(2, y), (4, y + 1), (4, y), (4, y + 2), (3, y)]
            self.blocks_x = [2, 4, 4, 3, 4]
            self.blocks_y = [y, y, y + 2, y, y+1]
            self.num_blocks = 5
        elif self.id == 3:  # tall block ID 3
            # self.blocks = [(2, y + 2), (2, y + 1), (2, y + 3), (2, y)]
            self.blocks_x = [2, 2, 2, 2]
            self.blocks_y = [y + 2, y + 1, y + 3, y]
            self.num_blocks = 4
        elif self.id == 4:  # square block ID 4
            # self.blocks = [(2, y), (3, y + 1), (2, y + 1), (3, y)]
            self.blocks_x = [2, 3, 2, 3]
            self.blocks_y = [y, y + 1, y + 1, y]
            self.num_blocks = 4

    def next_shape(self, height):
        self.id = (self.id + 1) % 5
        self.set_blocks(height)
        return


def drop(shape, grid):
    if shape.id == 0:
        x1 = shape.blocks_x[3]
        y1 = shape.blocks_y[3] - 1
        if grid[y1][x1] or grid[y1][x1 - 1] or grid[y1][x1 - 2] or grid[y1][x1 + 1]:
            return 0
        for block_i in range(0, 4):
            shape.blocks_y[block_i] -= 1
        return 1
    elif shape.id == 1:
        x1 = shape.blocks_x[3]
        y1 = shape.blocks_y[3] - 1
        if grid[y1][x1] or grid[y1+1][x1-1] or grid[y1+1][x1+1]:
            return 0
        for block_i in range(0, 5):
            shape.blocks_y[block_i] -= 1
        return 1
    elif shape.id == 2:
        x1 = shape.blocks_x[3]
        y1 = shape.blocks_y[3] - 1
        if grid[y1][x1] or grid[y1][x1-1] or grid[y1][x1+1]:
            return 0
        for block_i in range(0, 5):
            shape.blocks_y[block_i] -= 1
        return 1
    elif shape.id == 3:
        x1 = shape.blocks_x[3]
        y1 = shape.blocks_y[3] - 1
        if grid[y1][x1]:
            return 0
        for block_i in range(0, 4):
            shape.blocks_y[block_i] -= 1
        return 1
    elif shape.id == 4:
        x1 = shape.blocks_x[3]
        y1 = shape.blocks_y[3] - 1
        if grid[y1][x1] or grid[y1][x1-1]:
            return 0
        for block_i in range(0, 4):
            shape.blocks_y[block_i] -= 1
        return 1

    # new_blocks = []
    # for block_i in range(0, shape.num_blocks):
    #     y = shape.blocks_y[block_i] - 1
    #     if grid[y][shape.blocks_x[block_i]]:
    #         return 0
    #     new_blocks.append(y)
    # shape.blocks_y = new_blocks

    # for block_i in range(0, shape.num_blocks):
    #     shape.blocks_y[block_i] -= 1

    return 1


def drop_easy(shape):
    # first three steps, no checks
    for block_i in range(0, shape.num_blocks):
        shape.blocks_y[block_i] -= 1
    return


def slide(shape, grid, direction):
    # check edges first (easiest, no loop)
    if shape.blocks_x[0] + direction == -1 or shape.blocks_x[1] + direction == 7:
        return
    n = shape.num_blocks
    new_blocks = []
    for block_i in range(0, n):
        x = shape.blocks_x[block_i] + direction
        if grid[shape.blocks_y[block_i]][x]:
            return
        new_blocks.append(x)
    shape.blocks_x = new_blocks
    return


def slide_easy(shape, direction):
    # first block in array is always the left-most
    # second block in array is always the right-most
    if shape.blocks_x[0] + direction == -1 or shape.blocks_x[1] + direction == 7:
        return
    for block_i in range(0, shape.num_blocks):
        shape.blocks_x[block_i] += direction
    return


def travel3(shape, wind):
    x_l = shape.blocks_x[0]
    x_r = shape.blocks_x[1]

    direction = wind.get_next()
    net = direction
    if x_l + net == -1 or x_r + net == 7:
        net -= direction

    direction = wind.get_next()
    net += direction
    if x_l + net == -1 or x_r + net == 7:
        net -= direction

    direction = wind.get_next()
    net += direction
    if x_l + net == -1 or x_r + net == 7:
        net -= direction

    for block_i in range(0, shape.num_blocks):
        shape.blocks_x[block_i] += net
        shape.blocks_y[block_i] -= 3

    return


def create_base_grid(h):
    grid_bool = [[0] * 7] * h
    for i in range(1, h):
        grid_bool[i] = [0, 0, 0, 0, 0, 0, 0]
    grid_bool[0] = [1, 1, 1, 1, 1, 1, 1]
    return grid_bool


def update_grid(shape, grid_bool):
    for block_i in range(0, shape.num_blocks):
        x = shape.blocks_x[block_i]
        y = shape.blocks_y[block_i]
        grid_bool[y][x] = 1
    return


def roll_grid(grid_bool, half_max):
    for row_i in range(0, half_max):
        grid_bool[row_i] = grid_bool[row_i + half_max]
        grid_bool[row_i + half_max] = [0, 0, 0, 0, 0, 0, 0]
    return


def run():
    file_contents = fio.read_input(17, 0)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    pattern = file_contents
    windy = Wind(pattern)
    max_height = 0
    cheat = 0
    max_grid = 200
    half_max = int(max_grid/2)
    grid_bool = create_base_grid(max_grid)

    # grid_bool = create_base_grid(half_max)
    # grid_bool.append(grid_bool.copy())

    tetris = Shape(0, max_height + 4)
    block_counter = 1
    travel3(tetris, windy)

    # while block_counter != 5:
    # while block_counter != 2023:
    # while block_counter != 10000:  # 10K
    while block_counter != 100000:  # 100K
    # while block_counter != 1000000:  # 1M
    # for loop_i in range(0, 1):
        slide(tetris, grid_bool, windy.get_next())
        x = drop(tetris, grid_bool)
        if not x:
            update_grid(tetris, grid_bool)
            # update_grid_test(tetris, grid, grid_bool)
            test_height = tetris.get_height()
            if test_height > max_height:
                max_height = test_height
            # roll the grid if the spawning could be getting too close
            if test_height > max_grid - 5:
                roll_grid(grid_bool, half_max)
                max_height -= half_max
                cheat += half_max
            # tetris = next_shape(tetris, max_height + 4)
            tetris.next_shape(max_height + 4)
            # next_shape(tetris, max_height + 4)
            block_counter += 1
            # get three easy moves each for new block
            travel3(tetris, windy)



    # for i in range(0,3):
    #
    #     binary_rep = int(''.join(map(str,grid_bool[i])),2)
    #     # binary_rep = int('1111111',2)
    #
    #     print(binary_rep)




    print('Last block landed: #', block_counter-1)
    print('Max height:', max_height+cheat)
    # print('2023 max height:', 3068, '/', 3144, ', error: ', 3144 - max_height - cheat)
    # print('10K max height:', 15147, ', error: ', 15147 - max_height - cheat)
    print('100K max height:', 156491, ', error: ', 156491-max_height-cheat)
    # print('1M max height:', 1565199, ', error: ', 1565199 - max_height - cheat)

    part1 = 3144
    part2 = 0

    return [part1, part2]
