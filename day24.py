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
            if y == 1:
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


def create_empty_map(map_height, map_width):

    map_data = []
    base_line_data = []
    for coord_i in range(0, map_width):
        base_line_data.append(0)  # all squares are valid, except 1st and last

    for line_i in range(0, map_height):
        map_data.append(base_line_data.copy())

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


def show_map_enhanced(path_map, agent):
    x = agent.location[0]
    y = agent.location[1]

    for row_i in range(0, len(path_map)):
        line = path_map[row_i]
        txt_line = []
        for col_i in range(0, len(line)):
            if row_i == y and col_i == x:
                txt_line.append('A')
            elif line[col_i]:
                txt_line.append('.')
            else:
                txt_line.append('#')
        print(''.join(txt_line))
    return


def run():
    file_contents = fio.read_input(24, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    blizzard_map = file_contents.split('\n')
    map_height = len(blizzard_map)
    map_width = len(blizzard_map[0])
    start = (1, 0)
    end = (map_width - 2, map_height - 1)
    max_iters = 2000

    # generate all the storms and the path map at t = 0
    path_map = create_base_map(map_height, map_width)
    storm_history = []
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
        # for storm_i in range(0, 1):
        #     storm_i = 3
            current_storm = storm_list[storm_i]
            current_storm.move()
            # print(current_storm.location)
            path_map[current_storm.location[1]][current_storm.location[0]] = 0
        storm_history.append(path_map)

    # i = 1
    # print('storm')
    # show_paths(storm_history[i])


    # generate a visitation history
    visit_history = []
    for time_i in range(0, max_iters):
        visit_map = create_empty_map(map_height, map_width)
        visit_history.append(visit_map)

    # get started exploring -- start to finish, first time
    prospects = PriorityQueue()
    agent_id = -1

    new_agent = Agent(start, 0, end)
    agent_id += 1
    prospects.put((new_agent.heuristic, agent_id, new_agent))

    winner = 0
    for i in range(0, 400000):
        if prospects.qsize() == 0:
            print('Ran out of agents, nobody got home!')
            break

        current_prospect = prospects.get()
        agent = current_prospect[2]
        new_time = agent.steps + 1  # need to look ahead for most checks
        current_storm = storm_history[new_time]
        # print('Checking Agent', current_prospect[1], 'at location', agent.location, 'and time', agent.steps, '; current guess', agent.heuristic)

        if agent.location == end:
            winner = 1
            # print('Path -', current_agent.history)
            break

        # get options
        x = agent.location[0]
        y = agent.location[1]

        # check prior visitation -- helps to avoid weirdly convergent paths
        # still have to pop repeated agents, but this keeps them from spawning the same new agents
        check = visit_history[agent.steps][y][x]
        if not check:
            visit_history[agent.steps][y][x] = 1

            # option 1: wait
            if current_storm[y][x] == 1:  # moving storm may mean can't wait here
                new_agent = Agent((x, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 2: go north (catch initial conditions, never return to start)
            if y > 1 and current_storm[y - 1][x] == 1:  # never want to go north from row 1, regardless
                new_agent = Agent((x, y - 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 3: go south
            if current_storm[y + 1][x] == 1:
                new_agent = Agent((x, y + 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 4: go east
            if current_storm[y][x + 1] == 1:
                new_agent = Agent((x + 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 5: go west
            if current_storm[y][x - 1] == 1:
                new_agent = Agent((x - 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

        # end agent loop

    # show_map_enhanced(storm_history[agent.steps+1], agent)

    if winner:
        print('Victory (part 1)! Final step count:', agent.steps)
        print('Spawned', agent_id, 'agents')
        print('--')

    elif prospects.qsize() > 0:
        print('No agent finished! X')
        print('Spawned New Agents:', agent_id)
        print('Next X agents:')
        for i in range(0, min(10, prospects.qsize())):
            current_prospect = prospects.get()
            agent = current_prospect[2]
            print('Location -', agent.location, 'Time -', agent.steps, 'Guess -', agent.heuristic)

    part1_score = agent.steps


    # Part 2 -- REVERSE TRIP

    # invert start and end
    start = (map_width - 2, map_height - 1)
    end = (1, 0)

    # generate a new visitation history, just in case
    visit_history = []
    for time_i in range(0, max_iters):
        visit_map = create_empty_map(map_height, map_width)
        visit_history.append(visit_map)

    # get started exploring -- finish to start, reverse trip
    del prospects
    prospects = PriorityQueue()
    agent_id = -1

    # new_agent = Agent(start, 0, end)
    new_agent = Agent(start, agent.steps, end)
    agent_id += 1
    prospects.put((new_agent.heuristic, agent_id, new_agent))

    winner = 0
    for i in range(0, 400000):
        if prospects.qsize() == 0:
            print('Ran out of agents, nobody got home!')
            break

        current_prospect = prospects.get()
        agent = current_prospect[2]
        new_time = agent.steps + 1  # need to look ahead for most checks
        current_storm = storm_history[new_time]
        # print('Checking Agent', current_prospect[1], 'at location', agent.location, 'and time', agent.steps, '; current guess', agent.heuristic)

        if agent.location == end:
            winner = 1
            break

        # get options
        x = agent.location[0]
        y = agent.location[1]

        # check prior visitation -- helps to avoid weirdly convergent paths
        # still have to pop repeated agents, but this keeps them from spawning the same new agents
        check = visit_history[agent.steps][y][x]
        if not check:
            visit_history[agent.steps][y][x] = 1

            # option 1: wait
            if current_storm[y][x] == 1:  # moving storm may mean can't wait here
                new_agent = Agent((x, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 2: go north
            if current_storm[y - 1][x] == 1:
                new_agent = Agent((x, y - 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 3: go south (catch initial conditions, never return to start)
            if y < (map_height - 2) and current_storm[y + 1][x] == 1:
                new_agent = Agent((x, y + 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 4: go east
            if current_storm[y][x + 1] == 1:
                new_agent = Agent((x + 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 5: go west
            if current_storm[y][x - 1] == 1:
                new_agent = Agent((x - 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

        # end agent loop

    # show_map_enhanced(storm_history[agent.steps+1], agent)

    if winner:
        print('Victory (reverse)! Final step count:', agent.steps)
        print('Spawned', agent_id, 'agents')
        print('--')

    elif prospects.qsize() > 0:
        print('No agent finished! X')
        print('Spawned New Agents:', agent_id)
        print('Next X agents:')
        for i in range(0, min(10, prospects.qsize())):
            current_prospect = prospects.get()
            agent = current_prospect[2]
            print('Location -', agent.location, 'Time -', agent.steps, 'Guess -', agent.heuristic)



    # Part 2B -- ONCE MORE INTO THE WHITE

    # invert start and end (back to original)
    start = (1, 0)
    end = (map_width - 2, map_height - 1)


    # generate a new visitation history, just in case
    visit_history = []
    for time_i in range(0, max_iters):
        visit_map = create_empty_map(map_height, map_width)
        visit_history.append(visit_map)

    # get started exploring -- finish to start, reverse trip
    del prospects
    prospects = PriorityQueue()
    agent_id = -1

    # new_agent = Agent(start, 0, end)
    new_agent = Agent(start, agent.steps, end)
    agent_id += 1
    prospects.put((new_agent.heuristic, agent_id, new_agent))

    winner = 0
    for i in range(0, 400000):
        if prospects.qsize() == 0:
            print('Ran out of agents, nobody got home!')
            break

        current_prospect = prospects.get()
        agent = current_prospect[2]
        new_time = agent.steps + 1  # need to look ahead for most checks
        current_storm = storm_history[new_time]
        # print('Checking Agent', current_prospect[1], 'at location', agent.location, 'and time', agent.steps, '; current guess', agent.heuristic)

        if agent.location == end:
            winner = 1
            break

        # get options
        x = agent.location[0]
        y = agent.location[1]

        # check prior visitation -- helps to avoid weirdly convergent paths
        # still have to pop repeated agents, but this keeps them from spawning the same new agents
        check = visit_history[agent.steps][y][x]
        if not check:
            visit_history[agent.steps][y][x] = 1

            # option 1: wait
            if current_storm[y][x] == 1:  # moving storm may mean can't wait here
                new_agent = Agent((x, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 2: go north (catch initial condition)
            if y > 1 and current_storm[y - 1][x] == 1:  # never want to go north from row 1, regardless
                new_agent = Agent((x, y - 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 3: go south
            if current_storm[y + 1][x] == 1:
                new_agent = Agent((x, y + 1), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 4: go east
            if current_storm[y][x + 1] == 1:
                new_agent = Agent((x + 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

            # option 5: go west
            if current_storm[y][x - 1] == 1:
                new_agent = Agent((x - 1, y), new_time, end)
                agent_id += 1
                prospects.put((new_agent.heuristic, agent_id, new_agent))

        # end agent loop

    # show_map_enhanced(storm_history[agent.steps+1], agent)

    if winner:
        print('Victory (final)! Final step count:', agent.steps)
        print('Spawned', agent_id, 'agents')

    elif prospects.qsize() > 0:
        print('No agent finished! X')
        print('Spawned New Agents:', agent_id)
        print('Next X agents:')
        for i in range(0, min(10, prospects.qsize())):
            current_prospect = prospects.get()
            agent = current_prospect[2]
            print('Location -', agent.location, 'Time -', agent.steps, 'Guess -', agent.heuristic)

    part2_score = agent.steps

    part1 = part1_score
    part2 = part2_score

    return [part1, part2]
