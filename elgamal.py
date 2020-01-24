from hashlib import sha256
import pickle

from math_functions import *


class PrivateKey:
    """ Private key - keep in secret """
    def __init__(self, g, b, p, k):
        """
        :param g: generator
        :param b: g^k mod(p)
        :param p: prime number
        :param k: secret number from range 1 < k < p
        """
        self.g = g
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
    """ Public key - spread """
    def __init__(self, g, b, p):
        """
        :param g: generator
        :param b: g^k mod(p)
        :param p: prime number
        """
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


def generate_keys(p=None, q_set=None):
    """
    Generates pair: private and public keys.

    :param p: prime number
    :param q_set: p-1 factorization
    :return:
    private key (PrivateKey):
    public key (PublicKey):
    """

    if p is None and q_set is None:
        p, q_set = construct_prime()
    g = find_generator(p, q_set)
    k = random.randrange(2, p - 1)
    b = pow(g, k, p)
    private_key = PrivateKey(g, b, p, k)
    public_key = PublicKey(g, b, p)
    return private_key, public_key


def encode(public_key, message):
    """
    Encodes message using public key. The cryptogram is a pair of numbers: [g^k mod(p), mb^x mod(p)] where x is
    random number co-prime to p-1.

    :param public_key:
    :param message: number to encode
    :return:
    cryptogram: pair of numbers
    """

    x = get_coprime_integer(public_key.p - 1)
    bx = pow(public_key.b, x, public_key.p)
    b1 = public_key.p + bx
    cryptogram = [pow(public_key.g, x, public_key.p), (message*b1) % public_key.p]
    return cryptogram


def decode(cryptogram, private_key):
    """
    Encodes message using public key. The cryptogram is a pair of numbers: [g^k mod(p), mb^x mod(p)] where x is
    random number co-prime to p-1.

    :param private_key:
    :param cryptogram: pair of numbers to decode
    :return:
    decrypted_message: decrypted number
    """

    decrypted_message = cryptogram[1] * get_inverse_element(pow(cryptogram[0], private_key.k, private_key.p),
                                                            private_key.p) % private_key.p
    return decrypted_message


def generate_signature(private_key, message):
    """
    Generates ElGamal signature - pair of numbers [g^r mod(p), (H(m)-ky)r^(-1) mod(p-1)], where r is random number
    co-prime to p-1, y=g^r mod(p), H is hash function (in this case sha256) and m is integer form of hashing result.

    :param private_key:
    :param message: string with message
    :return:
    signature: ElGamal signature of message
    """

    r = get_coprime_integer(private_key.p - 1)
    y = pow(private_key.g, r, private_key.p)
    hm = int(sha256(message.encode()).hexdigest(), 16)
    s = (hm - private_key.k*y)*get_inverse_element(r, private_key.p-1) % (private_key.p-1)
    signature = tuple([y, s])
    return signature


def verify_signature(public_key, message, signature):
    """
    Verifies ElGamal signature of message. If b^y*y^s mod(p) = H(m): signature is valid.

    :param public_key:
    :param message: string with message
    :param signature: ElGamal signature, pair of numbers
    :return:
    True if signature is valid
    False if not
    """

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
    """
    Encodes string with message. Each character is encoded separately. Result - list of cryptograms is saved in pickle
    with given filename.

    :param public_key:
    :param message: string with message
    :param filename: name of file where results will be stored
    """

    cryptograms = []
    for m in message:
        cryptograms.append(encode(public_key, ord(m)))
    pickle.dump(cryptograms, open(filename, 'wb'))


def decode_string(private_key, filename):
    """
    Decodes list of cryptograms from filename.p pickle.

    :param private_key:
    :param filename: name of file where results are stored
    :return:
    message (string): result of decoding list of cryptograms
    """

    cryptograms = pickle.load(open(filename, 'rb'))
    string = []
    for cryptogram in cryptograms:
        string.append(chr(decode(cryptogram, private_key)))
    message = "".join(string)
    return message
