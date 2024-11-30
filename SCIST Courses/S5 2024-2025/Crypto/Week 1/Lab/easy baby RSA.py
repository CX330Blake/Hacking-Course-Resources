from pwn import *
from Crypto.Util.number import long_to_bytes

r = remote("lab.scist.org", 31160)


e = 0x10001
r.recvuntil(b"# p =")
p = int(r.recvline().decode().strip())

r.recvuntil(b"# q =")
q = int(r.recvline().decode().strip())

n = p * q

r.recvuntil(b"# c =")
c = int(r.recvline().decode().strip())

phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)

m = pow(c, d, n)
print(long_to_bytes(m))
