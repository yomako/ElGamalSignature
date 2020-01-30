import numpy as np
import random
import math


def egcd(a, b):
    """
    Extended Euclidean algorithm - recursive version.
    From https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

    :param a: natural number
    :param b: natural number
    :return:
    """

    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def get_inverse_element(a, m):
    """
    Returns inverse of a in multiplicative group Z*_m.

    :param a: natural number
    :param m:
    :return:
    inverse_element (int):
    """

    g, x, y = egcd(a, m)
    inverse_element = x % m
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return inverse_element


def get_coprime_integer(p):
    """
    Returns random number co-prime to p.

    :param p: prime number
    :return:
    x: number co-prime to p
    """

    while True:
        x = random.randrange(2, p - 1)
        if math.gcd(x, p) == 1:
            return x


def find_generator(n, q_set):
    """
    Finds one of generators of multiplicative group Z*_n. Element g is the generator of Z*_n then and only then if g
    is primitive root of n.
    Based on https://math.stackexchange.com/questions/124408/finding-a-primitive-root-of-a-prime-number

    :param n: natural number
    :param q_set: n-1 factorization
    :return:
    g: generator
    """

    while True:
        g = random.randrange(2, n - 1)
        res = list(map(lambda q: pow(g, int((n-1)//q), int(n)) == 1, list(q_set)))
        if sum(res) == 0:
            return g


def construct_prime(size=100, limit=100000):
    """
    Returns prime number p with known p-1 factorization in accordance with the formula:
    p = sum_i(q_i^e_i) + 1
    where q_i is factor (prime number from constructional set), e_i factor degree

    :param size: defines how many prime numbers construct target prime number
    :param limit: maximal prime number from base cannot be greater than limit
    :return:
    p: prime number
    q_set: p-1 factorization
    """

    primes = np.array(find_primes(limit))

    while True:
        es = np.append(np.random.randint(len(primes), size=size), 0)
        q_set = primes[list(set(es))]
        e_set = list(map(lambda qs: np.sum(q_set == qs), list(q_set)))
        q_set = list(map(int, q_set))
        e_set = list(map(int, e_set))
        p = 1
        for ii, q in enumerate(q_set):
            p *= pow(q, e_set[ii])
        p += 1
        if miller_rabin(p):
            return int(p), q_set


def miller_rabin(n, k=40):
    """
    Miller-Rabin algorithm to primality testing. Based on https://gist.github.com/bnlucas/5857478.

    :param n: natural number
    :param k: iterations of algorithm - the bigger k, the higher probability of correctness
    :return:
    True if n is prime
    False if is not
    """

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


def find_primes(limit):
    """
    Finds prime numbers in range from 2 to limit.

    :param limit: maximal prime number from base cannot be greater than limit
    :return:
    primes: prime numbers in range
    """

    if not float(limit).is_integer():
        raise ValueError("Limit must be integer greater or equal 2.")
    if limit <= 1:
        raise ValueError("Limit must be greater or equal 2. Lower numbers cannot be prime.")
    primes = []
    nums = np.arange(2, limit+1)
    base = np.copy(nums)
    while base.size:
        primes.append(base[0])
        base = base[np.remainder(base, base[0]).astype(np.bool)]

    return primes
