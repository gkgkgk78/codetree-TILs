import sys

from collections import deque
import heapq

input = sys.stdin.readline

# 몬스터 복제 시도
# 몬스터 이동
# 팩맨 이동
#   팩맨 이동시에는 이동하는 과정에 있는 몬스터만 먹는다
# 몬스터 시체 소멸
# 몬스터 복제 완성

m, t = map(int, input().split())
r, c = map(int, input().split())
pack_x = r - 1
pack_y = c - 1

# 전체 그래프
# 몬스터, 알,시체


monster_graph = [[[] for _ in range(4)] for _ in range(4)]

egg_graph = [[[] for _ in range(4)] for _ in range(4)]
death_graph = [[[] for _ in range(4)] for _ in range(4)]
dir = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
for _ in range(m):
    r, c, d = map(int, input().split())
    r -= 1
    c -= 1
    d -= 1
    monster_graph[r][c].append(d)  # 방향만 집어 넣자


def copy_monster():
    for i in range(4):
        for j in range(4):
            for k in monster_graph[i][j]:
                egg_graph[i][j].append(k)


def is_move_monster(x, y, d):
    now = dir[d]
    zx = x + now[0]
    zy = y + now[1]
    if not (0 <= zx < 4 and 0 <= zy < 4):
        return 0
    if zx == pack_x and zy == pack_y:
        return 0
    if len(death_graph[zx][zy]) > 0:
        return 0
    return 1


def move_monster():
    global monster_graph
    temp = [[[] for _ in range(4)] for _ in range(4)]  # 움직이게 되는 임시 얘들
    for i in range(4):
        for j in range(4):
            for k in monster_graph[i][j]:
                now = k
                find = 0
                for l in range(8):
                    check = is_move_monster(i, j, now)
                    if check == 1:
                        find = 1
                        break
                    now = (now + 1) % 8
                if find == 1:
                    # 변경된 자리로 이동 하면 됨
                    now1 = dir[now]
                    zx = i + now1[0]
                    zy = j + now1[1]
                    temp[zx][zy].append(now)
                else:
                    # 지금 자리 유지
                    temp[i][j].append(k)
    monster_graph = temp


pack_move_route = []
dx = [-1,0,1,0]  # 상좌하우로 움직인다
dy = [0,-1,0,1]


def make_pack_move_route():
    for i in range(4):
        for j in range(4):
            for k in range(4):
                pack_move_route.append((i, j, k))


make_pack_move_route()


def eat_monster(ind):
    global pack_x, pack_y
    now = pack_move_route[ind]
    for i in now:
        pack_x = pack_x + dx[i]
        pack_y = pack_y + dy[i]
        for k in monster_graph[pack_x][pack_y]:
            death_graph[pack_x][pack_y].append(3)
        monster_graph[pack_x][pack_y] = []


def move_pack():
    temp = []
    # 팩맨은 총 3칸을 이동하게 된다
    for i in range(len(pack_move_route)):
        check = 0
        data = 0
        zx = pack_x
        zy = pack_y
        tt = []
        for k in range(3):
            now = pack_move_route[i][k]
            zx += dx[now]
            zy += dy[now]
            if not (0 <= zx < 4 and 0 <= zy < 4):
                check = 1
                break
            if zx == pack_x and zy == pack_y or ((zx, zy) in tt):
                continue
            data += len(monster_graph[zx][zy])
            tt.append((zx, zy))

        if check == 0:
            temp.append((data, i))
    temp = sorted(temp, key=lambda x: (-x[0], x[1]))
    # 이제 이동하면서 먹어 치우기만 하면 된다
    eat_monster(temp[0][1])


def delete_death():
    for i in range(4):
        for j in range(4):
            temp = []
            for k in death_graph[i][j]:
                k -= 1
                if k > 0:
                    temp.append(k)
            death_graph[i][j] = temp


def make_monster():
    global egg_graph
    for i in range(4):
        for j in range(4):
            for k in egg_graph[i][j]:
                monster_graph[i][j].append(k)
    egg_graph = [[[] for _ in range(4)] for _ in range(4)]


for a in range(t):
    # 몬스터 복제 시도
    copy_monster()

    # 몬스터 이동
    move_monster()

    # 팩맨 이동
    move_pack()

    # 시체 소멸
    delete_death()

    # 몬스터 복제완성
    make_monster()
    #
    # print(a)
    # print("몬스터")
    # for i in monster_graph:
    #     print(i)
    # print("팩맨")
    # print(pack_x,pack_y)
    # #죽은
    # print("죽은")
    # for i in death_graph:
    #     print(i)
    # print("알")
    # for i in egg_graph:
    #     print(i)



answer = 0

for i in range(4):
    for j in range(4):
        now = monster_graph[i][j]
        answer += len(monster_graph[i][j])
print(answer)