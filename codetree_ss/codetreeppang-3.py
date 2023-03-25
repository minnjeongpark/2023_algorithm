from collections import deque

MAX_ = 100001

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

people = [[-1, -1, -1, -1] for _ in range(m+1)]
for i in range(1, m+1):
    target_x, target_y = map(int, input().split())
    people[i][2] = target_x-1
    people[i][3] = target_y-1

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

dist = [[MAX_] * n for _ in range(n)]


def is_arrived(p_num):
    cx, cy, tx, ty = people[p_num]
    if cx == tx and cy == ty:
        return True
    return False


def check_arrived(p_num):
    if is_arrived(p_num):
        cx, cy, tx, ty = people[p_num]
        board[cx][cy] = -1


def is_all_arrived():
    for idx in range(1, m+1):
        if not is_arrived(idx):
            return False
    return True


def bfs(target_x, target_y):
    global dist
    dist = [[MAX_] * n for _ in range(n)]

    q = deque()
    q.append((target_x, target_y))
    dist[target_x][target_y] = 0

    while q:
        x, y = q.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] != -1 and dist[nx][ny] == MAX_:
                q.append((nx, ny))
                dist[nx][ny] = dist[x][y] + 1


def init(p_num):
    # 베이스 캠프 찾기

    tx, ty = people[p_num][2], people[p_num][3]
    bfs(tx, ty)
    min_dist = MAX_
    min_i, min_j = -1, -1
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1 and dist[i][j] < min_dist:
                min_dist = dist[i][j]
                min_i = i
                min_j = j
    people[p_num][0] = min_i
    people[p_num][1] = min_j
    board[min_i][min_j] = -1


def move_person(p_num):
    if is_arrived(p_num):
        return
    cx, cy, tx, ty = people[p_num]
    bfs(tx, ty)

    min_dist = MAX_
    min_dir = -1

    for k in range(4):
        nx = cx + dx[k]
        ny = cy + dy[k]
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0 and dist[nx][ny] < min_dist:
            min_dist = dist[nx][ny]
            min_dir = k
    people[p_num][0] += dx[min_dir]
    people[p_num][1] += dy[min_dir]


def run():
    t = 0
    while not is_all_arrived():
        t += 1
        for p_num in range(1, t):
            if p_num <= m:
                move_person(p_num)
        for p_num in range(1, t):
            if p_num <= m:
                check_arrived(p_num)
        if t <= m:
            init(t)

    print(t)


run()