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


def add(c1, c2, h, n):
    t = random.randint(1, n)
    return c1 + c2 + h**t


def mul(c1, c2, h, n, pairing):
    u = random.randint(1, n)
    c = pairing.apply(c1, c2)
    c = c * pairing.apply(h, h) ** u
    return c


def decryption(params, sk, k, c):
    c = c ** sk
    t = k ** sk
    m = 1
    aux = t
    while aux != c:
        aux = aux + t
        m = m + 1
    return m


def decryptionm(params, sk, k, c, pairing):
    c = c ** sk
    k = pairing.apply(k, k)
    t = k ** sk
    m = 1
    aux = t
    while aux != c:
        aux = aux + t
        m = m + 1
    return m


if __name__ == '__main__':
    [pairing, params, h, k, sk, n] = KeyGen()
    m1 = input("Enter message.")
    m2 = input("Enter message.")
    cipher1 = encryption(m1, k, h, n)
    cipher2 = encryption(m2, k, h, n)
    ciphera = add(cipher1, cipher2, h, n)
    ciphera = add(ciphera, cipher2, h, n)
    cipherm = mul(cipher1, cipher2, h, n, pairing)
    m1 = decryption(params, sk, k, ciphera)
    print(m1)
    m2 = decryptionm(params, sk, k, cipherm, pairing)
    print(m2)