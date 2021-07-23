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
    k = gen_prime(p)
    t = pow(beta, k, p)
    r = pow(a, k, p)
    t = msg * t
    return r, t


# For decryption (first method)
def decryption(r, t, d, p):
    r = pow(r, d, p) # Modular exponentiation, one nore mod
    r = pow(r, -1, p) # (81 mod 53)*(36 mod 53) mod 53 = (28* 36) mod 53, general step: Not affected by previous step
    pt = int(t * r) % p
    return pt


# For decryption (second method)
def decryption2(r1, r2, t1, t2, d, p):
    r1 = pow(r1, d, p)
    r2 = pow(r2, d, p)
    return int((t1 / r1) % p)*int((t2 / r2) % p) % p


# For decryption (third method)
def decryption3(r1, r2, t1, t2, d, p):
    r1 = pow(r1, d, p)
    r2 = pow(r2, d, p)
    return int((t1 * t2/(r1 * r2))) % p


# For decryption (fourth method)
def decryption4(r1, r2, t1, t2, d, p):
    r1 = pow(r1, d, p)
    r2 = pow(r2, d, p)
    return int((t1 / r1)) * int((t2 / r2))


def eval_component_wise_product(r1, r2, t1, t2):
    return (r1 * r2), (t1 * t2)


# ------- HE ----------------------------
# ------- example 1 ------------------------
# ----input message 1: 12
# ----input message 2: 23
# ----ouput decrypted message: 276
# ------------------------------------------

msg1 = input("Enter message 1.")
msg2 = input("Enter message 2.")
# p: modulo
# p = random.randint(pow(10, 20), pow(10, 50))

p = "FCA682CE8E12CABA26EFCCF7110E526DB078B05EDECBCD1EB4A208F3AE1617AE01F35B91A47E6DF63413C5E12ED0899BCD132ACD50D99151BDC43EE737592E17"
p = int(p, 16)
a = random.randint(2, p)

# d is prime
d = gen_prime(p)  # Private key

beta = pow(a, d, p)
r1, t1 = encryption(int(msg1), p, beta, a)
r2, t2 = encryption(int(msg2), p, beta, a)
r_new, t_new = eval_component_wise_product(r1, r2, t1, t2)
m3 = decryption(r_new, t_new, d, p)
m4 = decryption2(r1, r2, t1, t2, d, p)
m5 = decryption3(r1, r2, t1, t2, d, p)
m6 = decryption3(r1, r2, t1, t2, d, p)
# d_msg2 = ''.join(m2)
print("Original Message=", msg1, msg2)
print("Decrypted Message=", m3, m4, m5, m6)


r3, t3 = encryption(int(msg1)*int(msg2), p, beta, a)
print("Original Message=", int(msg1)*int(msg2))
m3 = decryption(r3, t3, d, p)
print("Decrypted Message=", m3)