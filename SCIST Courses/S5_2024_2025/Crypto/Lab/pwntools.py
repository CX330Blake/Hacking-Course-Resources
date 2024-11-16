from base64 import b64encode, b32decode
from pwn import *

r = remote("lab.scist.org", 31100)
r.sendline(b"challenge")

for _ in range(100):
    r.recvuntil(b"100:")
    data = b32decode(r.recvline().decode().strip())
    r.sendline(b64encode(data))

r.interactive()
