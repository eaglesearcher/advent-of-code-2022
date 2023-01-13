import file_io as fio


class Sprite:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move_left(self):
        self.x = self.x-1

    def move_right(self):
        self.x = self.x+1

    def move_up(self):
        self.y = self.y+1

    def move_down(self):
        self.y = self.y-1

    def get_position(self):
        return self.x, self.y

    def chase(self, head):
        head_x, head_y = head.get_position()
        tail_x, tail_y = self.get_position()

        if head_x == tail_x:
            if head_y - tail_y == 2:
                self.move_up()
            elif head_y - tail_y == -2:
                self.move_down()
        elif head_x - tail_x == 1:
            if head_y - tail_y == 2:
                self.move_right()
                self.move_up()
            if head_y - tail_y == -2:
                self.move_right()
                self.move_down()
        elif head_x - tail_x == -1:
            if head_y - tail_y == 2:
                self.move_left()
                self.move_up()
            if head_y - tail_y == -2:
                self.move_left()
                self.move_down()
        elif head_x - tail_x == 2:
            if head_y == tail_y:
                self.move_right()
            elif head_y - tail_y == 1:
                self.move_right()
                self.move_up()
            elif head_y - tail_y == -1:
                self.move_right()
                self.move_down()
            elif head_y - tail_y == 2:
                self.move_right()
                self.move_up()
            elif head_y - tail_y == -2:
                self.move_right()
                self.move_down()
        elif head_x - tail_x == -2:
            if head_y == tail_y:
                self.move_left()
            elif head_y - tail_y == 1:
                self.move_left()
                self.move_up()
            elif head_y - tail_y == -1:
                self.move_left()
                self.move_down()
            elif head_y - tail_y == 2:
                self.move_left()
                self.move_up()
            elif head_y - tail_y == -2:
                self.move_left()
                self.move_down()

def run():
    file_contents = fio.read_input(9, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    motion = file_contents
    motion_lines = motion.split('\n')
    num_instructions = len(motion_lines)

    tail_history = {(0, 0)}
    num_knots = 10
    knots = [Sprite()]*num_knots
    for i in range(0, num_knots):
        knots[i] = Sprite()

    # for i in range(0, 2):
    for i in range(0, num_instructions):
        # i = 0
        new_instruction = motion_lines[i].split(' ')
        direction = new_instruction[0]
        repeat_move = int(new_instruction[1])

        for j in range(0, repeat_move):
            if direction == 'L':
                knots[0].move_left()
            elif direction == 'R':
                knots[0].move_right()
            elif direction == 'U':
                knots[0].move_up()
            elif direction == 'D':
                knots[0].move_down()

            for k in range(1, num_knots):
                knots[k].chase(knots[k-1])

            new_pos = knots[-1].get_position()
            tail_history.add(new_pos)

        print(knots[0].get_position(), knots[8].get_position(), knots[9].get_position())


    num_tail_positions = len(tail_history)

    part1 = num_tail_positions
    part2 = 0

    return [part1, part2]
