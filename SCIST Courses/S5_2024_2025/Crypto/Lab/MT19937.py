from mt19937predictor import MT19937Predictor
from pwn import *

predictor = MT19937Predictor()

r = remote("lab.scist.org", 31124)
r.sendline(b"challenge")

for i in range(624):
    r.recvuntil(b"Now state: ")
    data = r.recvline().strip().decode()
    rand_num = int(data)
    predictor.setrandbits(rand_num, 32)
    next_rand = predictor.getrandbits(32)
    print(next_rand)
    payload = str(0 - next_rand - int(data)).encode()
    r.sendline(payload)

r.sendline(str(next_rand).encode())

r.interactive()
