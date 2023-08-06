from pprint import pprint

# 격자 크기, 박멸 진행되는 년 수, 제초제 확산 범위, 제초제 남아있는 년수
n, m, K, C = map(int, input().split())
C += 1
board = [list(map(int, input().split())) for _ in range(n)]

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

herbicide = [[0] * n for _ in range(n)]

# 대각선
cdx = [-1, -1, 1, 1]
cdy = [-1, 1, -1, 1]


# 1. 성장
def grow():
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0: # 나무가 있는 칸
                tree_grid = 0
                for k in range(4):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if 0 <= nx < n and 0 <= ny < n and board[nx][ny] > 0:
                        tree_grid += 1
                board[i][j] += tree_grid
    # pprint(board)


# 2. 번식
def breed():
    tmp_board = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                cnt = 0
                tmp = []
                for k in range(4):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    # 제초제 x, 나무 없는 칸에 번식 예정
                    if 0 <= nx < n and 0 <= ny < n:
                        if herbicide[nx][ny] == 0 and board[nx][ny] == 0:
                            cnt += 1
                            tmp.append((nx, ny))
                if cnt:
                    tree_num = board[i][j] // cnt
                    for _x, _y in tmp:
                        tmp_board[_x][_y] += tree_num
    for i in range(n):
        for j in range(n):
            board[i][j] += tmp_board[i][j]
    # pprint(board)


# 3. 제초제 위치 찾고 뿌리기 -> 나무가 가장 많이 박멸될 곳 찾기
# 나무가 없는 칸에 제초제 -> 박멸되는 나무 없음
# 나무가 있는 칸에 제초제 -> 4개의 대각선 방향으로 k 칸만큼 전파
# 단, 벽이나 나무가 없는 칸 일 경우 그 칸 까지만 제초제가 뿌려짐
# c년만큼 제초제 남아있고 c+1 제초제 사라짐
# 그 이후에 제초제 생기면 새로뿌려진 해로부터 c년 유지됨
herbicide_board = [[0]*n for _ in range(n)]


def spread(_x, _y, dir_k):
    global herbicide_board

    dead_tree = 0
    for i in range(1, K+1):
        nx = _x + cdx[dir_k]*i
        ny = _y + cdy[dir_k]*i
        if 0 <= nx < n and 0 <= ny < n:
            herbicide_board[nx][ny] = C
            if board[nx][ny] == -1 or board[nx][ny] == 0:
                break
            else:
                dead_tree += board[nx][ny]
    return dead_tree


def simulate(_x, _y):
    # _x, _y 자리에서부터 제초제 뿌리기
    global herbicide_board
    herbicide_board = [[0]*n for _ in range(n)]

    dead_tree = 0
    for dir_k in range(4):
        dead_tree += spread(_x, _y, dir_k)
    # pprint(herbicide_board)
    return dead_tree


def find_herbicide_spot():
    global herbicide
    max_dead_tree = 0
    final_herbicide_board = [[0]*n for _ in range(n)]
    r_x, r_y = -1, -1
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                tmp_tree_dead = board[i][j]
                tmp_tree_dead += simulate(i, j)
                if max_dead_tree < tmp_tree_dead:
                    max_dead_tree = tmp_tree_dead
                    r_x = i
                    r_y = j
                    final_herbicide_board = herbicide_board
    for i in range(n):
        for j in range(n):
            if final_herbicide_board[i][j] > 0:
                herbicide[i][j] = final_herbicide_board[i][j]
    herbicide[r_x][r_y] = C
    for i in range(n):
        for j in range(n):
            if herbicide[i][j] > 0 and board[i][j] > 0:
                board[i][j] = 0
    # print("spot: ", r_x, r_y, max_dead_tree)
    return max_dead_tree


def decrease_herbicide():
    for i in range(n):
        for j in range(n):
            if herbicide[i][j]:
                herbicide[i][j] -= 1


def run():
    dead_tree = 0
    for _ in range(m):
        grow()
        breed()
        dead_tree += find_herbicide_spot()
        decrease_herbicide()
        # pprint(board)
        # pprint(herbicide)
        # print("######")

    print(dead_tree)
run()