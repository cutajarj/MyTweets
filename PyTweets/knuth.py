import random


numbers = []


def fisher_yates(arr):
    for i in range(len(arr) - 1):
        r = random.randrange(i, len(arr))
        arr[r], arr[i] = arr[i], arr[r]



fisher_yates(numbers)
print(numbers)


