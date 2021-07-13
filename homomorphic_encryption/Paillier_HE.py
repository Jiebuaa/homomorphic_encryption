import gmpy2
import random
import time


def get_prime(rs):
    p = gmpy2.mpz_urandomb(rs, 516)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p


def L(x, n): # compared with int((x-1)/n), gmpy2.div gains more precise results
    return gmpy2.div(x-1, n)


def keygen():
    while True:
        rs = gmpy2.random_state(int(time.time()))
        p = get_prime(rs)
        q = get_prime(rs)
        n = p * q
        lmd = (p - 1) * (q - 1)
        # originally, lmd(lambda) is the least common multiple.
        # However, if using p,q of equivalent length, then lmd = (p-1)*(q-1)
        if gmpy2.gcd(n, lmd) == 1:
            # This property is assured if both primes are of equal length
            break
    g = n + 1
    pk = [n, g]
    mu = gmpy2.invert(L(gmpy2.powmod(g, lmd, n ** 2),n ), n)  # first method
    # mu = gmpy2.invert(lmd, n)  # second method
    sk = [lmd, mu]
    return pk, sk


def encipher(plaintext, pk):
    n, g = pk
    r = random.randint(1, n ** 2)
    while gmpy2.gcd(n, r) != 1:
        r += 1
    c = gmpy2.powmod(g, int(plaintext), n ** 2) * gmpy2.powmod(r, n, n ** 2) % (n ** 2)
    return c


def decipher(c, pk, sk):
    [n, g] = pk
    [lmd, mu] = sk
    m = L(gmpy2.powmod(c, lmd, n ** 2), n) * mu % n
    return m


def eval_component_wise_addition(c1, c2):
    return c1 * c2



if __name__ == '__main__':
    pk, sk = keygen()
    message1 = input('Please input your message 1: ')
    message2 = input('Please input your message 2: ')
    print("Original Message =", message1, message2)
    ciphertext1 = encipher(message1, pk)
    ciphertext2 = encipher(message2, pk)
    ciphertext = eval_component_wise_addition(ciphertext1, ciphertext2)
    print('Encrypted Message =', ciphertext)
    message = decipher(ciphertext, pk, sk)
    print('Decrypted Message=', message)

    ciphertext1 = encipher(int(message1) + int(message2), pk)
    print("Original Message =", int(message1) + int(message2))
    print('Encrypted Message =', ciphertext)
    message = decipher(ciphertext, pk, sk)
    print('Decrypted Message =', message)