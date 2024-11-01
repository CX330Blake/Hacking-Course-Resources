values = [
    int(x)
    for x in "91 322 57 114 40 406 272 147 239 285 353 272 77 110 296 262 299 323 255 337 150 102".split()
]
print(values)

flag = ""

for value in values:
    value = value % 37
    if 0 <= value <= 25:
        flag += chr(ord("A") + value)
    elif 26 <= value <= 35:
        flag += str(value - 26)
    else:
        flag += "_"

print(flag)
