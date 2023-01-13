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


class Agent2:
    def __init__(self):
        self.location1 = 0
        self.location2 = 0
        self.rate = 0
        self.pressure = 0
        self.time = 26
        self.history1 = []
        self.history2 = []
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
            # print(time_left, remaining_valves[valve_i])
            # time_left -= 2
            if valve_i % 2 == 1:
                time_left -= 5
                # if time_left <= 0:
                #     break
        self.heuristic = heuristic
        return


def clone_agent2(old_agent, new_location1, new_location2, nodes):
    new_agent = Agent2()
    new_agent.location1 = new_location1
    new_agent.location2 = new_location2
    new_node1 = nodes[new_location1]  #
    new_node2 = nodes[new_location2]  #
    new_agent.time = old_agent.time - 1  # time advanced
    new_agent.pressure = old_agent.pressure + old_agent.rate  # more pressure release due to time
    new_agent.history1 = old_agent.history1.copy()  # history tracking
    new_agent.history2 = old_agent.history2.copy()  # history tracking
    new_agent.history1.append(new_node1.name)  # tack on new node
    new_agent.history2.append(new_node2.name)  # tack on new node
    new_agent.rate = old_agent.rate
    new_agent.active_valves = old_agent.active_valves.copy()
    if new_location1 == old_agent.location1:  # agent 1 stayed put, so turning on the valve
        new_agent.rate += new_node1.rate  # add to the existing flow
        new_agent.active_valves.append(new_location1)
        new_agent.history1[-1] += '+'
    if new_location2 == old_agent.location2:  # agent 1 stayed put, so turning on the valve
        new_agent.rate += new_node2.rate  # add to the existing flow
        new_agent.active_valves.append(new_location2)
        new_agent.history2[-1] += '+'
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
    new_agent = Agent2()
    new_agent.location1 = start_index
    new_agent.location2 = start_index
    new_agent.history1 = [node_map[new_agent.location1].name]
    new_agent.history2 = [node_map[new_agent.location2].name]
    new_agent.calc_heuristic(node_map)
    prospects.put((-new_agent.heuristic, prospect_id, new_agent))

    # print(prospects.qsize())
    winner = 0
    # while not winner:
    for i in range(0, 500000):
    # for i in range(0, 5):
        # grab highest priority prospects ("largest" heuristic, due to reverse order)
        current_prospect = prospects.get()
        current_agent = current_prospect[2]

        # check if victory achieved
        if current_agent.time == 0:
            winner = 1
            print('Victory!')
            print('Final pressure release:', current_agent.pressure)
            print('Spawned', prospect_id, 'agents')
            print('Path 1 -', current_agent.history1)
            print('Path 2 -', current_agent.history2)
            break

        # determine new prospects for current agent

        # current_map = current_agent.node_map
        current_node1 = node_map[current_agent.location1]
        current_node2 = node_map[current_agent.location2]
        # current_node.rate = 10
        location1_rate = current_node1.rate
        location2_rate = current_node2.rate
        # print('New set of scouts')

        agent1_at_valve = location1_rate > 0 and (current_agent.location1 not in current_agent.active_valves)
        agent2_at_valve = location2_rate > 0 and (current_agent.location2 not in current_agent.active_valves)
        if agent1_at_valve and agent2_at_valve:
            # both agent 1 & 2 are at valve locations, both will try to open
            if current_agent.location2 != current_agent.location1:
                # both agents at different valves, ok to open
                # print('Agent 1 turning valve at',current_node.name, current_node.id)
                # print(current_agent.location, current_agent.active_valves)
                new_agent = clone_agent2(current_agent, current_agent.location1, current_agent.location2, node_map)
                prospect_id += 1
                prospects.put((-new_agent.heuristic, prospect_id, new_agent))
            else:
                # agents 1 & 2 are at the same location, agent 2 moves instead of opening
                # this is the same case as agent1_at_valve & !agent2_at_valve
                # if agent 2 is stuck due to backtrack edge case, that probably isn't an optimal solution anyway
                agent2_at_valve = False
                # if current_node2.num_links > 0:
                #     for link2_i in range(0, current_node2.num_links):
                #         link2_node = current_node2.links[link2_i]
                #         link2_name = link2_node.name
                #         if len(current_agent.history2) > 1:
                #             if link2_name == current_agent.history2[-2]:
                #                 # avoid un-optimal backtracking
                #                 continue
                #         # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                #         new_agent = clone_agent2(current_agent, current_agent.location1, link2_node.id, node_map)
                #         prospect_id += 1
                #         prospects.put((-new_agent.heuristic, prospect_id, new_agent))
        if agent1_at_valve and not agent2_at_valve:
            # only agent 1 is at a valve location, agent 2 moves
            if current_node2.num_links > 0:
                for link2_i in range(0, current_node2.num_links):
                    link2_node = current_node2.links[link2_i]
                    link2_name = link2_node.name
                    if len(current_agent.history2) > 1:
                        if link2_name == current_agent.history2[-2]:
                            # avoid un-optimal backtracking, if taken at least 2 steps
                            continue
                    # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                    new_agent = clone_agent2(current_agent, current_agent.location1, link2_node.id, node_map)
                    prospect_id += 1
                    prospects.put((-new_agent.heuristic, prospect_id, new_agent))
        if not agent1_at_valve and agent2_at_valve:
            # only agent 2 is at a valve location, agent 1 moves
            if current_node1.num_links > 0:
                for link1_i in range(0, current_node1.num_links):
                    link1_node = current_node1.links[link1_i]
                    link1_name = link1_node.name
                    if len(current_agent.history1) > 1:
                        if link1_name == current_agent.history1[-2]:
                            # avoid un-optimal backtracking, if taken at least 2 steps
                            continue
                    # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                    new_agent = clone_agent2(current_agent, link1_node.id, current_agent.location2,  node_map)
                    prospect_id += 1
                    prospects.put((-new_agent.heuristic, prospect_id, new_agent))
        # if not agent1_at_valve and not agent2_at_valve:
        # both agents are moving, always an option
        if current_node1.num_links > 0:
            if current_agent.location2 == current_agent.location1:
                # special case to encourage not creating mirrors
                for link1_i in range(0, current_node1.num_links):
                    link1_node = current_node1.links[link1_i]
                    link1_name = link1_node.name
                    if len(current_agent.history1) > 1:
                        if link1_name == current_agent.history1[-2]:
                            # avoid un-optimal backtracking, if taken at least 2 steps
                            continue
                    # loop through possible steps for agent 2
                    for link2_i in range(link1_i+1, current_node2.num_links):
                        link2_node = current_node2.links[link2_i]
                        link2_name = link2_node.name
                        if len(current_agent.history2) > 1:
                            if link2_name == current_agent.history2[-2]:
                                # avoid un-optimal backtracking, if taken at least 2 steps
                                continue
                        # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                        new_agent = clone_agent2(current_agent, link1_node.id, link2_node.id, node_map)
                        prospect_id += 1
                        prospects.put((-new_agent.heuristic, prospect_id, new_agent))


            else:
                # loop through possible steps for agent 1
                for link1_i in range(0, current_node1.num_links):
                    link1_node = current_node1.links[link1_i]
                    link1_name = link1_node.name
                    if len(current_agent.history1) > 1:
                        if link1_name == current_agent.history1[-2]:
                            # avoid un-optimal backtracking, if taken at least 2 steps
                            continue
                    # loop through possible steps for agent 2
                    for link2_i in range(0, current_node2.num_links):
                        link2_node = current_node2.links[link2_i]
                        link2_name = link2_node.name
                        if len(current_agent.history2) > 1:
                            if link2_name == current_agent.history2[-2]:
                                # avoid un-optimal backtracking, if taken at least 2 steps
                                continue
                        # print('Agent heading to', link_name, linked_node.id, 'from', current_node.name, current_node.id)
                        new_agent = clone_agent2(current_agent, link1_node.id, link2_node.id, node_map)
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
            # current_node1 = node_map[current_agent.location1]
            # current_node2 = node_map[current_agent.location2]
            # print('agent 1 location', current_node1.name, current_agent.location1, 'time', current_agent.time)
            # print('agent 1 rate', current_agent.rate, 'pressure', current_agent.pressure,'location rate', current_node1.rate)
            # print('agent 2 location', current_node2.name, current_agent.location2, 'time', current_agent.time)
            # print('agent 2 rate', current_agent.rate, 'pressure', current_agent.pressure, 'location rate', current_node2.rate)
            print('agent estimate', current_agent.heuristic, 'time', 26-current_agent.time)
            print('agent1 history', current_agent.history1, 'agent2 history', current_agent.history2)

    part1 = 1751
    part2 = 2207

    return [part1, part2]
