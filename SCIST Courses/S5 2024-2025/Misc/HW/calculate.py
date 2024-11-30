from pwn import *

r = remote("lab.scist.org", 31010)

r.recvlines(4)

for _ in range(100):
    level = r.recvline().decode().strip()
    if "{" in level:
        print(level)
        break
    res = round(eval(r.recvline().decode().strip().replace("÷", "/")), 1)
    r.sendline(str(res).encode())

r.interactive()
