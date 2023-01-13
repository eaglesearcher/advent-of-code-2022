import file_io as fio
import random


class Square:
    def __init__(self, elevation, start, end):
        self.elevation = elevation
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.start = start
        self.end = end


def letter_to_elevation(letter):
    elevation = ord(letter)-ord('a')
    return elevation


def coord_to_index(row,column):
    return column + 8 * row


def run():
    file_contents = fio.read_input(12, 0)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    map_rows = file_contents.split('\n')
    map_height = len(map_rows)
    map_width = len(map_rows[0])
    num_of_squares = map_height*map_width

    map_list = [Square(0, 0, 0)] * num_of_squares
    for i in range(0, map_height):
        for j in range(0, map_width):
            row = map_rows[i]
            letter = row[j]
            start = 0
            end = 0
            if letter == 'S':
                letter = 'a'
                start = 1
                start_r = i
                start_c = j
            elif letter == 'E':
                letter = 'z'
                end = 1
            elevation = letter_to_elevation(letter)
            # print(letter, elevation)
            # map_list[j+8*i] = Square(elevation, start, end)
            map_list[coord_to_index(i,j)] = Square(elevation, start, end)

    for i in range(0, map_height):
        for j in range(0, map_width):
            spot = map_list[coord_to_index(i,j)]
            if i == 0:
                spot.up = 0
            else:
                spot2 = map_list[coord_to_index(i-1,j)]
                if spot2.elevation-1 <= spot.elevation:
                    spot.up = 1
            if i == map_height-1:
                spot.down = 0
            else:
                spot2 = map_list[coord_to_index(i+1,j)]
                if spot2.elevation-1 <= spot.elevation:
                    spot.down = 1
            if j == 0:
                spot.left = 0
            else:
                spot2 = map_list[coord_to_index(i,j-1)]
                if spot2.elevation-1 <= spot.elevation:
                    spot.left = 1
            if j == map_width-1:
                spot.down = 0
            else:
                spot2 = map_list[coord_to_index(i,j+1)]
                if spot2.elevation-1 <= spot.elevation:
                    spot.right = 1
            if spot.end == 1:
                spot.up = 0
                spot.down = 0
                spot.left = 0
                spot.right = 0


    # test = map_list[coord_to_index(0,0)]
    # print(test.up, test.down, test.left, test.right)
    # print(test.elevation)
    # print(test.start)
    # print(test.end)


    max_iters = 100
    trail_history = []
    trail_flag = []
    next_position = map_list[coord_to_index(start_r,start_c)]  # always start at 0,0

    r = start_r
    c = start_c

    for j in range(0,40):
        print(r,c)
        current_position = next_position
        trail_history.append((r,c))
        if current_position.end == 1:
            trail_flag = 1
            break
        options = [0, 1, 2, 3]
        if current_position.up == 0:
            options.remove(0)
        if current_position.down == 0:
            options.remove(1)
        if current_position.left == 0:
            options.remove(2)
        if current_position.right == 0:
            options.remove(3)
        if not options:
            trail_flag = 0
            break
        step = random.choice(options)
        # print(step)
        if step == 0:  # move up
            r = r - 1
            next_position = map_list[coord_to_index(r,c)]
            next_position.down = 0  # avoid backtrack
        elif step == 1:  # move down
            r = r + 1
            next_position = map_list[coord_to_index(r, c)]
            next_position.up = 0  # avoid backtrack
        elif step == 2:  # move left
            c = c - 1
            next_position = map_list[coord_to_index(r, c)]
            next_position.right = 0  # avoid backtrack
        elif step == 3:  # move right
            c = c + 1
            next_position = map_list[coord_to_index(r, c)]
            next_position.left = 0  # avoid backtrack


    print(trail_flag, len(trail_history))
    # print(map[i][j].elevation)

    # map[j+i*map_width] = Square()


    part1 = 0
    part2 = 0

    return [part1, part2]