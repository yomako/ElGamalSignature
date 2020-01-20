import pytest
import numpy as np
from elgamal import (
    miller_rabin,
    construct_prime,
    find_generator,
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
    for _ in range(1):
        g = find_generator(prime, q_set)
        ret = np.sort(np.array(list(map(lambda i: pow(g, i, prime), range(1, prime)))))
        assert np.array_equal(ret, np.arange(1, prime))
