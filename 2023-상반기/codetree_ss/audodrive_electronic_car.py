from collections import deque
import sys

MAX_N = 10001
n, m, c = map(int, sys.stdin.readline().split())
board = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

start_x, start_y = map(int, sys.stdin.readline().split())
start_x -= 1
start_y -= 1

passengers_srt = []
passengers_dst = []

for _ in range(m):
    sx, sy, tx, ty = map(int, sys.stdin.readline().split())
    passengers_srt.append((sx-1, sy-1))
    passengers_dst.append((tx-1, ty-1))

dist = [[MAX_N] * n for _ in range(n)]


dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def bfs(sx, sy):
    global dist
    dist = [[MAX_N] * n for _ in range(n)]
    q = deque()
    q.append((sx, sy))
    dist[sx][sy] = 0
    while q:
        x, y = q.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0 and dist[nx][ny] == MAX_N:
                q.append((nx, ny))
                dist[nx][ny] = dist[x][y] + 1


# 가장 가까운 위치의 승객 선택
def select_passenger(sx, sy):
    bfs(sx, sy)
    min_dist = MAX_N
    min_passenger = -1
    for i in range(n):
        for j in range(n):
            if dist[i][j] < min_dist:
                for k in range(len(passengers_srt)):
                    p_srt_x, p_srt_y = passengers_srt[k]
                    if i == p_srt_x and j == p_srt_y:
                        # print(k, i, j)
                        min_passenger = k
                        min_dist = dist[i][j]
    # pprint(dist)
    # 태울 승객이 없음 -> 종료
    if min_passenger == -1:
        return -1
    # 태울 승객이 있다
    return min_passenger # passenger idx


def move():
    global start_x, start_y, c
    while c:
        if len(passengers_srt) == 0:
            print(c)
            break
        p_idx = select_passenger(start_x, start_y)
        if p_idx == -1:
            # print("p_idx == -1")
            print(-1)
            break
        dst_p_x, dst_p_y = passengers_dst[p_idx]
        start_x, start_y = passengers_srt[p_idx] # src_p
        c -= dist[start_x][start_y] # 연료 차감

        # 승객 목적지로 이동
        bfs(start_x, start_y)
        dst_dist = dist[dst_p_x][dst_p_y]

        if dst_dist == MAX_N:
            # print("dst_dist 갈 수 없음")
            print(-1)
            break
        if c < dst_dist:
            # print("연료 부족 ")
            print(-1)
            break
        c -= dist[dst_p_x][dst_p_y]
        passengers_srt.pop(p_idx)
        passengers_dst.pop(p_idx)
        start_x = dst_p_x
        start_y = dst_p_y
        c += dist[dst_p_x][dst_p_y] * 2


move()