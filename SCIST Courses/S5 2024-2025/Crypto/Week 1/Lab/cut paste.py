from urllib.parse import urlencode
from pwn import *

r = remote("lab.scist.org", 31141)

r.sendline(b"register")
r.recvuntil(b"Username:")
r.sendline(b"A" * 4)
r.recvuntil(b"Token:")
first_part = r.recvline().decode().strip()

r.sendline(b"register")
r.recvuntil(b"Username:")
r.sendline(b"A" * 11 + b"Y" + b"O" * ord("O"))
r.recvuntil(b"Token:")
second_part = r.recvline().decode().strip()

chunk = []
final_part = first_part + second_part
print(final_part)

# 32 since 1 byte is 2 hex digits
for i in range(0, len(final_part), 32):
    chunk.append(final_part[i : i + 32])


payload = chunk[0] + chunk[3] + chunk[4] + chunk[5] + chunk[6] + chunk[7]

r.sendline(b"login")
r.recvuntil(b"Token:")
r.sendline(payload.encode())
r.interactive()
