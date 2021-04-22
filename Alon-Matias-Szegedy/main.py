import random

count_vars500 = 500
count_vars100 = 100

elements_map = {}

vars500 = []
vars100 = []


class Node:
    def __init__(self, index):
        self.index = index
        self.element = -1
        self.value = 0


def create_vars():
    for i in range(count_vars500):
        random_index = random.randint(1, 1000000)
        vars500.append(Node(random_index))

    for i in range(count_vars100):
        random_index = random.randint(1, 1000000)
        vars100.append(Node(random_index))


def start_stream():
    for i in range(1000000):
        random_int = random.randint(1, 1000)
        if elements_map.get(random_int) is None:
            elements_map[random_int] = 1
        else:
            elements_map[random_int] += 1

        for var in vars500:
            if var.index == i:
                var.element = random_int
                var.value = 1
            elif var.index < i:
                if var.element == random_int:
                    var.value += 1

        for var in vars100:
            if var.index == i:
                var.element = random_int
                var.value = 1
            else:
                if var.index < i:
                    if var.element == random_int:
                        var.value += 1


def count_simple_moments():
    map_len = len(elements_map)
    first_moment = 0
    second_moment = 0
    for var in elements_map:
        first_moment += elements_map[var]
        second_moment += elements_map[var] * elements_map[var]

    print("[zero_moment:] --- " + str(map_len))
    print("[first_moment:] --- " + str(first_moment))
    print("[second_moment simple:] --- " + str(second_moment))


def count_second_moment_on_AMS():
    sum500 = 0
    for var in vars500:
        current = var.value * 2 - 1
        sum500 += current
    print("[AMS for 500 vars:] --- " + str(sum500 * 1000000 / 500))

    sum100 = 0
    for var in vars100:
        current = var.value * 2 - 1
        sum100 += current
    print("[AMS for 100 vars:] --- " + str(sum100 * 1000000 / 100))


if __name__ == '__main__':
    create_vars()
    start_stream()
    count_simple_moments()
    print("-------------------")
    count_second_moment_on_AMS()
