import math


def primes(n):
    a = [True] * (n + 1)
    for i in range(2, int(math.sqrt(n))):
        exclude = (j for j in range(i * i, n + 1, i) if a[i])
        for j in exclude: a[j] = False
    for i in range(2, len(a)):
        if a[i]: print(i)


primes(100)
