import sys


dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

N, M = map(int, sys.stdin.readline().split())
board = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
max_safe_area = 0
virus_list = []
for i in range(N):
    for j in range(M):
        if board[i][j] == 2:
            virus_list.append((i, j))


def get_safe_area(brd):
    cnt = 0
    for i in range(N):
        for j in range(M):
            if brd[i][j] == 0:
                cnt += 1
    return cnt


def select_walls(start, walls):
    global max_safe_area
    if walls == 3:
        new_board = [b[:] for b in board]
        for vx, vy in virus_list:
            spread_virus(vx, vy, new_board)
        safe_area = get_safe_area(new_board)
        max_safe_area = max(max_safe_area, safe_area)
        return
    else:
        for i in range(start, N*M):
            r = i // M
            c = i % M
            if board[r][c] == 0:
                board[r][c] = 1
                select_walls(i, walls+1)
                board[r][c] = 0


def spread_virus(vx, vy, brd):
    if brd[vx][vy] == 2:
        for k in range(4):
            nx = vx + dx[k]
            ny = vy + dy[k]
            if 0 <= nx < N and 0 <= ny < M and brd[nx][ny] == 0:
                brd[nx][ny] = 2
                spread_virus(nx, ny, brd)


select_walls(0, 0)
print(max_safe_area)
