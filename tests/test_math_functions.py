import pytest
import numpy as np
from math_functions import (
    miller_rabin,
    construct_prime,
    find_generator,
    find_primes,
    get_coprime_integer,
)


@pytest.mark.parametrize(
    'n, expected',
    [
        pytest.param(np.int64(2579694547), True),
        pytest.param(1236457989131, True),
        pytest.param(129238593671, False),
        pytest.param(8, False),
        pytest.param(7, True),
    ],
)
def test_miller_rabin(n, expected):
    assert miller_rabin(n) == expected


def test_construct_prime():
    prime, _ = construct_prime()
    assert miller_rabin(prime) is True


@pytest.mark.parametrize(
    'prime, q_set',
    [
        pytest.param(np.int64(229), [2, 3, 19]),
        pytest.param(np.int64(37), [2, 3]),
    ],
)
def test_find_generator(prime, q_set):
    prime = int(prime)
    g = find_generator(prime, q_set)
    ret = np.sort(np.array(list(map(lambda i: pow(g, i, prime), range(1, prime)))))
    assert np.array_equal(ret, np.arange(1, prime))


@pytest.mark.parametrize(
    'limit, expected',
    [
        pytest.param(2, [2]),
        pytest.param(100, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                           37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]),
    ],
)
def test_generate_primes(limit, expected):
    assert find_primes(limit) == expected


@pytest.mark.parametrize(
    'limit',
    [
        pytest.param(1.5),
        pytest.param(-1),
    ],
)
def test_generate_primes_value(limit):
    with pytest.raises(ValueError):
        find_primes(limit)


def test_get_coprime_integer():
    assert get_coprime_integer(int(1e100)) > 1
