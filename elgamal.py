import numpy as np
import random
from hashlib import sha256
import pickle


class PrivateKey:
    def __init__(self, g, b, p, k):
        self.g = g # gene
        self.b = b
        self.p = p
        self.k = k

    def __eq__(self, other):
        if not isinstance(other, PrivateKey):
            return NotImplemented
        print(self.g == other.g, self.b == other.b, self.p == other.p, self.k == other.k)
        return self.g == other.g and self.b == other.b and self.p == other.p and self.k == other.k

    def show(self):
        print('g={}, b={}, p={}, k={}'.format(self.g, self.b, self.p, self.k))


class PublicKey:
    def __init__(self, g, b, p):
        self.g = g
        self.b = b
        self.p = p

    def __eq__(self, other):
        if not isinstance(other, PublicKey):
            return NotImplemented
        print(self.g == other.g, self.b == other.b, self.p == other.p)
        return self.g == other.g and self.b == other.b and self.p == other.p

    def show(self):
        print('g={}, b={}, p={}'.format(self.g, self.b, self.p))


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
            return int(n), q_set


def miller_rabin(n, k=40):
    # based on https://gist.github.com/bnlucas/5857478
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


def find_generator(n, q_set):
    # based on https://math.stackexchange.com/questions/124408/finding-a-primitive-root-of-a-prime-number
    while True:
        g = random.randrange(2, n - 1)
        res = np.array(list(map(lambda q: pow(g, int((n-1)//q), int(n)) == 1, list(q_set))))
        if np.sum(res) == 0:
            return g


def generate_keys(p=None, q_set=None):
    if p is None and q_set is None:
        p, q_set = construct_prime()
    g = find_generator(p, q_set)
    k = random.randrange(2, p - 1)
    b = pow(g, k, p)
    private_key = PrivateKey(g, b, p, k)
    public_key = PublicKey(g, b, p)
    return private_key, public_key


def get_coprime_integer(p):
    while True:
        x = random.randrange(2, p - 1)
        if np.gcd(x, p - 1) == 1:
            return x


def encode(public_key, message):
    x = get_coprime_integer(public_key.p)
    bx = pow(public_key.b, x, public_key.p)
    b1 = public_key.p + bx
    cryptogram = [pow(public_key.g, x, public_key.p), (message*b1) % public_key.p]
    return cryptogram


def decode(cryptogram, private_key):
    return cryptogram[1]*get_inverse_element(pow(cryptogram[0],
                                                 private_key.k, private_key.p), private_key.p) % private_key.p


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def get_inverse_element(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def generate_signature(private_key, message):
    r = get_coprime_integer(private_key.p)
    y = pow(private_key.g, r, private_key.p)
    hm = int(sha256(message.encode()).hexdigest(), 16)
    s = (hm - private_key.k*y)*get_inverse_element(r, private_key.p-1) % (private_key.p-1)
    return tuple([y, s])


def verify_signature(public_key, message, signature):
    y = signature[0]
    s = signature[1]
    hm = int(sha256(message.encode()).hexdigest(), 16)
    x1 = (pow(public_key.b, y, public_key.p) * pow(y, s, public_key.p)) % public_key.p
    x2 = pow(public_key.g, hm, public_key.p)
    if x1 == x2:
        return True
    else:
        return False


def encode_string(public_key, message, filename):
    cryptograms = []
    for m in message:
        cryptograms.append(encode(public_key, ord(m)))
    pickle.dump(cryptograms, open(filename, 'wb'))


def decode_string(private_key, filename):
    cryptograms = pickle.load(open(filename, 'rb'))
    string = []
    for cryptogram in cryptograms:
        string.append(chr(decode(cryptogram, private_key)))
    message = "".join(string)
    return message
