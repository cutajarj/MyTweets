import random


def str_space(a, b):
    return f'{a} {b}'


def desc_time(pre):
    return f'{pre} {random.randint(1, 10)}'


print(str_space("Hello", "World"))
print(desc_time("Random number is"))
