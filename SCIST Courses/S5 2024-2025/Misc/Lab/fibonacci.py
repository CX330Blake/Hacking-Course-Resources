from functools import lru_cache


# Use this to optimize the recursive function
@lru_cache(maxsize=None)
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# F[41]
f_41 = fibonacci(41)
print(f"F[41] = {f_41}")
