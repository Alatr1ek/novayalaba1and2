import random
import tkinter as tk

N, M = 14, 14

maze = [[1] * M for _ in range(N)]
start = (1, 1)
maze[3][2] = 0
stack = [start]
visited = {start}
dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]

while stack:
    r, c = stack[-1]
    neighbors = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 1 <= nr <= N - 2 and 1 <= nc <= M - 2 and (nr, nc) not in visited:
            neighbors.append((nr, nc, r + dr // 2, c + dc // 2))
    if neighbors:
        nr, nc, wr, wc = random.choice(neighbors)
        maze[nr][nc] = 0
        maze[wr][wc] = 0
        visited.add((nr, nc))
        stack.append((nr, nc))
    else:
        stack.pop()

exit_row = None
for r in range(1, N - 1):
    if maze[r][M - 2] == 0:
        exit_row = r
        break

if exit_row is None:
    exit_row = N // 2
    maze[exit_row][M - 2] = 0

maze[exit_row][M - 1] = 0
exit_pos = (exit_row, M - 1)

size = 30
root = tk.Tk()
root.title("Таракан идет искать свободу")
canvas = tk.Canvas(root, width=M * size, height=N * size, bg='white')
canvas.pack()

COLOR_WALL = 'orange'
COLOR_PATH = 'white'
COLOR_VISITED = '#cccccc'
COLOR_PATH_FINAL = 'blue'
COLOR_START = 'green'
COLOR_EXIT = 'red'

search_stack = [start]
visited_search = {start}
parent = {start: None}
found = False
final_path = []


def draw():
    canvas.delete("all")
    for r in range(N):
        for c in range(M):
            x1, y1 = c * size, r * size
            x2, y2 = x1 + size, y1 + size
            if maze[r][c] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_WALL, outline='gray')
            else:
                if (r, c) in visited_search:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_VISITED, outline='gray')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PATH, outline='gray')
    for r, c in final_path:
        canvas.create_rectangle(c * size, r * size, (c + 1) * size, (r + 1) * size,
                                fill=COLOR_PATH_FINAL, outline='orange')
    sr, sc = start
    er, ec = exit_pos
    canvas.create_rectangle(sc * size, sr * size, (sc + 1) * size, (sr + 1) * size,
                            fill=COLOR_START, outline='darkgreen')
    canvas.create_rectangle(ec * size, er * size, (ec + 1) * size, (er + 1) * size, fill=COLOR_EXIT,
                            outline='darkred')


def step():
    global found, final_path
    if found:
        return

    if not search_stack:
        print("Выход не найден!")
        return

    r, c = search_stack.pop()

    if (r, c) == exit_pos:
        found = True

        cur = exit_pos
        while cur != start:
            final_path.append(cur)
            cur = parent[cur]
        draw()
        return

    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < M and maze[nr][nc] == 0 and (nr, nc) not in visited_search:
            visited_search.add((nr, nc))
            parent[(nr, nc)] = (r, c)
            search_stack.append((nr, nc))

    draw()
    root.after(90, step)


draw()
root.after(500, step)
root.mainloop()
