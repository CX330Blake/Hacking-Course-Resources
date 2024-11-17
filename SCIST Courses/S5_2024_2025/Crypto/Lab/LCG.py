from math import gcd
from pwn import *


def recover_m(values):
    diffs = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    m = 0
    for i in range(len(diffs) - 2):
        # 计算 m 的候选值
        m_candidate = diffs[i + 2] * diffs[i] - diffs[i + 1] ** 2
        if m_candidate != 0:
            m = gcd(m, abs(m_candidate))
    if m == 0:
        raise Exception("Failed to recover m")
    return m


def recover_a(values, m):
    x0, x1, x2 = values[0], values[1], values[2]
    inv = pow(x1 - x0, -1, m)
    a = (x2 - x1) * inv % m
    return a


def recover_c(values, a, m):
    x0, x1 = values[0], values[1]
    c = (x1 - a * x0) % m
    return c


def verify_parameters(values, a, c, m):
    for i in range(1, len(values)):
        expected = (a * values[i - 1] + c) % m
        if expected != values[i]:
            print(f"Mismatch at index {i}: expected {expected}, got {values[i]}")
            return False
    return True


def predict_next(values):
    m = recover_m(values)
    print(f"Recovered m: {m}")
    a = recover_a(values, m)
    print(f"Recovered a: {a}")
    c = recover_c(values, a, m)
    print(f"Recovered c: {c}")

    # 验证恢复的参数
    if not verify_parameters(values, a, c, m):
        raise Exception("Parameter verification failed.")

    next_value = (a * values[-1] + c) % m
    return next_value


def main():
    # 连接到服务器
    r = remote("lab.scist.org", 31121)

    # 发送挑战请求
    r.sendline(b"challenge")

    # 接收问题
    r.recvuntil(b"Problem: ")
    values_line = r.recvline().decode().strip()
    values = list(map(int, values_line.split(",")))

    print(f"Received values: {values}")

    # 预测下一个值
    try:
        next_val = predict_next(values)
        print(f"Predicted next value: {next_val}")
    except Exception as e:
        print(f"Error: {e}")
        r.close()
        return

    # 发送预测结果
    r.sendline(str(next_val).encode())

    # 查看响应
    response = r.recvline().decode().strip()
    print(f"Response: {response}")

    if "Wrong answer." in response:
        print("The prediction was incorrect.")
    elif "Correct answer." in response:
        # 尝试接收 FLAG
        flag = r.recvline().decode().strip()
        print(f"Flag: {flag}")
    else:
        print("Unexpected response from server.")

    r.interactive()


if __name__ == "__main__":
    main()

"""
Problem: 14511992599573816421,250244187270459081698779405311522902978,266283989083802555728983142563390459027,38381737634870930965937900091677866755,248191094868887187687225603566700568951,329981188901404025516596763388029733155,185136087992442826540885752098087294761,312861585677614356556458747806137688130,30199083421400926900617130627602601190,121503878655234200977170715990253231260,57193134523891038004599964877949148204,199631906739756428051922010099179338717,78605606870378262267665575160275642324,93441371299702369870837603910268121310,279105497660419580055296706306064729567,127303756196175945477130773293473088759
"""
