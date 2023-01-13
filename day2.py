import file_io as fio


class Rock:  # A, X
    score = 1
    beats = "C"
    loses = "B"
    ties = "A"


class Paper:  # B, Y
    score = 2
    beats = "A"
    loses = "C"
    ties = "B"


class Scissors:  # C, Z
    score = 3
    beats = "B"
    loses = "A"
    ties = "C"


class Result:
    lose = 0
    draw = 3
    win = 6


def run():

    file_contents = fio.read_input(2, 0)  # 0 = test, 1 = input
    if not file_contents:
        return [0, 0]

    strategy_guide = file_contents
    rounds = strategy_guide.split("\n")
    num_rounds = len(rounds)

    total_score = 0
    for i in range(0, num_rounds):  # part 1 -- 2nd character = throw
        fight = rounds[i].split(" ")

        throw = Rock()
        score = 0
        if fight[1] == "X":
            throw = Rock()
        elif fight[1] == "Y":
            throw = Paper()
        elif fight[1] == "Z":
            throw = Scissors()

        score = score + throw.score

        if fight[0] == throw.loses:
            score = score + Result.lose
        elif fight[0] == throw.ties:
            score = score + Result.draw
        elif fight[0] == throw.beats:
            score = score + Result.win

        total_score = total_score + score

    total_score2 = 0
    for i in range(0, num_rounds):  # part 2 -- 2nd character = win condition
        fight = rounds[i].split(" ")

        elf_throw = Rock()
        score = 0
        if fight[0] == "A":
            elf_throw = Rock()
        elif fight[0] == "B":
            elf_throw = Paper()
        elif fight[0] == "C":
            elf_throw = Scissors()

        throw = "A"
        if fight[1] == "X":
            score = Result.lose
            throw = elf_throw.beats
        elif fight[1] == "Y":
            score = Result.draw
            throw = elf_throw.ties
        elif fight[1] == "Z":
            score = Result.win
            throw = elf_throw.loses

        if throw == "A":
            throw = Rock()
        elif throw == "B":
            throw = Paper()
        elif throw == "C":
            throw = Scissors()

        score = score + throw.score

        total_score2 = total_score2 + score

    part1 = total_score
    part2 = total_score2

    return [part1, part2]
