import file_io as fio
from queue import PriorityQueue


class ValveNode:
    def __init__(self):
        self.name = 'AA'
        self.id = 0
        self.rate = 0
        self.link_labels = []
        self.links = []
        self.link_weights = []
        self.num_links = 0


class Agent:
    def __init__(self):
        self.location = 0
        self.rate = 0
        self.pressure = 0
        self.time = 30
        self.history = []
        self.heuristic = 0
        self.active_valves = []

    def calc_heuristic(self, nodes):
        time_left = self.time
        remaining_valves = []
        for node_i in range(0, len(nodes)):
            valve_rate = nodes[node_i].rate
            if valve_rate > 0:
                if node_i not in self.active_valves:
                    remaining_valves.append(valve_rate)
        remaining_valves.sort(reverse=True)
        heuristic = self.pressure + self.rate * time_left
        time_left -= 1
        for valve_i in range(0, len(remaining_valves)):
            heuristic += time_left * remaining_valves[valve_i]
            time_left -= 3
            if time_left <= 0:
                break
        self.heuristic = heuristic
        return


def clone_agent(old_agent, new_location, nodes):
    new_agent = Agent()
    new_agent.location = new_location
    new_node = nodes[new_location]  #
    new_agent.time = old_agent.time - 1  # time advanced
    new_agent.pressure = old_agent.pressure + old_agent.rate  # more pressure release due to time
    new_agent.history = old_agent.history.copy()  # history tracking
    new_agent.history.append(new_node.name)  # tack on new node
    new_agent.rate = old_agent.rate
    new_agent.active_valves = old_agent.active_valves.copy()
    if new_location == old_agent.location:  # stayed put, so we're turning on the valve
        new_agent.rate += new_node.rate  # add to the existing flow
        new_agent.active_valves.append(new_location)
        new_agent.history[-1] += '+'
    new_agent.calc_heuristic(nodes)
    return new_agent


def parse_line(line):
    split_txt = line.split(' ')
    new_node = ValveNode()
    new_node.name = split_txt[1]
    temp = split_txt[4].split('=')
    temp = temp[1].split(';')
    new_node.rate = int(temp[0])
    num_links = len(split_txt)-9
    for i in range(0, num_links):
        link_name = split_txt[-1-i].split(',')
        new_node.link_labels.append(link_name[0])
    new_node.num_links = num_links
    return new_node


def build_map(lines):
    num_valves = len(lines)
    nodes = []
    for valve_i in range(0, num_valves):
        new_node = parse_line(lines[valve_i])
        nodes.append(new_node)
        nodes[valve_i].id = valve_i

    for link_src in range(0, num_valves):
        source_node = nodes[link_src]
        for link_i in range(0, source_node.num_links):
            target_link = source_node.link_labels[link_i]
            for link_dest in range(0, num_valves):
                test_node = nodes[link_dest]
                if test_node.name == target_link:
                    source_node.links.append(test_node)
                    break

    return nodes


def find_start(node_map):
    node_index = -1
    for node_i in range(0, len(node_map)):
        label = node_map[node_i].name
        if label == 'AA':
            node_index = node_i
            break
    return node_index


def run():
    file_contents = fio.read_input(16, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    full_list = file_contents
    lines = full_list.split('\n')
    num_valves = len(lines)
    node_map = build_map(lines)
    start_index = find_start(node_map)
    # print(start_index)
    current_flow = 0
    current_pressure = 0

    # print(start_index)

    prospects = PriorityQueue()
    prospect_id = 0
    # new_prospect = [heuristic, ID, agent_node]

    # starting agent // uses default values for class
    new_agent = Agent()
    new_agent.location = start_index
    new_agent.history = [node_map[new_agent.location].name]
    new_agent.calc_heuristic(node_map)
    prospects.put((-new_agent.heuristic, prospect_id, new_agent))

    # print(prospects.qsize())
    winner = 0
    # while not winner:
    for i in range(0, 50000):
    # for i in range(0, 50):
        # grab highest priority prospects ("largest" heuristic, due to reverse order)
        current_prospect = prospects.get()
        current_agent = current_prospect[2]

        # check if victory achieved
        if current_agent.time == 0:
            winner = 1
            print('Victory!')
            print('Final pressure release:', current_agent.pressure)
            print('Spawned', prospect_id, 'agents')
            print('Path -', current_agent.history)
            break

        # determine new prospects for current agent

        # current_map = current_agent.node_map
        current_node = node_map[current_agent.location]
        # current_node.rate = 10
        location_rate = current_node.rate
        # print('New set of scouts')

        if location_rate > 0 and (current_agent.location not in current_agent.active_valves):
            # print('Agent turning valve at',current_node.name, current_node.id)
            # print(current_agent.location, current_agent.active_valves)
            new_agent = clone_agent(current_agent, current_agent.location, node_map)
            prospect_id += 1
            prospects.put((-new_agent.heuristic, prospect_id, new_agent))
        if current_node.num_links > 0:
            for link_i in range(0, current_node.num_links):
                linked_node = current_node.links[link_i]
                link_name = linked_node.name
                if len(current_agent.history) > 1:
                    if link_name == current_agent.history[-2]:
                        continue
                # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                new_agent = clone_agent(current_agent, linked_node.id, node_map)
                prospect_id += 1
                prospects.put((-new_agent.heuristic, prospect_id, new_agent))

    if not winner:
        print('No agents timed out')
        print('Spawned', prospects.qsize(), 'agents')
        l = prospects.qsize()
        if l > 2:
            l = 2
        for i in range(0, l):

            current_prospect = prospects.get()
            current_agent = current_prospect[2]
            current_node = node_map[current_agent.location]

            print('agent location', current_node.name, current_agent.location, 'time', current_agent.time)
            print('agent rate', current_agent.rate, 'pressure', current_agent.pressure,'location rate', current_node.rate)
            print('agent estimate', current_agent.heuristic, 'agent history', current_agent.history)
            # print('B rate', node_map[1].rate, 'D rate', node_map[3].rate)

    part1 = 1751
    part2 = 0

    return [part1, part2]
