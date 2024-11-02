from pwn import *

context.log_level = "error"

r = remote("140.110.112.212", 5124)

F = [
    lambda x: 3 * (x**2) + x + 3,
    lambda x: 5 * (x**2) + 8,
    lambda x: 4 * (x**3) + 6 * x + 6,
    lambda x: 7 * (x**3) + 5 * (x**2),
    lambda x: x**2 + 4 * x + 3,
]


r.recvuntil(b"----- wave : 1/100 -----")
for _ in range(100):
    r.recvline()
    r.recvuntil(b"function : ")
    f = int(r.recvline().strip())
    r.recvuntil(b"x = ")
    x = int(r.recvline().strip())
    r.sendline(str(F[f](x)).encode())

r.interactive()
