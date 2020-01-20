import numpy as np
import random


def construct_prime(size=10):
    while True:
        primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                           37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
        es = np.append(np.random.randint(len(primes), size=size), 0)
        q_set = primes[list(set(es))]
        e_set = list(map(lambda q: np.sum(q_set == q), list(q_set)))
        q_set = np.array(q_set)
        e_set = np.array(e_set)
        n = np.prod(q_set**e_set)+1
        if miller_rabin(n):
            return n


def miller_rabin(n, k=40):
    n = int(n)
    if n <= 1:
        raise ValueError("Prime number must be greater or equal 2")

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
