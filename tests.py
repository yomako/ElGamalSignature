import pytest
import numpy as np
from elgamal import (
    miller_rabin,
    construct_prime,
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
    assert miller_rabin(construct_prime()) is True
