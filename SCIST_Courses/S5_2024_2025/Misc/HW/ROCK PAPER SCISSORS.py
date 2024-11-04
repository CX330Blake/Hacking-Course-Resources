rock = """
    _______
---'   ____)
        (_____)
        (_____)
        (____)
---.__(___)
"""

paper = """
     _______
---'    ____)____
            ______)
            _______)
            _______)
---.__________)
"""

scissors = """
    _______
---'   ____)____
            ______)
        __________)
        (____)
---.__(___)
"""

from pwn import *

r = remote("lab.scist.org", 31011)

for _ in range(100):
    r.recvuntil(b"bot >")
    bot = r.recvuntil(b"=====================").decode()
    if "rock" in bot:
        r.sendline(b"1")
    elif "paper" in bot:
        r.sendline(b"2")
    else:
        r.sendline(b"3")

r.interactive()
