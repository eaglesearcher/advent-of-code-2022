import file_io as fio
import numpy as np

def run():
    file_contents = fio.read_input(8, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    tree_map = file_contents

    tree_rows = tree_map.split('\n')

    col_height = len(tree_rows)
    row_width = len(tree_rows[0])

    trees = np.zeros((col_height,row_width))
    for i in range(0, col_height):
        for j in range(0, row_width):
            trees[i][j] = tree_rows[i][j]

    # part 1
    visible = np.zeros((col_height, row_width))
    for i in range(0, row_width):
        visible[0][i] = 1
        visible[-1][i] = 1
    for i in range(0, col_height):
        visible[i][0] = 1
        visible[i][-1] = 1

    for i in range(1, col_height-1):
        for j in range(1, row_width-1):
            tree_height = trees[i][j]
            left = trees[i][0:j]
            right = trees[i][j+1:row_width]

            top = [0]*(i)
            bottom = [0] * (col_height-i-1)
            for a in range(0, i):
                top[a] = trees[a][j]
            for a in range(0, col_height-i-1):
                bottom[a] = trees[a+i+1][j]

            left = max(left)
            right = max(right)
            top = max(top)
            bottom = max(bottom)

            lowest_blocker = min(left,right,top,bottom)

            if lowest_blocker < tree_height:
                visible[i][j] = 1

    # print(trees)
    # print(visible)

    visible_sum = sum(sum(visible))

    # part 2
    scenic = np.zeros((col_height, row_width))

    for i in range(1, col_height-1):
        for j in range(1, row_width-1):
            tree_height = trees[i][j]
            left = trees[i][0:j]
            right = trees[i][j+1:row_width]

            top = [0]*(i)
            bottom = [0] * (col_height-i-1)
            for a in range(0, i):
                top[a] = trees[a][j]
            for a in range(0, col_height-i-1):
                bottom[a] = trees[a+i+1][j]

            left = np.flip(left)
            top = np.flip(top)

            score_left = 0
            score_right = 0
            score_up = 0
            score_down = 0

            # print(tree_height)
            # print(left)
            # print(right)
            # print(top)
            # print(bottom)

            for a in range(0, len(left)):
                score_left = score_left + 1
                if left[a] >= tree_height:
                    break
            for a in range(0, len(right)):
                score_right = score_right + 1
                if right[a] >= tree_height:
                    break
            for a in range(0, len(top)):
                score_up = score_up + 1
                if top[a] >= tree_height:
                    break
            for a in range(0, len(bottom)):
                score_down = score_down + 1
                if bottom[a] >= tree_height:
                    break

            # print(score_left)
            # print(score_right)
            # print(score_up)
            # print(score_down)

            score = score_left*score_right*score_up*score_down
            scenic[i][j] = score

    # print(scenic)

    max_counter = [0]*col_height
    for i in range(0, col_height):
        max_counter[i] = max(scenic[i])

    max_scenic = max(max_counter)

    part1 = visible_sum
    part2 = max_scenic

    return [part1, part2]