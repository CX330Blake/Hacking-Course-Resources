from pwn import *

context.log_level = "error"

r = remote("140.110.112.212", 2403)

for i in range(1, 101):
    r.sendline(str(i).encode())

r.interactive()
