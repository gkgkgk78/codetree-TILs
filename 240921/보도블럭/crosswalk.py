import sys
input = sys.stdin.readline

answer = 0
n, l = map(int, input().split())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))


def check_left(row, index, visit):
    if index - l < 0:
        return 0
    now = index - 1
    before = graph[row][index]
    for i in range(l - 1):
        if graph[row][now] == before and visit[now] == 0:
            now -= 1
            continue
        else:
            return 0
    return 1


def check_right(row, index, visit):
    if index + 1 + l >= n:
        return 0
    now = index + 1
    before = graph[row][index]
    for i in range(l):
        if graph[row][now] == before - 1 and visit[now] == 0:
            now += 1
            continue
        else:
            return 0
    return 1


def check_row(index):
    global answer
    before = graph[index][0]
    start = 0
    visit = [0] * (n)
    while start < n:
        if start == n - 1:
            break
        if graph[index][start + 1] == before:
            start += 1
            continue
        else:
            if abs(graph[index][start + 1] - before) >= 2:
                return
            if graph[index][start + 1] > before:
                check = check_left(index, start, visit)
                if (check == 0):
                    return
                test = start
                for i in range(l):
                    visit[test] = 1
                    test -= 1
                start += 1
            else:
                check = check_right(index, start, visit)
                if (check == 0):
                    return
                test = start + 1
                for i in range(l):
                    visit[test] = 1
                    test += 1
                start += l
        before = graph[index][start]
    answer += 1


def check_up(row, index, visit):
    if row + 1 - l < 0:
        return 0
    now = row - 1
    before = graph[row][index]
    for i in range(l - 1):
        if graph[now][index] == before and visit[now] == 0:
            now -= 1
            continue
        else:
            return 0
    return 1


def check_down(row, index, visit):
    if row + l >= n:
        return 0
    now = row + 1
    before = graph[row][index]
    for i in range(l):
        if graph[now][index] == before - 1 and visit[now] == 0:
            now += 1
            continue
        else:
            return 0
    return 1


def check_col(index):
    global answer
    before = graph[0][index]
    start = 0
    visit = [0] * (n)
    while start < n:
        if start == n - 1:
            break
        if graph[start + 1][index] == before:
            start += 1
            continue
        else:
            if abs(graph[start + 1][index] - before) >= 2:
                return
            if graph[start + 1][index] > before:
                check = check_up(start, index, visit)
                if (check == 0):
                    return
                test = start - 1
                for i in range(l):
                    visit[test] = 1
                    test -= 1
                start += 1
            else:
                check = check_down(start + 1, index, visit)
                if (check == 0):
                    return
                test = start + 1
                for i in range(l):
                    visit[test] = 1
                    test += 1
                start += l
        before = graph[index][start]
    answer += 1


# 행
for i in range(n):
    check_row(i)
# 열
for i in range(n):
    check_col(i)

print(answer)