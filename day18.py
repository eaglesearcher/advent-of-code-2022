import file_io as fio
import numpy as np


def build_cubes(cubes_lines):
    num_cubes = len(cubes_lines)
    cubes = [(0, 0, 0)] * num_cubes
    min_coords = (1000, 1000, 1000)
    max_coords = (0, 0, 0)

    min_x = 1000
    max_x = 0
    min_y = 1000
    max_y = 0
    min_z = 1000
    max_z = 0

    for cube_i in range(0, num_cubes):
        coords = cubes_lines[cube_i].split(',')
        x = int(coords[0])
        y = int(coords[1])
        z = int(coords[2])
        cubes[cube_i] = (x, y, z)
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
        if z < min_z:
            min_z = z
        elif z > max_z:
            max_z = z
        min_coords = min_x, min_y, min_z
        max_coords = max_x, max_y, max_z

    return cubes, min_coords, max_coords


def check_neighbors(cube, grid):
    x = cube[0]
    y = cube[1]
    z = cube[2]

    neighbors = []
    max_grid = len(grid)

    # self is grid[x][y][z]

    # straight up, ID 0
    if (z + 1) < max_grid and grid[x][y][z+1]:
        neighbors.append(0)

    # straight down, ID 1
    if (z - 1) >= 0 and grid[x][y][z - 1]:
        neighbors.append(1)

    # left side, ID 2
    if (x - 1) >= 0 and grid[x - 1][y][z]:
        neighbors.append(2)

    # right side, ID 3
    if (x + 1) < max_grid and grid[x + 1][y][z]:
        neighbors.append(3)

    # front side, ID 4
    if (y - 1) >= 0 and grid[x][y - 1][z]:
        neighbors.append(4)

    # back side, ID 5
    if (y + 1) < max_grid and grid[x][y + 1][z]:
        neighbors.append(5)

    return neighbors


def check_not_neighbors(cube, grid):
    x = cube[0]
    y = cube[1]
    z = cube[2]

    open_face = []
    max_grid = len(grid)

    # self is grid[x][y][z]

    # straight up, ID 0
    if (z + 1) >= max_grid:
        open_face.append(0)
    elif not grid[x][y][z+1]:
        open_face.append(0)

    # straight down, ID 1
    if (z - 1) < 0:
        open_face.append(1)
    elif not grid[x][y][z - 1]:
        open_face.append(1)

    # left side, ID 2
    if (x - 1) < 0:
        open_face.append(2)
    elif not grid[x - 1][y][z]:
        open_face.append(2)

    # right side, ID 3
    if (x + 1) >= max_grid:
        open_face.append(3)
    elif not grid[x + 1][y][z]:
        open_face.append(3)

    # front side, ID 4
    if (y - 1) < 0:
        open_face.append(4)
    elif not grid[x][y - 1][z]:
        open_face.append(4)

    # back side, ID 5
    if (y + 1) >= max_grid:
        open_face.append(5)
    elif not grid[x][y + 1][z]:
        open_face.append(5)

    return open_face


def check_exterior(cube, grid):
    x = cube[0]
    y = cube[1]
    z = cube[2]

    open_face = []
    max_grid = len(grid)

    # self is grid[x][y][z]

    # straight up, ID 0
    if (z + 1) >= max_grid:
        open_face.append(0)
    elif not grid[x][y][z+1] and is_exterior((x, y, z + 1), grid, set()):
        open_face.append(0)

    # straight down, ID 1
    if (z - 1) < 0:
        open_face.append(1)
    elif not grid[x][y][z - 1] and is_exterior((x, y, z - 1), grid, set()):
        open_face.append(1)

    # left side, ID 2
    if (x - 1) < 0:
        open_face.append(2)
    elif not grid[x - 1][y][z] and is_exterior((x - 1, y, z), grid, set()):
        open_face.append(2)

    # right side, ID 3
    if (x + 1) >= max_grid:
        open_face.append(3)
    elif not grid[x + 1][y][z] and is_exterior((x + 1, y, z), grid, set()):
        open_face.append(3)

    # front side, ID 4
    if (y - 1) < 0:
        open_face.append(4)
    elif not grid[x][y - 1][z] and is_exterior((x, y - 1, z), grid, set()):
        open_face.append(4)

    # back side, ID 5
    if (y + 1) >= max_grid:
        open_face.append(5)
    elif not grid[x][y + 1][z] and is_exterior((x, y + 1, z), grid, set()):
        open_face.append(5)

    return open_face


def is_exterior(cube, grid, checked):
    # checked.add(cube)  # add self to checked list, so it isn't checked again in recursion
    max_grid = len(grid)
    x = cube[0]
    y = cube[1]
    z = cube[2]

    # print('self cube', cube)
    if x <= 0 or x >= max_grid or y <= 0 or y >= max_grid or z <= 0 or z >= max_grid:
        # checked.add(cube)  # add self, so it isn't checked again... though this shouldn't happen
        return 1

    open_faces = check_not_neighbors(cube, grid)
    count = len(open_faces)
    if count == 0: # fully enclosed air bubble
        # checked.add(cube) # fully enclosed bubble should never be checked recursively
        return 0
    else:
        checked.add(cube) # add self to checked list, so it isn't checked again in recursion
        for face_i in open_faces:
            new_cube = get_neighbor(cube, face_i)
            if new_cube not in checked:
                if is_exterior(new_cube, grid, checked):
                    return 1
    return 0


def get_neighbor(cube, face_id):
    x = cube[0]
    y = cube[1]
    z = cube[2]

    # straight up, ID 0
    if face_id == 0:
        return x, y, z + 1
    # straight down, ID 1
    elif face_id == 1:
        return x, y, z - 1
    # left side, ID 2
    elif face_id == 2:
        return x - 1, y, z
    # right side, ID 3
    elif face_id == 3:
        return x + 1, y, z
    # front side, ID 4
    elif face_id == 4:
        return x, y - 1, z
    # back side, ID 5
    elif face_id == 5:
        return x, y + 1, z


def run():
    file_contents = fio.read_input(18, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    cubes_txt = file_contents

    cubes_lines = cubes_txt.split('\n')
    num_cubes = len(cubes_lines)
    cubes, min_coords, max_coords = build_cubes(cubes_lines)
    # print('min', min_coords)
    # print('max', max_coords)

    max_grid = 20
    grid = np.zeros((max_grid,max_grid,max_grid),dtype=int)
    for cube_i in range(0, num_cubes):
        grid[cubes[cube_i][0]][cubes[cube_i][1]][cubes[cube_i][2]] = 1

    surface_area = 0
    for cube_i in range(0, num_cubes):
        test_cube = cubes[cube_i]
        # open_faces = check_not_neighbors(test_cube, grid)
        open_faces = check_exterior(test_cube, grid)
        count = len(open_faces)
        # print(count)
        surface_area += count

    print(surface_area)

    # open_faces = check_exterior((2,3,2), grid)
    # print(open_faces)

    # x = is_exterior((2,3,3), grid, {(2,3,2)})
    # x = is_exterior((2, 2, 5), grid, set())

    # print(grid[3])
    # print("is exterior", x)

    part1 = 3610
    part2 = 2082

    return [part1, part2]
