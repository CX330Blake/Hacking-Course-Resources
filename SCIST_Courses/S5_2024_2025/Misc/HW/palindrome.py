num = int(input())

i = 1
while len(str(i)) <= num:
    binary = str(bin(i))[2:]
    decimal = str(i)
    if binary == binary[::-1] and decimal == decimal[::-1]:
        print(i)
    i += 1
