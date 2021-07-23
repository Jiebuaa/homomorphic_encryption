import random


# To find greatest common divisor of two numbers
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# For key generation i.e. large random number
def gen_prime(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key


# For asymmetric encryption
def encryption(msg, p, beta, a):
    r = []
    k = gen_prime(p)
    s = pow(beta, k, p)
    t = pow(a, k, p)
    for i in range(0, len(msg)):
        r.append(msg[i])
    for i in range(0, len(r)):
        r[i] = s * ord(r[i])
    return r, t


# For decryption
def decryption(ct, p, key, q):
    pt = []
    h = pow(p, key, q)
    for i in range(0, len(ct)):
        pt.append(chr(int(ct[i]/h)))
    return pt



# ------- example 1 ------------------------
# ----input message: 'ab'
# ----ouput decrypted message: 'ab'
# ------------------------------------------

# ------- example 2 ------------------------
# ----input message: '12'
# ----ouput decrypted message: '12'
# ------------------------------------------


msg = input("Enter message.")

p = random.randint(pow(10, 20), pow(10, 50))   # p: modulo
a = random.randint(2, p)

# d is prime
d = gen_prime(p)  # Private key

beta = pow(a, d, p)
r, t = encryption(msg, p, beta, a)
print("Original Message =", msg)
print("Encrypted Message r =", r)
print("Encrypted Message t =", t)
m = decryption(r, t, d, p)
d_msg = ''.join(m)
print("Decrypted Message=", d_msg)