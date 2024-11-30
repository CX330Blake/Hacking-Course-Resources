def L(m):
    return (m * 8).to_bytes(8, byteorder="big")


def LEA(chunk: bytes):
    w = [
        int.from_bytes(chunk[i : i + 4], byteorder="big")
        for i in range(0, len(chunk), 4)
    ]
    for i in range(16, 80):
        w.append(left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))
    # initialize hash value for this chunk
    a, b, c, d, e = h0, h1, h2, h3, h4
    for i in range(80):
        if 0 <= i <= 19:
            f, k = (b & c) | (~b & d), 0x5A827999
        elif 20 <= i <= 39:
            f, k = b ^ c ^ d, 0x6ED9EBA1
        elif 40 <= i <= 59:
            f, k = (b & c) | (b & d) | (c & d), 0x8F1BBCDC
        elif 60 <= i <= 79:
            f, k = b ^ c ^ d, 0xCA62C1D6
        a, b, c, d, e = (
            (left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF,
            a,
            left_rotate(b, 30),
            c,
            d,
        )
    # add this chunk's hash to result so far
    h0 = (h0 + a) & 0xFFFFFFFF
    h1 = (h1 + b) & 0xFFFFFFFF
    h2 = (h2 + c) & 0xFFFFFFFF
    h3 = (h3 + d) & 0xFFFFFFFF
    h4 = (h4 + e) & 0xFFFFFFFF
    return [h0, h1, h2, h3, h4]


token = bytes.fromhex(
    "757365723d67756573742661646d696e3d3037884276a0ab1f262e6c90967e6ed7c63901ab30"
)

print(token)

payload, token_signature = token[:-20], token[-20:]

payload += (
    b"\x80" + b"\x00" * 51 + L(68) + b"&admin=1" + b"\x80" + b"\x00" * 47 + L(136)
)

print(len(payload))


""" CHALLENGE.py
    
import hashlib
import os
import sys

from secret import FLAG

secret = os.urandom(50)


def get_token():
    payload = b"user=guest&admin=0"
    signature = hashlib.sha1(secret + payload).digest()
    token = (payload + signature).hex()
    print(f"Token: {token}")


def verify(debug: bool = False):
    token = bytes.fromhex(input("> Token: "))
    payload, token_signature = token[:-20], token[-20:]
    signature = hashlib.sha1(secret + payload).digest()
    if debug:
        print(f"[DEBUG] signature={signature.hex()}")

    if signature != token_signature:
        print("Invalid signature.")
        return

    data = dict(map(lambda x: x.split(b"="), payload.split(b"&")))
    if debug:
        print(f"[DEBUG] {data=}")

    if not debug and data[b"admin"] == b"1":
        print(f"Here is your flag: {FLAG}")
        print("[FLAG] LEA", file=sys.stderr)

    try:
        username = data[b"user"].decode()
    except UnicodeDecodeError:
        username = data[b"user"].hex()

    print(f"Hi {username}")


def read_server():
    with open("./server.py", "r", encoding="utf-8") as file:
        print(file.read())


def main():
    debug: bool = False
    while True:
        print("> get_token")
        print("> verify")
        print("> debug")
        print("> server.py")
        print("> exit")
        cmd = input("> Command: ")
        if cmd == "exit":
            sys.exit()
        elif cmd == "get_token":
            get_token()
        elif cmd == "verify":
            verify(debug=debug)
            sys.exit()
        elif cmd == "debug":
            debug = True
            print(f"[DEBUG] secret={secret.hex()}")
        elif cmd == "server.py":
            read_server()
        else:
            print("Bad hacker")


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        sys.exit(1)
"""
