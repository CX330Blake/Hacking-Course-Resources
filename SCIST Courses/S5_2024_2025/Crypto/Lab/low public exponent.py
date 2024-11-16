from Crypto.Util.number import long_to_bytes
import gmpy2
from pwn import *

r = remote("lab.scist.org", 31171)

r.recvuntil(b"# n = ")
n = int(r.recvline().strip())

r.recvuntil(b"# c = ")
c = int(r.recvline().strip())

e = 0x03

k = 0
while True:
    m, is_root = gmpy2.iroot(k * n + c, e)
    if is_root:
        break
    else:
        k += 1

print(long_to_bytes(m).decode())
