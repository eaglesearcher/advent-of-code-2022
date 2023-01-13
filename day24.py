import file_io as fio
from queue import PriorityQueue


class Agent:
    def __init__(self, location, steps, end):
        self.location = location
        self.steps = steps
        self.heuristic = steps + get_distance(self.location, end)


class Blizzard:
    def __init__(self, x, y, direction, blizzard_map):
        map_height = len(blizzard_map)
        map_width = len(blizzard_map[0])
        self.location = (x, y)
        if direction == '>':
            self.direction = 0
            self.wrap = map_width - 2
        elif direction == 'v':
            self.direction = 1
            self.wrap = map_height - 2
        elif direction == '<':
            self.direction = 2
            self.wrap = map_width - 2
        elif direction == '^':
            self.direction = 3
            self.wrap = map_height - 2

    def move(self):
        x = self.location[0]
        y = self.location[1]
        if self.direction == 0:
            if x == self.wrap:
                x = 1
            else:
                x += 1
            self.location = (x, y)
        elif self.direction == 1:
            if y == self.wrap:
                y = 1
            else:
                y += 1
            self.location = (x, y)
        elif self.direction == 2:
            if x == 1:
                x = self.wrap
            else:
                x -= 1
            self.location = (x, y)
        elif self.direction == 3:
            if y == 0:
                y = self.wrap
            else:
                y -= 1
            self.location = (x, y)
        return


def create_base_map(map_height, map_width):

    map_data = []
    first_line_data = []
    for coord_i in range(0, map_width):
        first_line_data.append(0)
    first_line_data[1] = 1 # only valid square is the starting spot, needs to remain valid to enable "wait"

    base_line_data = [0]
    for coord_i in range(1, map_width-1):
        base_line_data.append(1)  # all squares are valid, except 1st and last
    base_line_data.append(0)

    last_line_data = []
    for coord_i in range(0, map_width):
        last_line_data.append(0)
    last_line_data[-2] = 1  # only valid square is the final spot

    map_data.append(first_line_data)
    for line_i in range(1, map_height-1):
        map_data.append(base_line_data.copy())
    map_data.append(last_line_data)

    return map_data


def get_distance(location1, location2):
    x1 = location1[0]
    y1 = location1[1]
    x2 = location2[0]
    y2 = location2[1]

    return abs(x1-x2)+abs(y1-y2)


def show_paths(path_map):
    for row_i in range(0, len(path_map)):
        print(path_map[row_i])
    return


def run():
    file_contents = fio.read_input(24, 0)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    blizzard_map = file_contents.split('\n')

    map_height = len(blizzard_map)
    map_width = len(blizzard_map[0])
    storm_history = []
    start = (1, 0)
    end = (map_width - 2, map_height - 1)
    max_iters = 20

    # generate all the storms and the path map at t = 0
    path_map = create_base_map(map_height, map_width)
    storm_list = []
    for row_i in range(1, map_height-1):
        for col_i in range(1, map_width-1):
            if blizzard_map[row_i][col_i] != '.':
                new_storm = Blizzard(col_i, row_i, blizzard_map[row_i][col_i], blizzard_map)
                path_map[row_i][col_i] = 0
                storm_list.append(new_storm)
    num_storms = len(storm_list)
    storm_history.append(path_map)

    # simulate the storms for a long time
    for time_i in range(0, max_iters):
        path_map = create_base_map(map_height, map_width)
        for storm_i in range(0, num_storms):
            current_storm = storm_list[storm_i]
            current_storm.move()
            path_map[current_storm.location[1]][current_storm.location[0]] = 0
        storm_history.append(path_map)



    # get started exploring
    prospects = PriorityQueue()
    agent_id = -1

    new_agent = Agent(start, 0, end)
    agent_id += 1
    prospects.put((new_agent.heuristic, agent_id, new_agent))

    winner = 0
    for i in range(0, max_iters):  # 10M
        if prospects.qsize() == 0:
            print('Ran out of agents, nobody got home!')
            break

        current_prospect = prospects.get()
        agent = current_prospect[2]
        current_time = agent.steps + 1
        current_storm = storm_history[current_time]
        print('Checking Agent', current_prospect[1])

        if agent.location == end:
            winner = 1
            # print('Path -', current_agent.history)
            break

        # get options

        # option 1: wait
        x = agent.location
        # if


    if winner:
        print('Victory! Final step count:', current_time)
        print('Spawned', agent_id, 'agents')

    # show_paths(storm_history[8])


    # for i in range(0, map_height):
    #     print(storm_history[0][i])


    # print(get_distance(start, end))

    # for row_i in range(0, map_height):
    #     for col_i in range(0, map_width):
    #         print(blizzard_map[row_i][col_i])



    part1 = 0
    part2 = 0

    return [part1, part2]
