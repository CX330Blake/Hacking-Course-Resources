#!/usr/bin/env python3
from pwn import *
from fractions import Fraction

context.log_level = "error"

r = remote("127.0.0.1", 20000)

r.recvlines(5)

for _ in range(100):
    r.recvuntil("Fahrenheit : ")
    F = Fraction(int(r.recvline().strip()), 1)
    C = (F - 32) * 5 / 9
    r.sendline(str(C.numerator) + "/" + str(C.denominator))

r.interactive()
