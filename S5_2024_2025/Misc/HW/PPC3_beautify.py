from pwn import *

r = remote("140.110.112.212", 2401)

r.interactive()
