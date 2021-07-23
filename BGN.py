from pypbc import *
import hashlib
import random
import math


def KeyGen():
    q_1 = get_random_prime(60)
    q_2 = get_random_prime(60)
    n = q_1 * q_2
    params = Parameters(n = n)
    pairing = Pairing(params)
    k = Element.random(pairing, G2)
    u = Element.random(pairing, G2)
    sk = Element.random(pairing, Zr)
    h = Element(pairing, G2, value=u ** q_2)
    sk = q_1
    return [pairing, params, h, k, sk, n]


def encryption(m, k, h, n):
    t = random.randint(1, n)
    c = k ** int(m) +  h ** t 
    return c


def decryption(params, sk, k, c, n):
    c = c ** sk
    t = k ** sk
    m = 1
    aux = t
    while aux != c:
        aux = aux + t
        m = m + 1
    return m


if __name__ == '__main__':
    [pairing, params, h, k, sk, n] = KeyGen()
    m = input("Enter message.")
    cipher = encryption(m, k, h, n)
    m = decryption(params, sk, k, cipher, n)
    print(m)