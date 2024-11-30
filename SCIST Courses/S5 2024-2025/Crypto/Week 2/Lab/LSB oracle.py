from pwn import *
from Crypto.Util.number import *

conn = remote("lab.scist.org", 31191)


conn.sendline(b"n")  # no debug mode
conn.recvuntil(b"public key: (")

e = int(conn.recvuntil(b",", drop=True).decode().strip())
n = int(conn.recvuntil(b")\n", drop=True).decode().strip())
c = int(conn.recvline().decode().split(": ")[1].strip())


l, r = 0, n


def decrypt(c):
    conn.sendlineafter(b": ", b"decrypt")
    conn.sendlineafter(b": ", str(c).encode())
    conn.recvuntil(b": ")
    return conn.recvuntil(b"\n")


while r - l > 1:
    c = pow(2, e, n) * c % n
    if b"0\n" == decrypt(c):
        r = (l + r) // 2
    else:
        l = (l + r) // 2
    print(r - l)

print(long_to_bytes(l))


""" CHALLENGE.py

import sys

from Crypto.Util.number import bytes_to_long, getPrime, inverse

from secret import FLAG

DEBUG = False


def decrypt(d: int, n: int):
    m = pow(int(input("> Ciphertext: ")), d, n)
    print(f"plaintext last bit: {m & 1}")
    if DEBUG:
        print(f"[DEBUG] decrypt {m=}")


def read_server():
    with open("./server.py", "r", encoding="utf-8") as file:
        print(file.read())


def main():
    p, q = getPrime(512), getPrime(512)
    n, e = p * q, 0x10001
    d = inverse(e, (p - 1) * (q - 1))
    print(f"public key: {(e, n)}")
    print(f"enc: {pow(bytes_to_long(FLAG.encode()), e, n)}")
    if DEBUG:
        print(f"[DEBUG] {p=}, {q=}, {d=}")

    for _ in range(1024):
        print("> decrypt")
        print("> server.py")
        print("> exit")
        cmd = input("> Command: ")
        if cmd == "exit":
            sys.exit()
        elif cmd == "decrypt":
            decrypt(d, n)
        elif cmd == "server.py":
            read_server()
        else:
            print("Bad hacker")


if __name__ == "__main__":
    try:
        if input("Do you want to open DEBUG mode? [y/n]: ").lower() == "y":
            DEBUG = True
            FLAG = "flag{THE FLAG FOR DEBUG MODE}"

        main()
    except EOFError:
        sys.exit(1)

"""
