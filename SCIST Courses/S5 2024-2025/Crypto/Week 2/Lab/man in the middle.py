"""

key = hashlib.sha256(long_to_bytes(shared_secret)).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)

"""
