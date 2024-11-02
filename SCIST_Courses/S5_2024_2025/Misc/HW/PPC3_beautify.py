from pwn import *

context.log_level = "error"

r = remote("140.110.112.212", 2401)
r.recvuntil(b"----- Now You Turn -----")
r.recvuntil(b"sentence : ")
text = r.recvline().decode().strip()
text = text.replace("-", " ")
text = text.replace("_", " ")
text = text.lower()
r.recvuntil(b"answer : ")
r.sendline(text.encode())
print(text)
r.interactive()
