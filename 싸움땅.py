from sys import stdin
input = stdin.readline

N, M, K = map(int, input().split())
guns = [list(map(int, input().split())) for _ in range(N)]
guns_map = [[[] for _ in range(N)] for _ in range(N)]
player = [list(map(int, input().split())) for _ in range(M)]
player_map = [[0 for _ in range(N)] for _ in range(N)]
scores = [0 for _ in range(M)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
turn = 0

def move(pnum, chk):
    global player, player_map
    x, y, d, s, w = player[pnum - 1]

    if chk:#지고서 이동하는 것
        for _ in range(4):
            nx, ny = x + dx[d], y + dy[d]

            if 0 <= nx < N and 0 <= ny < N and player_map[nx][ny] == 0:
                x, y = nx, ny
                player_map[x][y] = pnum

                break
            else:
                d = (d + 1) % 4

        #총 선택 부분
        if w > 0: guns_map[x][y].append(w)

        if guns_map[x][y]:
            guns_map[x][y].sort()
            w = guns_map[x][y].pop()
    else:#처음에 이동하는 것
        if not (0 <= x + dx[d] < N and 0 <= y + dy[d] < N):
            if d < 2: d += 2
            else: d -= 2

        player_map[x][y] = 0
        x += dx[d]
        y += dy[d]

    player[pnum - 1] = [x, y, d, s, w]

    return

def utilMove(pnum):
    move(pnum, 0)

    x, y, d, s, w = player[pnum - 1]

    if player_map[x][y] > 0:
        oppnum = player_map[x][y]
        opx, opy, opd, ops, opw = player[oppnum - 1]

        if s + w > ops + opw or (s + w == ops + opw and s > ops):#움직인자가 이김
            scores[pnum - 1] += (s + w) - (ops + opw)

            if w > 0: 
                guns_map[x][y].append(w)
                player[pnum - 1][-1] = 0
            if opw > 0: 
                guns_map[x][y].append(opw)
                player[oppnum - 1][-1] = 0

            move(oppnum, 1)

            if guns_map[x][y]:
                guns_map[x][y].sort()
                w = guns_map[x][y].pop()

            player_map[x][y] = pnum
            player[pnum - 1] = [x, y, d, s, w]
        elif s + w < ops + opw or (s + w == ops + opw and s < ops):#기존의 자가 이김
            scores[oppnum - 1] += (ops + opw) - (s + w)

            if w > 0: 
                guns_map[x][y].append(w)
                player[pnum - 1][-1] = 0
            if opw > 0: 
                guns_map[x][y].append(opw)
                player[oppnum - 1][-1] = 0

            move(pnum, 1)

            if guns_map[x][y]:
                guns_map[x][y].sort()
                opw = guns_map[x][y].pop()

            player[oppnum - 1][-1] = opw
    else:#아무도 없음
        player_map[x][y] = pnum

        if w > 0: 
            guns_map[x][y].append(w)
            player[pnum - 1][-1] = 0

        if guns_map[x][y]:
            guns_map[x][y].sort()
            w = guns_map[x][y].pop()

        player[pnum - 1] = [x, y, d, s, w]

for i in range(M):
    player[i][0] -= 1
    player[i][1] -= 1
    player[i].append(0)
    player_map[player[i][0]][player[i][1]] = i + 1

for i in range(N):
    for j in range(N):
        if guns[i][j]:
            guns_map[i][j].append(guns[i][j])

while(turn < K):
    for i in range(1, M + 1):
        utilMove(i)

    turn += 1

print(" ".join(map(str, scores)))
