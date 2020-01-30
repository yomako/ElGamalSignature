import pytest
import random
from elgamal import (
    get_coprime_integer,
    generate_keys,
    encode,
    decode,
)


@pytest.mark.parametrize(
    'p, q_set',
    [
        pytest.param(229, [2, 3, 19]),
    ],
)
def test_encode(p, q_set):
    for __ in range(100):
        _, public_key = generate_keys(p=p, q_set=q_set)
        x = get_coprime_integer(public_key.p)
        message = random.randint(1, 1000)
        bx = pow(public_key.b, x, public_key.p)
        b1 = public_key.p + bx
        assert (message*b1) % public_key.p == (message*bx) % public_key.p


def test_encode_decode():
    private_key, public_key = generate_keys()
    cryptogram = encode(public_key, ord('m'))
    message = decode(cryptogram, private_key)
    assert message == ord('m')
