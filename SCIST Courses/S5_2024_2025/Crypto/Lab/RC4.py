from pwn import *

context.log_level = "error"

r = remote("lab.scist.org", 31131)

r.sendline(b"n")
r.recvuntil(b"flag:")

# key ^ flag = ciphertext
ciphertext = bytes.fromhex(r.recvline().decode().strip())
# key ^ payload = output
payload = b"A" * len(ciphertext)
r.sendline(b"something")
r.recvuntil(b"> say something:")
r.sendline(payload)
output = bytes.fromhex(r.recvline().decode().strip())
r.close()

key = bytes([b1 ^ b2 for b1, b2 in zip(payload, output)])

flag = bytes([b1 ^ b2 for b1, b2 in zip(key, ciphertext)])
print(flag.decode())
