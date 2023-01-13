import file_io as fio
import numpy as np

class SandUnit:
    def __init__(self):
        self.position = (500, 0)
        self.rest = False

    def drop(self, Grid):
        x0 = self.position[0]
        y0 = self.position[1]

        # check bounds
        b1 = y0+1 > Grid.max_y  # sand fell off bottom of board
        b2 = x0-1 < Grid.min_x  # sand fell off left of board
        b3 = x0 + 1 > Grid.max_x  # sand fell off right of board
        if b1 or b2 or b3:
            Grid.stable = True
            self.rest = True
            return
        test_position = (x0, y0 + 1)  # 1) check straight down
        test = {test_position}.issubset(Grid.block)
        if test:  # path 1 blocked!
            test_position = (x0-1, y0 + 1)  # 2) check down and to the left
            test = {test_position}.issubset(Grid.block)
            if test:  # path 2 blocked!
                test_position = (x0 + 1, y0 + 1)  # 3) check down and to the right
                test = {test_position}.issubset(Grid.block)
                if test:  # path 3 blocked!
                    self.rest = True
                    if y0 == 0:
                        Grid.stable = True
                    return
        self.position = test_position
        return

class GridObject:
    def __init__(self, coords):
        self.stable = False
        self.block = coords
        min_x, max_x, min_y, max_y = get_minmax(coords)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        grid = [[' '] * width] * height
        for i in range(0, height):
            grid[i] = ['.']*width

        num_pts = len(coords)
        coord_copy = coords.copy()
        for i in range(0, num_pts):
            pt = coord_copy.pop()
            x = pt[0]-min_x
            y = pt[1]
            # print(x+min_x,y, 'turns into', x, y)
            grid[y][x] = '#'
        grid[0][500-min_x] = '+'
        self.grid = grid

    def show(self):
        for i in range(0, len(self.grid)):
            print(' '.join(self.grid[i]))

    def add_sand(self, sand_position):
        x = sand_position[0]
        y = sand_position[1]
        self.block.add(sand_position)
        if self.max_x >= x >= self.min_x:
            if self.max_y >= y >= self.min_y:
                self.grid[y][x-self.min_x] = 's'
                return
        print('Out of bounds!')
        return


def parse_line(line):
    coords_txt = line.split(' -> ')
    num_coords = len(coords_txt)
    coords = [(0, 0)]*num_coords
    for i in range(0, num_coords):
        temp = coords_txt[i].split(',')
        x = int(temp[0])
        y = int(temp[1])
        coords[i] = (x,y)
    return coords


def get_points(coords):
    coord_set = {(0, 0)}
    coord_set.remove((0, 0))
    for i in range(1, len(coords)):
        x0 = coords[i - 1][0]
        x1 = coords[i][0]
        y0 = coords[i - 1][1]
        y1 = coords[i][1]
        xrange = 0
        yrange = 0
        num_pts = 0
        if x0 == x1:
            num_pts = abs(y1 - y0) + 1
            xrange = np.ones(num_pts) * x0
            yrange = np.linspace(y0, y1, num_pts)
        elif y0 == y1:
            num_pts = abs(x1 - x0) + 1
            yrange = np.ones(num_pts) * y0
            xrange = np.linspace(x0, x1, num_pts)
        for j in range(0, num_pts):
            coord_set.add((int(xrange[j]),int(yrange[j])))
    return coord_set


def make_coords(lines):
    coord_set = {(0, 0)}
    coord_set.remove((0, 0))
    for i in range(0, len(lines)):
        coords = parse_line(lines[i])
        coord_set.update(get_points(coords))
    return coord_set


def add_floor(coords):
    min_x, max_x, min_y, max_y = get_minmax(coords)
    floor_y = max_y + 2
    floor_min_x = min_x - floor_y
    floor_max_x = max_x + floor_y
    new_coords = get_points([(floor_min_x,floor_y),(floor_max_x,floor_y)])
    coords.update(new_coords)
    return


def get_minmax(coords):
    coord_copy = coords.copy()
    num_points = len(coord_copy)
    min_x = 1000
    max_x = 0
    min_y = 1000
    max_y = 0

    for i in range(0, num_points):
        pt = coord_copy.pop()
        x = pt[0]
        y = pt[1]
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    if min_y > 0:
        min_y = 0
    return min_x, max_x, min_y, max_y


def run():
    file_contents = fio.read_input(14, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    mapping = file_contents
    lines = mapping.split('\n')
    coords = make_coords(lines)
    add_floor(coords)
    Grid = GridObject(coords)
    # print('Starting grid')
    # Grid.show()
    # print(Grid.min_x)

    # for j in range(0, 1):
    sand_counter = 0
    while not Grid.stable:
        sand_counter = sand_counter + 1
        if sand_counter > 100000:  # arbitrary break
            break
        Sand = SandUnit()
        i = 0
        while Sand.rest == 0:
            Sand.drop(Grid)
            i = i+1
            if i > Grid.max_y+1: # sand fell too far without hitting rest
                print('Hold up!')
                break
        if not Grid.stable:
            Grid.add_sand(Sand.position)
        # Grid.show()
        # print('Sand unit', sand_counter, 'Board Stability: ', Grid.stable)

    Grid.show()


    print('Maximum sand (part 1, do not count last) = ', sand_counter-1)
    print('Maximum sand (part 2, count last) = ', sand_counter)

    part1 = 0
    part2 = 0

    return [part1, part2]
