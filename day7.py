import file_io as fio


class Directory:
    def __init__(self,name,parent):
        self.subdir = []
        self.name = name
        self.size = 0
        self.parent = parent

    def add_subdir(self, new_directory):
        self.subdir.append(new_directory)

    def get_total_size(self):
        num_subdirectories = len(self.subdir)
        total_size = self.size

        if num_subdirectories != 0:
            for i in range(0, num_subdirectories):
                total_size = total_size + self.subdir[i].get_total_size()
        return total_size


def run():
    file_contents = fio.read_input(7, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    terminal = file_contents
    cmd_list = terminal.split('\n')
    num_lines = len(cmd_list)

    root = Directory('root','-')
    flat_list = [root]
    current_level = root
    for i in range(1, num_lines): # always start in root
    # for i in range(1, 10):  # always start in root
        current_line = cmd_list[i]
        command = current_line[0:4]
        # print(command)
        if command == '$ cd':  # move through the FS
            # move through FS
            temp = current_line.split(' ')
            destination = temp[2]
            if destination == '..':
                current_level = current_level.parent
                # print('moving to parent directory')
                continue
            num_subdirectories = len(current_level.subdir)
            no_joy = 0
            for j in range(0, num_subdirectories):
                if current_level.subdir[j].name == destination:
                    current_level = current_level.subdir[j]
                    no_joy = 1
                    # print('moving to - ', destination)
                    break
            if no_joy == 0:
                print('Attempting to move to uninitialized directory -- Abort!')
        elif command == '$ ls': # list files
            continue
            # ignore this command
            # print('just listing files')
        elif command == 'dir ': # found directory as part of ls
            # add a new subdirectory below current level
            temp = current_line.split(' ')
            new_dir = Directory(temp[1],current_level)
            current_level.add_subdir(new_dir)
            flat_list.append(new_dir)
            # print('adding directory - ', new_dir.name)
        else: # only other option is found file as part of ls
            # add file size to existing directory
            temp = current_line.split(' ')
            filesize = int(temp[0])
            current_level.size = current_level.size + filesize
            # print('adding filesize - ', filesize)

    num_dirs = len(flat_list)
    s = [0]*num_dirs
    score = 0
    for i in range(0, num_dirs):
        s[i] = flat_list[i].get_total_size()
        # print(flat_list[i].name, s[i])
        if s[i] <= 100000:
            score = score + s[i]


    disk_size = 70000000
    required_space = 30000000
    drive_usage = root.get_total_size()
    free_space = disk_size - drive_usage
    need_to_free = required_space - free_space
    # print(need_to_free)

    s.sort()

    for i in range(0, num_dirs):
        if s[i] > need_to_free:
            marker = s[i]
            break

    # print(marker)


    part1 = score
    part2 = marker

    return [part1, part2]