import sys
from collections import deque

MAX_N = 100001

n, m = map(int, sys.stdin.readline().split())
board = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

people = [[-1, -1, -1, -1] for _ in range(m+1)]
for i in range(1, m+1):
    dst_x, dst_y = map(int, sys.stdin.readline().split())
    people[i][2] = dst_x - 1
    people[i][3] = dst_y - 1

# bfs 했을 때 거리 저장할 곳
dist_board = [[MAX_N] * n for _ in range(n)]


dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]


def bfs(tx, ty):
    global dist_board
    dist_board = [[MAX_N]*n for _ in range(n)]
    dist_board[tx][ty] = 0
    q = deque()
    q.append((tx, ty))
    while q:
        x, y = q.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] != -1 and dist_board[nx][ny] == MAX_N:
                    dist_board[nx][ny] = dist_board[x][y] + 1
                    q.append((nx, ny))


def init(p_idx):
    dst_x, dst_y = people[p_idx][2], people[p_idx][3]
    bfs(dst_x, dst_y)
    dist = MAX_N
    bc_x, bc_y = 0, 0

    # 목표 편의점과 가장 가까운 베이스 캠프 찾기
    for i in range(n):
        for j in range(n):
            if board[i][j] != 1:
                continue
            if dist_board[i][j] < dist:
                dist = dist_board[i][j]
                bc_x = i
                bc_y = j

    people[p_idx][0] = bc_x
    people[p_idx][1] = bc_y
    board[bc_x][bc_y] = -1


def move_people(p_idx):
    cur_x, cur_y, tx, ty = people[p_idx]
    if is_arrived(p_idx):
        return
    dist = MAX_N
    dist_k = -1
    bfs(tx, ty)

    # 현재 상하좌우 중에 목표 편의점과 가장 거리가 가까운 애로 현재 위치를 옮겨야함
    for k in range(4):
        nx = cur_x + dx[k]
        ny = cur_y + dy[k]
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] != -1:
            if dist_board[nx][ny] < dist:
                dist = dist_board[nx][ny]
                dist_k = k

    people[p_idx][0] += dx[dist_k]
    people[p_idx][1] += dy[dist_k]


def check_arrived(p_idx):
    if is_arrived(p_idx):
        board[people[p_idx][0]][people[p_idx][1]] = -1


def all_arrived():
    for p_idx in range(1, m+1):
        if not is_arrived(p_idx):
            return False
    return True


def is_arrived(p_idx):
    cur_x, cur_y, dst_x, dst_y = people[p_idx]
    if cur_x == dst_x and cur_y == dst_y:
        return True
    return False


t = 0

while not all_arrived():
    t += 1
    for p_idx in range(1, t):
        if p_idx <= m:
            move_people(p_idx)

    for p_idx in range(1, t):
        if p_idx <= m:
            check_arrived(p_idx)

    if t <= m:
        init(t)
print(t)
