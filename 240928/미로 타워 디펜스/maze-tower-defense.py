import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
answer = 0


def make(q):
    global graph
    graph=[[0]*(n)for _ in range(n)]
    x, y = n // 2, n // 2
    index = 2
    cnt = 0
    go = 1
    check = 0

    while q:
        # 해당 방향으로 go만큼 이동
        for _ in range(go):
            x += dx[index]
            y += dy[index]
            if x < 0 or y < 0:
                check = 1
                break
            if len(q) == 0:
                check = 1
                break
            graph[x][y] = q.popleft()
        if check == 1:
            break
        cnt += 1
        if cnt == 2:
            go += 1
            cnt = 0
        index-=1
        if index<0:
            index=3


def attack(d, p):
    global answer
    x, y = n // 2, n // 2
    for _ in range(p):
        x += dx[d]
        y += dy[d]
        answer += graph[x][y]
        graph[x][y] = 0


def get():
    x, y = n // 2, n // 2
    index = 2
    cnt = 0
    go = 1
    check = 0
    q = deque()
    while 1:
        # 해당 방향으로 go만큼 이동
        for _ in range(go):
            x += dx[index]
            y += dy[index]
            if x < 0 or y < 0:
                check = 1
                break
            if graph[x][y] == 0:
                continue
            q.append(graph[x][y])
        if check == 1:
            break
        cnt += 1
        if cnt == 2:
            go += 1
            cnt = 0
        index -= 1
        if index < 0:
            index = 3
    return q
def delete(q):
    global answer
    while 1:
        check=0
        origin=deque()
        temp=deque()
        before=-1
        size=0
        while q:
            now=q.popleft()
            if before==-1:
                before = now
                size = 1
                temp.append(now)
                continue
            if now!=before:
                if len(temp)<4:
                    while temp:
                        origin.append(temp.popleft())
                elif len(temp)>=4:
                    check=1
                    answer+=before*size
                size=1
                before=now
                temp=deque()
                temp.append(now)
            else:
                temp.append(now)
                size+=1
        if len(temp) < 4:
            while temp:
                origin.append(temp.popleft())
        elif len(temp) >= 4:
            check = 1
            answer += before * size
        q=origin
        if check==0:
            break
    return q

def make_pair(q):

    origin=deque()
    before=-1
    size=0
    while q:
        now=q.popleft()
        if before==-1:
            size=1
            before=now
            continue
        if now!=before:
            origin.append(size)
            origin.append(before)
            before=now
            size=1
        else:
            size+=1
    origin.append(size)
    origin.append(before)
    return origin


for _ in range(m):
    a1, a2 = map(int, input().split())
    # 공격
    attack(a1, a2)
    # 빈공간 채우기
    now=get()
    # 몬스터의 종류가 4번이상 반복되면 삭제
    now=delete(now)
    # 짝 지어주기
    now=make_pair(now)
    # 배치하기
    make(now)


print(answer)