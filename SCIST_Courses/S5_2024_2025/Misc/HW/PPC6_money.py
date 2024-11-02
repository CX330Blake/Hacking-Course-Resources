from pwn import *

context.log_level = "error"

r = remote("140.110.112.212", 2407)

r.recvuntil(b"----- wave 1/100 -----")
for _ in range(100):
    r.recvuntil(b"money : ")
    money = int(r.recvline().decode().strip())
    r.recvuntil(b"interest : ")
    interest = int(r.recvline().decode().strip().removesuffix("%"))
    r.sendline(str(money + money // 100 * interest).encode())

r.interactive()
