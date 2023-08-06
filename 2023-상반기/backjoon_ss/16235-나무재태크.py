import sys
from pprint import pprint


N, M, K = map(int, sys.stdin.readline().split())
soil = [[5] * N for _ in range(N)]
a_board = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
trees = [[[] for _ in range(N)] for _ in range(N)]

for _ in range(M):
    x, y, z = map(int, sys.stdin.readline().split())
    trees[x-1][y-1].append(z)

for i in range(N):
    for j in range(N):
        if trees[i][j]:
            trees[i][j].sort()
# print(trees)

dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, -1, 1, -1, 0, 1]


# 봄
# 어린 나무부터 자기 나이만큼 양분을 먹기
def spring():
    dead_tree = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if trees[i][j]:
                tmp_tree = []
                for idx, tree in enumerate(trees[i][j]):
                    if tree <= soil[i][j]:
                        soil[i][j] -= tree
                        tmp_tree.append(tree+1)
                    else:
                        dead_tree[i][j] += tree // 2
                trees[i][j] = tmp_tree
    # 여름
    # 봄에 죽은 나무가 양분이 됨
    # 양분 -> 죽은 나무 마다 나이 // 2 만큼 칸에 추가됨
    for i in range(N):
        for j in range(N):
            if dead_tree[i][j]:
                soil[i][j] += dead_tree[i][j]


# 가을
# 번식. 번식하는 나무는 나이가 5의 배수
# 인접한 8개의 칸에 나이가 1인 나무가 생김
def fall():
    new_tree = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if trees[i][j]:
                for tree in trees[i][j]:
                    if tree % 5 == 0:
                        for k in range(8):
                            nx = i + dx[k]
                            ny = j + dy[k]
                            if 0 <= nx < N and 0 <= ny < N:
                                new_tree[nx][ny].append(1)
    for i in range(N):
        for j in range(N):
            if new_tree[i][j]:
                trees[i][j] = new_tree[i][j] + trees[i][j]

    # pprint(trees)

# 겨울
# 땅에 양분 추가
def winter():
    for i in range(N):
        for j in range(N):
            soil[i][j] += a_board[i][j]


def run():
    tree = 0
    for _ in range(K):
        spring()
        fall()
        winter()
    for i in range(N):
        for j in range(N):
            if trees[i][j]:
                tree += len(trees[i][j])

    print(tree)


run()