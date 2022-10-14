from sys import stdin
from collections import deque
input = stdin.readline

N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def art_score():
    group_arr = [[0 for _ in range(N)] for _ in range(N)]
    group = 1
    group_cnt = [1e9]
    group_val = [1e9]

    for i in range(N):
        for j in range(N):
            if group_arr[i][j] == 0:
                q = deque()
                q.append((i, j))
                group_arr[i][j] = group
                cnt = 1

                while(q):
                    x, y = q.popleft()

                    for k in range(4):
                        nx, ny = x + dx[k], y + dy[k]

                        if 0 <= nx < N and 0 <= ny < N and group_arr[nx][ny] == 0 and arr[nx][ny] == arr[i][j]:
                            q.append((nx, ny))
                            group_arr[nx][ny] = group
                            cnt += 1

                group_cnt += [cnt]
                group_val += [arr[i][j]]
                group += 1

    shared_lines = [[0 for _ in range(group)] for _ in range(group)]
    visited = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if visited[i][j] == 0:
                q = deque()
                q.append((i, j))
                visited[i][j] = 1

                while(q):
                    x, y = q.popleft()

                    for k in range(4):
                        nx, ny = x + dx[k], y + dy[k]

                        if 0 <= nx < N and 0 <= ny < N and visited[nx][ny] == 0:
                            if group_arr[nx][ny] == group_arr[i][j]:#Same Group
                                q.append((nx, ny))
                                visited[nx][ny] = 1
                            else:#Different Group
                                shared_lines[group_arr[i][j]][group_arr[nx][ny]] += 1
                                shared_lines[group_arr[nx][ny]][group_arr[i][j]] += 1
    
    sm = 0

    for i in range(1, group):
        for j in range(i + 1, group):
            sm += (group_cnt[i] + group_cnt[j]) * group_val[i] * group_val[j] * shared_lines[i][j]

    return sm

def rotate(x, y):
    row = x

    for j in range(y, y + N//2):
        stack = []
        for i in range(x + N//2 - 1, x - 1, -1):
            stack += [arr[i][j]]
        new_arr[row][y:y + N//2] = stack
        row += 1

ans = 0

for tc in range(4):
    ans += art_score()
    new_arr = [[0 for _ in range(N)] for _ in range(N)]
    rotate(0, 0)
    rotate(0, N//2 + 1)
    rotate(N//2 + 1, 0)
    rotate(N//2 + 1, N//2 + 1)

    new_arr[N//2][N//2] = arr[N//2][N//2]

    for i in range(N//2):#상에서 좌로
        new_arr[N//2][i] = arr[i][N//2]

    for i in range(N//2 + 1, N, 1):#하에서 우로
        new_arr[N//2][i] = arr[i][N//2]

    for i in range(N // 2):#좌에서 하로
        new_arr[N - 1 - i][N//2] = arr[N//2][i]

    for i in range(N // 2):#우에서 상으로
        new_arr[i][N//2] = arr[N//2][N - 1 - i]

    for i in range(N):
        for j in range(N):
            arr[i][j] = new_arr[i][j]

print(ans)
