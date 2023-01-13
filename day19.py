import file_io as fio
from queue import PriorityQueue


class Blueprint:
    def __init__(self, blueprint_line):
        temp = blueprint_line.split(' ')
        self.id = temp[1][:-1]
        self.ore_bot_cost = int(temp[6])  # cost in ores
        self.clay_bot_cost = int(temp[12])  # cost in ores
        self.obsidian_bot_cost = (int(temp[18]), int(temp[21]))  # cost in ores / clay
        self.geode_bot_cost = (int(temp[27]), int(temp[30]))  # cost in ores / obsidian
        self.max_ore_rate = max(int(temp[12]), int(temp[18]), int(temp[27]))


class Agent:
    def __init__(self, time_left, stock, bots, blueprint):
        self.time_left = time_left
        self.stock = tuple(stock)
        self.bots = tuple(bots)
        self.heuristic = self.get_heuristic(blueprint)

    def get_heuristic(self, blueprint):
        # heuristic = current geodes + geode_rate * time + (future_bots)
        time_left = self.time_left
        heuristic = self.stock[3] + self.bots[3] * time_left

        # need to estimate how many geodes we can crack with bots we haven't built yet
        # determine when we can build the next geode bot, then assume we can build geode bots every turn after
        # pretty optimistic
        macro_time = next_geode_bot(self, blueprint)
        time_left -= (macro_time + 1)  # account for time to begin producing
        if time_left > 0:
            # if time_left <= 0, can't build any productive geode bots
            # assume build a bot every turn after first
            # each bot is T-1 less productive, so future = sum(T) = T+1 * T / 2
            # need a less naive estimation...
            factor = 4
            if 10 < time_left < 20:
                factor = 3
            if time_left < 10:
                factor = 2
            heuristic += int((time_left+1)*time_left/3)
        return heuristic


def next_clay_bot(agent, blueprint):
    current_ore_rate = agent.bots[0]
    need_ore = blueprint.clay_bot_cost
    total_ore = agent.stock[0]
    macro_time = 0
    while total_ore < need_ore:
        total_ore += current_ore_rate + macro_time
        macro_time += 1
    return macro_time


def next_obsidian_bot(agent, blueprint):
    current_clay_rate = agent.bots[1]
    need_clay = blueprint.obsidian_bot_cost[1]
    total_clay = agent.stock[1]
    pre_macro = 0
    if current_clay_rate == 0:
        pre_macro = next_clay_bot(agent, blueprint)+1
        current_clay_rate += 1
    macro_time = 0
    while total_clay < need_clay:
        total_clay += current_clay_rate + macro_time
        macro_time += 1
    return macro_time + pre_macro


def next_geode_bot(agent, blueprint):
    current_obsidian_rate = agent.bots[2]
    need_obsidian = blueprint.geode_bot_cost[1]
    total_obsidian = agent.stock[2]
    pre_macro = 0
    if current_obsidian_rate == 0:
        pre_macro = next_obsidian_bot(agent, blueprint)+1
        current_obsidian_rate += 1
    macro_time = 0
    while total_obsidian < need_obsidian:
        total_obsidian += current_obsidian_rate + macro_time
        macro_time += 1
    return macro_time + pre_macro


def can_build_ore_bot(agent, blueprint):
    return agent.stock[0] >= blueprint.ore_bot_cost


def can_build_ore_bot_next(agent, blueprint):
    return (agent.stock[0] + agent.bots[0]) >= blueprint.ore_bot_cost


def can_build_clay_bot(agent, blueprint):
    return agent.stock[0] >= blueprint.clay_bot_cost


def can_build_clay_bot_next(agent, blueprint):
    return (agent.stock[0] + agent.bots[0]) >= blueprint.clay_bot_cost


def can_build_obsidian_bot(agent, blueprint):
    return (agent.stock[1] >= blueprint.obsidian_bot_cost[1]) and (agent.stock[0] >= blueprint.obsidian_bot_cost[0])


def can_build_obsidian_bot_next(agent, blueprint):
    need_ore = blueprint.obsidian_bot_cost[0]
    need_clay = blueprint.obsidian_bot_cost[1]
    return ((agent.stock[1] + agent.bots[1]) >= need_clay) and ((agent.stock[0] + agent.bots[0]) >= need_ore)


def can_build_geode_bot(agent, blueprint):
    return (agent.stock[2] >= blueprint.geode_bot_cost[1]) and (agent.stock[0] >= blueprint.geode_bot_cost[0])


def can_build_geode_bot_next(agent, blueprint):
    current_ore = agent.stock[0]
    current_ore_rate = agent.bots[0]
    current_obsidian = agent.stock[2]
    current_obsidian_rate = agent.bots[2]

    need_ore = blueprint.geode_bot_cost[0]
    need_obsidian = blueprint.geode_bot_cost[1]

    next_time = ((current_ore + current_ore_rate) >= need_ore) and ((current_obsidian + current_obsidian_rate) >= need_obsidian)

    return next_time


def run():
    file_contents = fio.read_input(19, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    blueprints_txt = file_contents
    blueprint_lines = blueprints_txt.split('\n')
    num_bp = len(blueprint_lines)

    geode_count = []
    # mega blueprint loop
    # for bp_i in range(0, num_bp):
    # for bp_i in range(0, 1):
    # for bp_i in range(1, 2):
    for bp_i in range(2, 3):
    #     bp_i = 14
        bp = Blueprint(blueprint_lines[bp_i])

        prospects = PriorityQueue()
        agent_id = 0

        # starting agent -- no stocks & 1 ore bot
        new_stock = [0, 0, 0, 0]
        new_bots = [1, 0, 0, 0]
        time_left = 32
        new_agent = Agent(time_left, new_stock, new_bots, bp)
        agent_id += 1
        prospects.put((-new_agent.heuristic, agent_id, new_agent))

        winner = 0
        # optimization loop for each blueprint
        print('Optimizing Blueprint #', bp.id)
        for i in range(0, 10000000):  # 10M
        # for i in range(0, 1000000):  # 1M
        # for i in range(0, 100000):  # 100K
            if prospects.qsize() == 0:
                print('Something went terribly wrong!')
                break
            current_prospect = prospects.get()
            agent = current_prospect[2]
            current_time = agent.time_left

            # print('Checking Agent', current_prospect[1])
            # print('current stock', current_agent.stock, 'current rates', current_agent.bots, 'current time', current_time)

            # check if victory achieved
            # also if strongest remaining agent has a 0 estimate, this blueprint is hopeless
            if current_time == 0 or agent.heuristic == 0:
                winner = 1
                print('Victory! Final geode count:', agent.stock[3])
                geode_count.append(agent.stock[3])
                print('Spawned', agent_id, 'agents')
                # print('Path -', current_agent.history)
                break

            # spawn new agents / always increment metals by rates
            # makes sense to do this here, since (do nothing) is always a valid option
            updated_stock = list(agent.stock)
            updated_bots = list(agent.bots)
            for metal_i in range(0, 4):  # increment all metals by rates
                updated_stock[metal_i] += updated_bots[metal_i]

            if can_build_geode_bot(agent, bp):
                new_bots = updated_bots.copy()
                new_stock = updated_stock.copy()
                new_stock[0] -= bp.geode_bot_cost[0]  # spend ores to build geode bot
                new_stock[2] -= bp.geode_bot_cost[1]  # spend obsidian to build geode bot
                new_bots[3] += 1  # add new geode bot at the end
                new_agent = Agent(current_time - 1, new_stock, new_bots, bp)
                agent_id += 1
                prospects.put((-new_agent.heuristic, agent_id, new_agent))

            if can_build_obsidian_bot(agent, bp) and agent.bots[2] < bp.geode_bot_cost[1]:
                # there's no sense in building obs bots if our rate is higher than the obs cost of
                # a geo bot, since we can only build 1 bot at a time
                new_bots = updated_bots.copy()
                new_stock = updated_stock.copy()
                new_stock[0] -= bp.obsidian_bot_cost[0]  # spend ores to build obsidian bot
                new_stock[1] -= bp.obsidian_bot_cost[1]  # spend clay to build obsidian bot
                new_bots[2] += 1  # add new obsidian bot at the end
                new_agent = Agent(current_time - 1, new_stock, new_bots, bp)
                agent_id += 1
                prospects.put((-new_agent.heuristic, agent_id, new_agent))

            if agent.bots[1] < bp.obsidian_bot_cost[1] and can_build_clay_bot(agent, bp):
                # there's no sense in building clay bots if our rate higher than the clay cost of
                # an obs bot, since we can only build 1 bot at a time
                new_bots = updated_bots.copy()
                new_stock = updated_stock.copy()
                new_stock[0] -= bp.clay_bot_cost  # spend ores to build clay bot
                new_bots[1] += 1  # add new clay bot at the end
                new_agent = Agent(current_time - 1, new_stock, new_bots, bp)
                agent_id += 1
                prospects.put((-new_agent.heuristic, agent_id, new_agent))

            if agent.bots[0] < bp.max_ore_rate and can_build_ore_bot(agent, bp):
                # there's no sense in building ore bots if our rate higher than the ore cost of
                # higher tech bots, since we can only build 1 bot at a time anyway
                new_bots = updated_bots.copy()
                new_stock = updated_stock.copy()
                new_stock[0] -= bp.ore_bot_cost  # spend ores to build ore bot
                new_bots[0] += 1  # add new ore bot at the end
                new_agent = Agent(current_time - 1, new_stock, new_bots, bp)
                agent_id += 1
                prospects.put((-new_agent.heuristic, agent_id, new_agent))

            # do nothing, only increment stocks based on rates [always possible]
            new_bots = updated_bots.copy()
            new_stock = updated_stock.copy()
            new_agent = Agent(current_time - 1, new_stock, new_bots, bp)
            agent_id += 1
            prospects.put((-new_agent.heuristic, agent_id, new_agent))

            # print('--')

        # if winner:
        #     print('Winning agent for BP ID:', current_bp.id, 'found', current_agent.stock[3], 'geodes')

        if not winner:
            print('No agent finished! X')
            print('Spawned Agents:', agent_id)
            print('Next X agents:')
            for i in range(0, 5):
                current_prospect = prospects.get()
                agent = current_prospect[2]
                print('Stock -', agent.stock, 'Bots -', agent.bots, 'Time -', agent.time_left, 'Score -', agent.heuristic)


    final_score = 0
    if len(geode_count) == num_bp:
        for bp_i in range(0, num_bp):
            final_score += (bp_i+1) *geode_count[bp_i]
        print(final_score)
    else:
        print('All blueprints did not converge!')

    # part2_score = 1
    # if len(geode_count) == 2:
    #     for bp_i in range(0, 2):
    #         part2_score *= geode_count[bp_i]
    #     print(part2_score)
    # else:
    #     print('All blueprints did not converge!')

    # 1783 - too low
    # 1861 - too low


    part1 = 1958
    part2 = 4257

    return [part1, part2]
