#2시간 32분
import sys
from collections import deque
import heapq

input = sys.stdin.readline

# 애초에 공격력이 0인 포탑이 존재 가능함
# 하나의 턴이 k번 반복이 된다
# 부서지지 않은 포탑이 1개가 된다면 즉시 중지된다


n, m, k = map(int, input().split())

# 포탑 관리는 일차원 배여롤 해서 관리를 해보도록 하자

# 포탑  : x,y, 공격력, 가장 최근에 공격한거

graph = []
portal = [[0] * (m) for _ in range(n)]
for i in range(n):
    e = list(map(int, input().split()))
    graph.append(e)


def get_attacker():
    # 공격자 선정하기
    temp = []
    for i in range(n):
        for j in range(m):
            if graph[i][j] > 0:
                temp.append([i, j, graph[i][j], portal[i][j]])
    temp = sorted(temp, key=lambda x: (x[2], -x[3], -(x[0] + x[1]), -x[1]))
    now = temp[0]
    graph[now[0]][now[1]] += (n + m)
    temp[0][2] += (n + m)
    return temp[0]


def attacked(x, y):
    # 자신을 제외한 가장 강한 포탑을 공격한다
    temp = []
    for i in range(n):
        for j in range(m):
            if i == x and j == y:
                continue
            if graph[i][j] > 0:
                temp.append([i, j, graph[i][j], portal[i][j]])
    temp = sorted(temp, key=lambda x: (-x[2], x[3], (x[0] + x[1]), x[1]))
    now = temp[0]
    return now


# 최단 경로 찾자
def go(gx, gy, tx, ty):
    visit = [[0] * m for _ in range(n)]
    path = [[[] for _ in range(m)] for _ in range(n)]
    q = deque()
    visit[gx][gy] = 1
    # 부서진 포탑 있을시 지나지 못한다
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    q.append((gx, gy, 1))  # x,y, 순서
    while q:
        x, y, time = q.popleft()
        if x == tx and y == ty:
            break
        for i in range(4):
            zx = dx[i] + x
            zy = dy[i] + y
            if not (0 <= zx < n and 0 <= zy < m):
                # 좌표 변환 해야함
                if zy >= m:
                    zy = 0
                if zy < 0:
                    zy = m - 1
                if zx < 0:
                    zx = n - 1
                if zx >= n:
                    zx = 0
            if graph[zx][zy] > 0 and visit[zx][zy] == 0:
                visit[zx][zy] = time + 1
                q.append((zx, zy, time + 1))
                path[zx][zy] = [x, y]
    if visit[tx][ty] != 0:
        # 이제 점수 깎으면 됨
        graph[tx][ty] -= graph[gx][gy]
        visit=[[0] * m for _ in range(n)]
        visit[tx][ty]=1
        delete(tx, ty, gx, gy, visit, graph[gx][gy], path)
        if graph[tx][ty] <= 0:
            graph[tx][ty] = 0
        return [1, visit]
    else:
        return [0, visit]


def delete(gx, gy, tx, ty, visited, tack, path):
    # 부서진 포탑 있을시 지나지 못한다
    [zx, zy] = path[gx][gy]
    visited[zx][zy]=1
    if zx==tx and zy==ty:
        return
    graph[zx][zy] -= tack // 2
    if graph[zx][zy] <= 0:
        graph[zx][zy] = 0
    delete(zx, zy, tx, ty, visited, tack, path)


def bomb(gx, gy, tx, ty):
    # 포탄 공격 하자
    dx = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
    visit = [[0] * m for _ in range(n)]
    visit[gx][gy] = 1
    for i in range(len(dx)):
        zx = dx[i] + tx
        zy = dy[i] + ty
        if not (0 <= zx < n and 0 <= zy < m):
            # 좌표 변환 해야함
            if zy >= m:
                zy = 0
            if zy < 0:
                zy = m - 1
            if zx < 0:
                zx = n - 1
            if zx >= n:
                zx = 0
        if zx == gx and zy == gy:
            continue
        if graph[zx][zy] == 0:
            continue
        if zx==tx and zy==ty:
            graph[zx][zy] -= graph[gx][gy]
        else:
            graph[zx][zy] -= graph[gx][gy] // 2
        if graph[zx][zy]<=0:
            graph[zx][zy]=0
        visit[zx][zy] = 1
    return visit


def growth(visit):
    for i in range(n):
        for j in range(m):
            if visit[i][j] == 0 and graph[i][j] > 0:
                graph[i][j] += 1


def attacks(attack, gone):
    # 공격자가 레이저 공격하고자 함

    # 최단경로 확인하기
    check1 = go(attack[0], attack[1], gone[0], gone[1])
    if check1[0] == 1:
        # 이제 증가해주는 작업하면 된다
        growth(check1[1])
        return
    # 이제 포탄 공격 하면 된다
    visit = bomb(attack[0], attack[1], gone[0], gone[1])
    growth(visit)

def check():
    co=0
    for i in range(n):
        for j in range(m):
            if graph[i][j] > 0:
                co+=1
    return co

for tt in range(k):
    if check()==1:
        break
    attack = get_attacker()
    gone = attacked(attack[0], attack[1])
    portal[attack[0]][attack[1]] = tt+1  # 공격자 공격한거 갱신
    attacks(attack, gone)


answer = -1
for i in range(n):
    for j in range(m):
        answer = max(answer, graph[i][j])
print(answer)