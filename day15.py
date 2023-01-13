import file_io as fio


class Sensor:
    def __init__(self, position, beacon):
        self.position = position
        self.closest_beacon = beacon
        self.distance = get_distance(self.position, self.closest_beacon)


class MapBounds:
    def __init__(self):
        self.min_x = 100000000
        self.min_y = 100000000
        self.max_x = -100000000
        self.max_y = -100000000
        self.max_distance = 0

    def check_bounds(self, test_sensor):
        if test_sensor.distance > self.max_distance:
            self.max_distance = test_sensor.distance
        if test_sensor.position[0]-test_sensor.distance < self.min_x:
            self.min_x = test_sensor.position[0]-test_sensor.distance
        if test_sensor.position[0]+test_sensor.distance > self.max_x:
            self.max_x = test_sensor.position[0]+test_sensor.distance
        if test_sensor.position[1]-test_sensor.distance < self.min_y:
            self.min_y = test_sensor.position[1]+test_sensor.distance
        if test_sensor.position[1]+test_sensor.distance > self.max_y:
            self.max_y = test_sensor.position[1]+test_sensor.distance
        return


def get_distance(pos1, pos2):
    x0 = pos1[0]
    x1 = pos2[0]
    y0 = pos1[1]
    y1 = pos2[1]
    return abs(x1-x0)+abs(y1-y0)


def parse_line(line):
    temp = line.split(' ')
    sensor_x_txt = temp[2]
    sensor_x = int(sensor_x_txt[2:-1])
    sensor_y_txt = temp[3]
    sensor_y = int(sensor_y_txt[2:-1])
    beacon_x_txt = temp[8]
    beacon_x = int(beacon_x_txt[2:-1])
    beacon_y_txt = temp[9]
    beacon_y = int(beacon_y_txt[2:len(beacon_y_txt)])

    sensor_position = (sensor_x, sensor_y)
    beacon_position = (beacon_x, beacon_y)
    new_sensor = Sensor(sensor_position, beacon_position)

    return new_sensor


def create_row(xs, y):
    num_pts = abs(xs[1]-xs[0])+1  # inclusive
    row = [(0,0)]*num_pts
    for i in range(0, num_pts):
        row[i] = (xs[0]+i,y)
    return row


def run():
    file_contents = fio.read_input(15, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    sensors = file_contents
    sensor_txt = sensors.split('\n')
    num_sensors = len(sensor_txt)

    new_map = MapBounds()
    sensor_list = [Sensor((0, 0), (0, 0))]*num_sensors
    for i in range(0, num_sensors):
        sensor_list[i] = parse_line(sensor_txt[i])
        new_map.check_bounds(sensor_list[i])

    new_map.min_x = 0
    new_map.min_y = 0
    # new_map.max_x = 20
    # new_map.max_y = 20
    new_map.max_x = 4000000
    new_map.max_y = 4000000

    # # check each row for valid missing spot - X
    # # for test_row in range(0, new_map.max_y+1):
    # # test_row = 11
    # test_row = 2000000
    # found = 0
    # for test_row in range(test_row, test_row+1):
    # # for test_row in range(0, 12):
    # # for test_row in range(0, new_map.max_y+1):
    # #     checked = {0}
    # #     checked.remove(0)
    # #     beacons = {0}
    # #     beacons.remove(0)
    #     checked = []
    #     beacons = []
    #     # if test_row % 100000 == 0:
    #     #     print(int(test_row/100000))
    #     upper_bound = [-1]*num_sensors
    #     lower_bound = [-1]*num_sensors
    #     for sensor_i in range(0, num_sensors):  # loop through all sensors & test distances
    #     # for sensor_i in range(0, 1):  # loop through all sensors & test distances
    #         # print('Test Sensor', sensor_i)
    #         test_sensor = sensor_list[sensor_i]
    #         y_distance = abs(test_sensor.position[1] - test_row)
    #         remaining_distance = test_sensor.distance - y_distance
    #         if remaining_distance > 0:
    #             # print('Sensor',sensor_i,'in range')
    #             upper_bound[sensor_i] = min(test_sensor.position[0]+remaining_distance, new_map.max_x)
    #             lower_bound[sensor_i] = max(test_sensor.position[0]-remaining_distance, new_map.min_x)
    #             # line = set(range(lower_bound, upper_bound+1))
    #             # checked = checked.union(line)
    #             # line = list(range(lower_bound, upper_bound + 1))
    #             # checked = checked+line
    #             # for check_i in range(lower_bound, upper_bound+1):
    #             #     checked(check_i) = 1
    #
    #             # # only need to check beacon if row is within range
    #             # if test_sensor.closest_beacon[1] == test_row:
    #             #     # print('Beacon on row')
    #             #     beacons.append(test_sensor.closest_beacon[0])
    #             #     # beacons.add(test_sensor.closest_beacon[0])
    #
    #     # print(upper_bound)
    #
    #         # checked = list(set(checked))
    #
    #         # if len(checked) == new_map.max_x+1:
    #         #     print('Line cleared')
    #         #     break
    #     # checked = set(checked)
    #
    #     if len(checked) < new_map.max_x + 1:
    #         found = 1
    #         break
    #
    # # beacons = set(beacons)
    # # print(checked)
    # # print(beacons)
    # # print(len(checked) - len(beacons))  # part 1 result
    # # print('Target row = ', test_row)
    # # print(len(checked))  # part 2
    #
    # if found:
    #     full_row = set(range(0,new_map.max_x+1))
    #     # print(full_row)
    #
    #     test = full_row.difference(checked)
    #     # print(test)
    #     # print(len(test))
    #     missing = test.pop()
    #     print('Beacon at x =', missing,', y =', test_row)
    #     result = missing*4000000+test_row
    #     print(result)
    # else:
    #     print('Beacon not found!')

    winner = 0
    num_agents = 4000000
    agent_list = [0]*num_agents
    stable_agents = [0]*num_agents
    stable_count = 0
    # num_agents = len(agent_list)
    # print(num_agents)
    while not winner:
        if stable_count == num_agents:
            # print(sum(stable_agents))
            print('Stability reached.')
            break
        # print(agent_list, stable_agents)
        for agent_i in range(0, num_agents):
            if stable_agents[agent_i]:
                continue
            agent_y = agent_list[agent_i]
            check = 1
            for sensor_i in range(0, num_sensors):
                test_sensor = sensor_list[sensor_i]
                dx = abs(test_sensor.position[0] - agent_i)
                dy = abs(test_sensor.position[1] - agent_y)
                d = dx + dy
                # print('Test Sensor', sensor_i,'Distance:',d,'Max:', test_sensor.distance)
                if d <= test_sensor.distance:
                    check = 0
                    new_y = test_sensor.distance - dx + test_sensor.position[1]+1
                    agent_list[agent_i] = new_y
                    if new_y > new_map.max_y:
                        stable_agents[agent_i] = 1
                        stable_count += 1
                    break
            if check == 1:
                print('Gap found!')
                winner = (agent_i, agent_y)
                break

    print(min(agent_list))

    # print(stable_count)

    if winner:
        print(winner)
    # else:
    # print(agent_list)
        # agent_y = agen

    result = winner[0]*4000000+winner[1]
    # print(result)


    # part 1:
    # 3148307 too low
    # 4793062 correct

    part1 = 4793062
    part2 = result

    return [part1, part2]
