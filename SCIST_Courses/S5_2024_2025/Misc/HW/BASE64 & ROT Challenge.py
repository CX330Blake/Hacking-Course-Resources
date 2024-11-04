from pwn import *
from base64 import b64decode
from string import ascii_lowercase


def rot(text, shift):
    shifted = ""
    for char in text:
        if char.isalpha():
            # Handle both uppercase and lowercase letters
            if char.islower():
                shifted += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            elif char.isupper():
                shifted += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
        else:
            shifted += char  # Keep non-alphabet characters as they are
    return shifted


r = remote("lab.scist.org", 31014)
r.recvuntil(b"ANS list: ")

ans_str = r.recvline().decode().strip()
ANS_LIST = eval(ans_str)

for _ in range(100):
    r.recvuntil(b"bot: ")
    text = r.recvline().decode().strip()
    for i in range(26):
        try:
            rotated_text = rot(text, i + 1)
            decoded_text = b64decode(rotated_text).decode()
            if decoded_text in ANS_LIST:
                r.sendline(decoded_text.encode())
                break
        except Exception:
            continue
r.interactive()
