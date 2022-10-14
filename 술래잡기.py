from sys import stdin
from copy import deepcopy
input = stdin.readline

N, M, H, K = map(int, input().split())
runners = [[[] for _ in range(N)] for _ in range(N)]
catcher = [N//2, N//2]
trees = [[0 for _ in range(N)] for _ in range(N)]
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

for _ in range(M):
    #rd = {0: 우, 1: 하, 2: 좌, 3: 상}
    a, b, rd = map(int, input().split())
    runners[a - 1][b - 1].append(rd - 1)

for _ in range(H):
    a, b = map(int, input().split())
    trees[a - 1][b - 1] = 1

def runners_run():
    global runners
    new_runners = [[[] for _ in range(N)] for _ in range(N)]
    
    for x in range(N):
        for y in range(N):
            if runners[x][y] and ((abs(x - catcher[0]) + abs(y - catcher[1])) <= 3):
                while(runners[x][y]):
                    direction = runners[x][y].pop()

                    if not (0 <= x + dx[direction] < N and 0 <= y + dy[direction] < N):
                        if direction < 2: direction += 2
                        else: direction -= 2

                    nx, ny = x + dx[direction], y + dy[direction]

                    if nx != catcher[0] or ny != catcher[1]:
                        new_runners[nx][ny].append(direction)
                    else:
                        new_runners[x][y].append(direction)
            #내가 틀렸던 부분
            elif runners[x][y]:
                while(runners[x][y]):
                    new_runners[x][y].append(runners[x][y].pop())

    runners = deepcopy(new_runners)

turn = 0
ans = 0
catcher_d = 3

while(True):
    for jump in range(1, N):
        for _ in range(2 if jump < N - 1 else 3):
            for i in range(jump):
                turn += 1
                runners_run()

                x, y = catcher

                nx, ny = x + dx[catcher_d], y + dy[catcher_d]
                catcher[0], catcher[1] = nx, ny

                if i == jump - 1: 
                    if nx == 0 and ny == 0: catcher_d = 1
                    else: catcher_d = (catcher_d + 1) % 4

                for j in range(3):
                    cx, cy = catcher[0] + dx[catcher_d] * j, catcher[1] + dy[catcher_d] * j
                    if 0 <= cx < N and 0 <= cy < N and trees[cx][cy] == 0:
                        if runners[cx][cy]:
                            ans += turn * len(runners[cx][cy])
                            runners[cx][cy] = []

                if turn == K:
                    print(ans)
                    exit(0)

    for jump in range(N-1, 0, -1):
        for _ in range(2 if jump < N - 1 else 3):
            for i in range(jump):
                turn += 1
                runners_run()

                x, y = catcher

                nx, ny = x + dx[catcher_d], y + dy[catcher_d]

                catcher[0], catcher[1] = nx, ny

                if i == jump - 1: 
                    if nx == N//2 and ny == N//2: catcher_d = 3
                    else: catcher_d = catcher_d - 1 if catcher_d > 0 else 3

                for j in range(3):
                    cx, cy = catcher[0] + dx[catcher_d] * j, catcher[1] + dy[catcher_d] * j
                    if 0 <= cx < N and 0 <= cy < N and trees[cx][cy] == 0:
                        if runners[cx][cy]:
                            ans += turn * len(runners[cx][cy])
                            runners[cx][cy] = []

                if turn == K:
                    print(ans)
                    exit(0)
