import file_io as fio
from queue import PriorityQueue


class Node:
    def __init__(self, position, map_grid, history):
        self.position = position
        self.elevation = get_elevation(self.position, map_grid)
        self.past_cost = len(history)
        new_history = history.copy()
        new_history.append(self.position)
        self.history = new_history
        self.future_cost = estimate_future(self.position, map_grid)
        self.heuristic = self.past_cost + self.future_cost


def check_victory(chosen_node, map_grid):
    end = find_end(map_grid)
    return end == chosen_node.position


def explore(chosen_node, explored, map_grid):
    row = chosen_node.position[0]
    col = chosen_node.position[1]
    map_height = len(map_grid)
    map_width = len(map_grid[0])
    history = chosen_node.history
    current_el = get_elevation(chosen_node.position, map_grid)
    new = []
    if row > 0:  # check up, only if not on top
        new_row = row - 1
        new_col = col
        new_pos = (new_row, new_col)
        if explored[new_row][new_col] == 0:
            new_el = get_elevation(new_pos, map_grid)
            if new_el <= current_el+1:
                temp = Node(new_pos, map_grid, history)
                new.append(temp)
    if row < map_height-1:  # check down, only if not on bottom
        new_row = row + 1
        new_col = col
        new_pos = (new_row, new_col)
        if explored[new_row][new_col] == 0:
            new_el = get_elevation(new_pos, map_grid)
            if new_el <= current_el + 1:
                temp = Node(new_pos, map_grid, history)
                new.append(temp)
    if col > 0:  # check up, only if not on top
        new_row = row
        new_col = col - 1
        new_pos = (new_row, new_col)
        if explored[new_row][new_col] == 0:
            new_el = get_elevation(new_pos, map_grid)
            if new_el <= current_el + 1:
                temp = Node(new_pos, map_grid, history)
                new.append(temp)
    if col < map_width-1:  # check down, only if not on bottom
        new_row = row
        new_col = col + 1
        new_pos = (new_row, new_col)
        if explored[new_row][new_col] == 0:
            new_el = get_elevation(new_pos, map_grid)
            if new_el <= current_el + 1:
                temp = Node(new_pos, map_grid, history)
                new.append(temp)
    return new


def find_end(map_grid):
    map_height = len(map_grid)
    map_width = len(map_grid[0])
    flag = 0
    end_r = 0
    end_c = 0
    for r in range(0, map_height):
        for c in range(0, map_width):
            letter = map_grid[r][c]
            if letter == 'E':
                end_r = r
                end_c = c
                flag = 1
                break
    if flag == 0:
        print('End position not found!')
    return end_r, end_c


def find_start(map_grid):
    map_height = len(map_grid)
    map_width = len(map_grid[0])
    flag = 0
    start_r = 0
    start_c = 0
    for r in range(0, map_height):
        for c in range(0, map_width):
            letter = map_grid[r][c]
            if letter == 'S':
                start_r = r
                start_c = c
                flag = 1
                break
    if flag == 0:
        print('Start position not found!')
    return start_r, start_c


def set_explored(position, explored):
    explored[position[0]][position[1]] = 1


def estimate_future(position, map_grid):
    end = find_end(map_grid)
    current_elevation = get_elevation(position, map_grid)
    end_elevation = get_elevation(end, map_grid)
    current_r = position[0]
    end_r = end[0]
    current_c = position[1]
    end_c = end[1]
    estimate1 = abs(end_r - current_r)+abs(end_c-current_c)
    estimate2 = end_elevation - current_elevation
    return max(estimate1, estimate2)


def get_elevation(position, map_grid):
    row = position[0]
    column = position[1]
    letter = map_grid[row][column]
    if letter == 'S':
        letter = 'a'
    if letter == 'E':
        letter = 'z'
    elevation = letter_to_elevation(letter)
    return elevation


def letter_to_elevation(letter):
    elevation = ord(letter)-ord('a')
    return elevation


def run():
    file_contents = fio.read_input(12, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    full_map = file_contents
    map_grid = full_map.split('\n')
    map_height = len(map_grid)
    map_width = len(map_grid[0])
    # print(full_map)

    start_pos = find_start(map_grid)

    explored = [[0] * map_width] * map_height
    for i in range(0, map_height):
        explored[i] = [0] * map_width

    prospects = PriorityQueue()

    # set starting position
    history = []
    position = start_pos
    current_node = Node(position, map_grid, history)
    prospect_num = 1
    prospects.put((current_node.heuristic, prospect_num, current_node))
    set_explored(current_node.position, explored)

    success = 0
    # for i in range(0, 10):
    while not prospects.empty():
        if not prospects.empty():
            choice = prospects.get()
            current_node = choice[2]
            # print(current_node.position)
            if check_victory(current_node, map_grid):
                success = 1
                break
            else:
                new_prospects = explore(current_node, explored, map_grid)

                for j in range(0, len(new_prospects)):
                    prospect_num = prospect_num+1
                    prospects.put((new_prospects[j].heuristic, prospect_num, new_prospects[j]))
                    set_explored(new_prospects[j].position, explored)

    if success:
        step_count = current_node.past_cost
        print(step_count)

    part1 = 0
    part2 = 0

    return [part1, part2]
