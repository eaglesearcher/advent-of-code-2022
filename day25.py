import file_io as fio



def snafu_to_dec(input_snafu):
    num_digits = len(input_snafu)
    output_dec = 0

    current_power = num_digits - 1
    for digit_i in range(0, num_digits):
        current_digit_txt = input_snafu[digit_i]
        if current_digit_txt == '=':
            current_digit = -2
        elif current_digit_txt == '-':
            current_digit = -1
        else:
            current_digit = int(current_digit_txt)
        output_dec += current_digit * 5**current_power
        current_power -= 1

    return output_dec


def dec_to_snafu(input_dec):

    digits = []
    current_power = 1
    while input_dec != 0:
        rem = input_dec % (5 ** current_power)
        # print(current_power, rem, rem / (5 ** (current_power-1)))
        digits.append(int(rem / (5 ** (current_power-1))))
        input_dec -= rem
        current_power += 1
    digits.append(0)  # add the leading digit in case leading snafu digit carries over

    output_snafu = []
    for digit_i in range(0, len(digits)):
        if digits[digit_i] < 3:
            output_snafu.insert(0, str(digits[digit_i]))
        elif digits[digit_i] == 3:
            output_snafu.insert(0, '=')
            digits[digit_i + 1] += 1
        elif digits[digit_i] == 4:
            output_snafu.insert(0, '-')
            digits[digit_i + 1] += 1
        elif digits[digit_i] == 5:
            output_snafu.insert(0, '0')
            digits[digit_i + 1] += 1
        # print(digits, ''.join(output_snafu))

    if output_snafu[0] == '0':  # trim the leading digit
        output_snafu.pop(0)

    return ''.join(output_snafu)


def run():
    file_contents = fio.read_input(25, 1)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    list_lines = file_contents.split('\n')
    num_numbers = len(list_lines)

    sum = 0
    for line_i in range(0, num_numbers):
        x = snafu_to_dec(list_lines[line_i])
        sum += x
        # print(list_lines[line_i], '>>', x)

    print('sum is', sum)
    x = dec_to_snafu(sum)
    print(x)

    part1score = x

    # x = snafu_to_dec('1121-1110-1=0')
    # print(x, 'should be 314159265')
    # x = dec_to_snafu(314159265)
    # print(x, 'should be 1121-1110-1=0')

    # 2-=2==-===2=022=10   not correct

    part1 = part1score
    part2 = 0

    return [part1, part2]
