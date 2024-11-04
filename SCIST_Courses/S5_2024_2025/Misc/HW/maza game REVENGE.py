from pwn import *

r = remote("lab.scist.org", 31013)

directions = {"up": b"W", "down": b"S", "left": b"A", "right": b"D"}
moves = [(0, 1, "right"), (0, -1, "left"), (1, 0, "down"), (-1, 0, "up")]


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

    return maze_matrix


def dfs(maze_matrix, start, end):
    stack = [(start, [])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == end:
            return path

        visited.add((x, y))

        for dx, dy, direction in moves:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(maze_matrix)
                and 0 <= ny < len(maze_matrix[0])
                and (nx, ny) not in visited
            ):
                if maze_matrix[nx][ny] == 0 or maze_matrix[nx][ny] == "E":
                    stack.append(((nx, ny), path + [direction]))
    return None


def find_positions(maze_matrix):
    start = end = None
    for i, row in enumerate(maze_matrix):
        for j, cell in enumerate(row):
            if cell == "P":
                start = (i, j)
            elif cell == "E":
                end = (i, j)
    return start, end


if __name__ == "__main__":
    while True:
        try:
            maze_matrix = read_maze()
            start, end = find_positions(maze_matrix)
            if start and end:
                path = dfs(maze_matrix, start, end)
                if path:
                    for move in path:
                        r.sendline(directions[move])
        except:
            break
    r.interactive()
