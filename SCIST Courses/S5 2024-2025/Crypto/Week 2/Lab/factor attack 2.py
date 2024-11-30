from Crypto.Util.number import GCD, inverse, long_to_bytes
import gmpy2
from pwn import info


def pollard(n: int) -> int:
    a, b = 2, 2
    while True:
        a = pow(a, b, n)
        p = GCD(a - 1, n)
        if 1 < p < n:
            return p
        b += 1


def fermat_factorize(n: int) -> tuple[int, int]:
    a = gmpy2.isqrt(n) + 1
    b = a**2 - n
    while not gmpy2.iroot(b, 2)[1]:
        a += 1
        b = a**2 - n
    b = gmpy2.iroot(b, 2)[0]
    return (a + b, a - b)


n = 89440560733164708153845415331446945959245098008966030018929526224499627757561588031620648168516773823431871418356339994635745869093527493722219078655396271734959826773338477957209319942403927521493751796095337134761865520104013849636230344195374484615442639465418351367038754528133862123415585916462336887316272609032894837016897778296130831547243876103719134564487881368375292269727492130954469891687595162077285957074426084146076230091131943856427238665819605762639
flag_enc = 70677748948501844132153830929251677244113768980787500369152141990965232213831862207217721522056164204162823419806165910568220932219900368675591552968178184614121712327013011109514719999717122365733828157304155345657621328222420087192300965297138284125891425367991980443832811085424797902616979150681335481651723930150196824667059658752617939365799090553917136979687242700603979742173293315404232654368071971864852868586639814633504013277004899488199641716300195627399

p = pollard(n)
q1, q2 = fermat_factorize(n // p)
phi = (p - 1) * (q1 - 1) * (q2 - 1)

e = 0x10001
d = inverse(e, phi)
flag = pow(flag_enc, d, n)

# 转换为明文
info(f"FLAG: {long_to_bytes(flag).decode()}")


""" CHALLENGE.py

import gmpy2
from Crypto.Util.number import bytes_to_long, getPrime, isPrime, size
from Crypto.Random.random import randrange

from secret import FLAG


def genkey() -> int:
    while True:
        p = 2
        while size(p) < 512:
            p *= getPrime(randrange(2, 12))
        if isPrime(p + 1):
            return p + 1


def sprkey(p: int) -> tuple[int, int]:
    q1 = p
    for _ in range(100):
        q1 = int(gmpy2.next_prime(q1))
    p2 = int(gmpy2.next_prime(2 * p - q1))
    return q1, p2


def main():
    e = 0x10001
    p, (q1, q2) = genkey(), sprkey(genkey())
    flag_enc = bytes_to_long(FLAG.encode())
    flag_enc = pow(flag_enc, e, p * q1 * q2)
    print(f"n = {p * q1 * q2}")
    print(f"flag = {flag_enc}")


if __name__ == "__main__":
    main()
    
"""
