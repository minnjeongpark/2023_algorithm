from collections import deque
import sys
from pprint import pprint


# 격자 크기 n, 사람 수 m
n, m = map(int, sys.stdin.readline().split())
# 격자 정보, 빈 칸: 0, 베이스 캠프: 1
graph = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
p = [[-1, -1, -1, -1] for _ in range(m+1)] # 현재 위치 x, y, 목표 위치 x, y
dist = [[10001]*n for _ in range(n)]

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

for i in range(1, m+1): # 각 사람마다의 목표 위치 저장
    x, y = map(int, sys.stdin.readline().split())
    p[i][2] = x-1
    p[i][3] = y-1


def bfs(tx, ty):
    global dist
    dist = [[10001]*n for _ in range(n)]
    dist[tx][ty] = 0
    q = deque()
    q.append((tx, ty))
    while q:
        x, y = q.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < n:
                if graph[nx][ny] != -1 and dist[nx][ny] == 10001:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))


def move_person(p_num):
    if is_arrived(p_num):
        return

    # 편의점으로부터 모든 격자의 거리 구한 후
    # 사람 위치의 네 방향 중 가장 최단 거리의 위치 구하기
    min_dist = 10001
    min_dir = -1
    x, y = p[p_num][0], p[p_num][1]
    tx, ty = p[p_num][2], p[p_num][3]
    bfs(tx, ty)
    for k in range(4):
        nx = x + dx[k]
        ny = y + dy[k]
        if 0 <= nx < n and 0 <= ny < n and graph[nx][ny] != -1:
            if dist[nx][ny] < min_dist:
                min_dist = dist[nx][ny]
                min_dir = k

    p[p_num][0] += dx[min_dir]
    p[p_num][1] += dy[min_dir]


def initiate(p_num): # p_num 번째 사람이 처음! 격자로 들어갈 때
    # 편의점과 가장 가까운 베이스캠프 구하기
    tx, ty = p[p_num][2], p[p_num][3]
    bfs(tx, ty)
    min_dist = 10001
    min_i = 0
    min_j = 0
    for i in range(n):
        for j in range(n):
            if graph[i][j] != 1:
                continue
            if dist[i][j] < min_dist:
                min_dist = dist[i][j]
                min_i = i
                min_j = j
    p[p_num][0] = min_i
    p[p_num][1] = min_j
    graph[p[p_num][0]][p[p_num][1]] = -1


def check_arrived(p_num):
    if is_arrived(p_num):
        graph[p[p_num][0]][p[p_num][1]] = -1


def is_arrived(p_num):
    if p[p_num][0] == p[p_num][2] and p[p_num][1] == p[p_num][3]:
        return True
    return False


def is_all_arrived():
    for i in range(1, m+1):
        if not is_arrived(i):
            return False
    return True


def run():
    t = 0
    while not is_all_arrived():
        t += 1
        for i in range(1, t):
            if i <= m:
                move_person(i)
        for i in range(1, t):
            if i <= m:
                check_arrived(i)
        if t <= m:
            initiate(t)
    print(t)


run()
