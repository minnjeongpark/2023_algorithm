import sys


n, m, q = -1, -1, -1
N = 100000
M = 100000


prv, nxt = [0] * (M+1), [0] * (M+1) # i번 박스의 prev, next
head, tail, num_gift = [0] * (N+1), [0] * (N+1), [0] * (N+1)


def init(elem):
    n, m = elem[1], elem[2] # n개의 벨트, m개의 선물
    boxes = [[] for _ in range(n)] # 벨트 개수 만큼 리스트
    for id in range(1, m+1): # 박스 숫자
        box_num = elem[id+2]
        box_num -= 1
        boxes[box_num].append(id)
    # 초기 베트의 head, tail, prev, next 관리
    for i in range(n):
        if len(boxes[i]) == 0:
            continue

        # head, tail
        head[i] = boxes[i][0]
        tail[i] = boxes[i][-1]

        num_gift[i] = len(boxes[i])

        # prv, nxt
        for j in range(len(boxes[i]) - 1):
            nxt[boxes[i][j]] = boxes[i][j+1]
            prv[boxes[i][j+1]] = boxes[i][j]


def move(elem):
    m_src, m_dst = elem[1] - 1, elem[2] - 1 # 벨트 번호

    # m_src에 아무것도 없다면
    if num_gift[m_src] == 0:
        print(num_gift[m_dst])
        return

    # m_dst 에 아무것도 없다면
    # 그대로 옮기기
    if num_gift[m_dst] == 0:
        head[m_dst] = head[m_src]
        tail[m_dst] = head[m_src]
    else:
        origin_head = head[m_dst]
        head[m_dst] = head[m_src]

        src_tail = tail[m_src]
        nxt[src_tail] = origin_head
        prv[origin_head] = src_tail

    head[m_src] = tail[m_src] = 0

    # 선물 상자 수
    num_gift[m_dst] += num_gift[m_src]
    num_gift[m_src] = 0

    print(num_gift[m_dst])


def remove_head(belt_num):
    if not num_gift[belt_num]:
        return 0

    # only one box in belt
    # then prv, nxt also 0
    if num_gift[belt_num] == 1:
        _id = head[belt_num]
        head[belt_num] = tail[belt_num] = 0
        num_gift[belt_num] = 0
        return _id

    hid = head[belt_num]
    next_head = nxt[hid]
    nxt[hid] = prv[next_head] = 0
    num_gift[belt_num] -= 1
    head[belt_num] = next_head

    return hid


def push_head(belt_num, box_num):
    if box_num == 0:
        return

    # belt is empty
    if not num_gift[belt_num]:
        head[belt_num] = tail[belt_num] = box_num
        num_gift[belt_num] = 1

    else:
        origin_num = head[belt_num]
        prv[origin_num] = box_num
        head[belt_num] = origin_num
        nxt[box_num] = origin_num
        num_gift[belt_num] += 1


def change(elem):
    m_src, m_dst = elem[1] - 1, elem[2] - 1

    src_head = remove_head(m_src)
    dst_head = remove_head(m_dst)
    push_head(m_dst, src_head)
    push_head(m_src, dst_head)
    print(num_gift[m_dst])


def divide(elem):
    m_src, m_dst = elem[1] - 1, elem[2] - 1

    cnt = num_gift[m_src]
    box_ids = []
    for _ in range(cnt // 2):
        box_ids.append(remove_head(m_src))

    for i in range(len(box_ids) - 1, -1):
        push_head(m_dst, box_ids[i])

    print(num_gift[m_dst])


def get_box_info(elem):
    bid = elem[1]
    a = prv[bid] if prv[bid] != 0 else -1
    b = nxt[bid] if nxt[bid] != 0 else -1
    print(a + 2 * b)


def get_belt_info(elem):
    belt_id = elem[1]
    a = head[belt_id] if head[belt_id] != 0 else -1
    b = tail[belt_id] if tail[belt_id] != 0 else -1
    c = num_gift[belt_id]
    print(a + 2 * b + 3 * c)


q = int(sys.stdin.readline())
for _ in range(q):
    elem = list(map(int, sys.stdin.readline().split()))
    cmd = elem[0]

    if cmd == 100:
        init(elem)
    elif cmd == 200:
        move(elem)
    elif cmd == 300:
        change(elem)
    elif cmd == 400:
        divide(elem)
    elif cmd == 500:
        get_box_info(elem)
    else:
        get_belt_info(elem)