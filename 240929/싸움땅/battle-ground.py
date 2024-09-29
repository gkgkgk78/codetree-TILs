import sys

input = sys.stdin.readline
n, m, k = map(int, input().split())
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
guns = [[[] for _ in range(n)] for _ in range(n)]
players_graph = [[[] for _ in range(n)] for _ in range(n)]
players = []  # x,y,dir,능력치,gun,살아있는지
answer = [0] * (m)
for i in range(n):
    now=list(map(int, input().split()))
    for j in range(n):
        guns[i][j].append(now[j])
for i in range(m):
    x, y, d, s = map(int, input().split())
    players.append((x - 1, y - 1, d, s, 0, 1))
    players_graph[x - 1][y - 1] = [i]


def go(x, y, d):
    zx = x + dx[d]
    zy = y + dy[d]
    if 0 <= zx < n and 0 <= zy < m:
        return [zx, zy, d]
    else:
        d = (d + 2) % 4
        zx = x + dx[d]
        zy = y + dy[d]
        return [zx, zy, d]


def fight(x, y):
    first=players[x]
    second=players[y]
    s1 = first[3] + first[4]
    s2 = second[3] + second[4]
    if s1 > s2:
        return [x, y]
    elif s1 < s2:
        return [y, x]
    else:
        if first[3] > second[3]:
            return [x, y]
        else:
            return [y, x]


def move_loser(index):
    x, y, d, s, gun, live = players[index]
    players_graph[x][y]=[]
    guns[x][y].append(gun)
    gun = 0
    zx = x + dx[d]
    zy = y + dy[d]
    if 0 <= zx < n and 0 <= zy < n and len(players_graph[zx][zy]) == 0:
        x = zx
        y = zy
    else:
        for i in range(3):
            d = (d + 1) % 4
            zx = x + dx[d]
            zy = y + dy[d]
            if 0 <= zx < n and 0 <= zy < n and len(players_graph[zx][zy]) == 0:
                x = zx
                y = zy
                break
    check = guns[x][y]
    if len(check)>0:
        check.sort(reverse=True)
        gun = check[0]
        check = check[1:]
        guns[x][y] = check
    players[index] = (x, y, d, s, gun, live)

def move_last(index):
    x, y, d, s, gun, live = players[index]
    players_graph[x][y]=[]
    if gun != 0:
        guns[x][y].append(gun)
    check = guns[x][y]
    check.sort(reverse=True)
    gun = check[0]
    check = check[1:]
    guns[x][y] = check
    players[index] = (x, y, d, s, gun, live)
    players_graph[x][y]=[index]


def move(index):
    x, y, d, s, gun, live = players[index]
    players_graph[x][y]=[]
    first_move = go(x, y, d)
    x, y, d = first_move[0], first_move[1], first_move[2]
    if len(players_graph[x][y]) == 0:
        if len(guns[x][y]) > 0:
            if gun != 0:
                guns[x][y].append(gun)
            check = guns[x][y]
            check.sort(reverse=True)
            gun = check[0]
            check = check[1:]
            guns[x][y] = check
            players[index] = (x, y, d, s, gun, live)
            players_graph[x][y]=[index]

    else:
        # 싸워야 함
        other = players_graph[x][y][0]
        players[index] = (x, y, d, s, gun, live)
        winner_index, loser_index = fight(index, other)
        winner=players[winner_index]
        loser=players[loser_index]
        answer[winner_index] += (winner[3] + winner[4]) - (loser[3] + loser[4])
        # 진플레이어 부터 처리 해야함
        move_loser(loser_index)
        zx, zy, zd, zs, zgun, zlive = players[winner_index]
        players[winner_index]=(x,y,zd, zs, zgun, zlive)
        move_last(winner_index)



for _ in range(k):
    for i in range(m):
        x, y, d, s, gun, live = players[i]
        if live == 1:
            move(i)


print(*answer)