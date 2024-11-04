from pwn import *
import time

# 連接到伺服器
r = remote("lab.scist.org", 31013)

# 定義方向的對應字符
directions = {"up": b"W", "down": b"S", "left": b"A", "right": b"D"}


def read_maze():
    r.recvuntil(b"  ========")
    maze_rows = r.recvuntil(b"move:", drop=True).decode().strip().split("\n")
    maze_matrix = []
    for row in maze_rows:
        row_data = []
        for idx in range(0, len(row), 2):
            if row[idx] == "█":
                row_data.append(1)
            elif row[idx] == "P":
                row_data.append("P")
            elif row[idx] == "E":
                row_data.append("E")
            else:
                row_data.append(0)
        maze_matrix.append(row_data)

    for row in maze_matrix:
        print(row)


if __name__ == "__main__":
    read_maze()
    r.close()
