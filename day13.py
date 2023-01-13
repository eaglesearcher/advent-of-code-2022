import file_io as fio


def get_packet(packet_input):
    packet_length = len(packet_input)
    new_packet = []
    i = 1
    item = ''
    while i != packet_length:
        new_char = packet_input[i]
        # print('i = ',i, ', char1 =', new_char)
        if new_char == '[':
            sub_packet_input = packet_input[i:packet_length]
            # print('going down a level')
            sub_packet, sub_len = get_packet(sub_packet_input)
            new_packet.append(sub_packet)
            # print('sub len',sub_len)
            i = i + sub_len
        elif new_char == ']':
            packet_length = i
            if item:
                # print('end of packet - adding last item', item)
                new_packet.append(int(item))
            # print('end of packet - going up a level')
            break
        elif new_char == ',':
            if item:
                # print('end of item - adding last item', item)
                new_packet.append(int(item))
                item = ''
        else:
            item = item+new_char
            # print('new char read, add to item -', item)
        i = i + 1
    return new_packet, packet_length


def compare_packets(packet1, packet2):
    p1_length = len(packet1)
    p2_length = len(packet2)

    for i in range(0, p1_length):
        item1 = packet1[i]
        if i >= p2_length:
            # print('Right side ran out of items - incorrect')
            return 0
        item2 = packet2[i]
        if isinstance(item1, int) and isinstance(item2, int):
            if item2 < item1:
                # print('Right side item is lower in value - incorrect')
                return 0
            if item2 > item1:
                # print('Left side item is lower in value - correct')
                return 1
        else:
            # print('Checking sub-packet')
            if isinstance(item1, int):
                item1 = [item1]
            if isinstance(item2, int):
                item2 = [item2]
            # print(item1)
            # print(item2)
            test = compare_packets(item1, item2)
            if test == 0:
                return 0
            if test == 1:
                return 1
    if p2_length > p1_length:
        # print('Left side out of items - correct')
        return 1
    else:
        return -1


def packet_sort(packets):
    # print(packets, ' list')
    num_packets = len(packets)
    if num_packets == 0 or num_packets == 1:
        # print(packets, 'sorted')
        return packets
    pivot = int(num_packets/2)-1
    lower_bucket = []
    upper_bucket = []
    sorted_bucket = []
    # print(packets[pivot], ' pivot')
    for i in range(0, num_packets):
        if i != pivot:
            test = compare_packets(packets[i], packets[pivot])
            if test:
                lower_bucket.append(packets[i])
            else:
                upper_bucket.append(packets[i])
    # print(lower_bucket, ' lower bucket')
    # print(upper_bucket, ' upper bucket')
    if lower_bucket:
        lb = packet_sort(lower_bucket)
        for j in range(0, len(lb)):
            sorted_bucket.append(lb[j])
    sorted_bucket.append(packets[pivot])
    if upper_bucket:
        ub = packet_sort(upper_bucket)
        for j in range(0, len(ub)):
            sorted_bucket.append(ub[j])

    # print(sorted_bucket, 'sorted')
    return sorted_bucket


def run():
    file_contents = fio.read_input(13, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    all_packets = file_contents
    packet_pairs = all_packets.split('\n\n')

    num_pairs = len(packet_pairs)

    packets = []

    score = [0]*num_pairs
    for i in range(0, num_pairs):
        pair = packet_pairs[i].split('\n')
        packet1 = pair[0]
        packet2 = pair[1]

        packet1_built, p1_length = get_packet(packet1)
        packet2_built, p2_length = get_packet(packet2)

        packet1 = packet1_built
        packet2 = packet2_built

        score[i] = compare_packets(packet1, packet2)*(i+1)

        packets.append(packet1)
        packets.append(packet2)

    # print('len = ', len(packets), packets)

    packets.append([[2]])
    packets.append([[6]])

    # print('len = ', len(packets), packets)

    new_packets = packet_sort(packets)

    # print('len = ', len(new_packets), new_packets)

    index1 = new_packets.index([[2]]) + 1
    index2 = new_packets.index([[6]]) + 1
    # print(index1, index2, index1*index2)

    # print(score, ' sum = ', sum(score))
    # print(score)

    # ID = 0
    # packets = []*num_pairs*2
    # for i in range(0, num_pairs):

    part1 = sum(score)
    part2 = index1*index2

    return [part1, part2]
