def euclidean_algorithm(a, b) -> int:
    if b == 0:
        return a
    return euclidean_algorithm(b, a % b)


while 1:
    N = int(input())
    if N == 0:
        break
    G = 0
    for i in range(1, N):
        for j in range(i + 1, N + 1):
            G += euclidean_algorithm(i, j)
    print(G)
