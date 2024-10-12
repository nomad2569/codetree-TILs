from collections import deque

R, C, K = list(map(int, input().split()))

faries = []

for _ in range(K):
    sc, outlet = list(map(int, input().split()))
    faries.append((sc - 1, outlet))

forest = [
    [0 for _ in range(C)]
    for __ in range(R + 2)
]

ret = 0

dys = [-1, 0, 1, 0, 0]
dxs = [0, 1, 0, -1, 0]


def is_available(y, x) -> bool:
    if y < 0 or y >= R + 2 or x < 0 or x >= C:
        return False

    return True


def is_next_golam_available(center_y: int, center_x: int, direction: int) -> bool:
    global forest

    ds = []

    # 동쪽
    if direction == 1:
        ds = [(-1, 1), (0, 2), (1, 1)]
    elif direction == 2:
        ds = [(1, 1), (2, 0), (1, -1)]
    elif direction == 3:
        ds = [(-1, -1), (0, -2), (1, -1)]

    for dy, dx in ds:
        ny, nx = center_y + dy, center_x + dx

        if not is_available(ny, nx):
            return False

        if forest[ny][nx] != 0:
            return False

    return True


def gen_golam_coords(center_y: int, center_x: int):
    for dy, dx in zip(dys, dxs):
        yield center_y + dy, center_x + dx


def reset_golam(cy, cx):
    global forest

    for golam_y, golam_x in gen_golam_coords(cy, cx):
        if not is_available(golam_y, golam_x):
            continue

        forest[golam_y][golam_x] = 0


def move_golam(cy, cx, ny, nx, v):
    global forest

    reset_golam(cy, cx)

    for golam_y, golam_x in gen_golam_coords(ny, nx):
        if not is_available(golam_y, golam_x):
            continue

        if golam_y < 2:
            continue

        forest[golam_y][golam_x] = v

    return ny, nx


def rotate_outlet_clock_wise(outlet_dir: int) -> int:
    return (outlet_dir + 1) % 4


def rotate_outlet_reverse_clock_wise(outlet_dir: int) -> int:
    return (outlet_dir + 3) % 4


def reset_forest():
    global forest

    for y in range(R + 2):
        for x in range(C):
            forest[y][x] = 0


for idx, (start_column, outlet_dir) in enumerate(faries):
    value = idx + 1
    # print("시작", "start_c", start_column, "outlet_dir", outlet_dir, value)

    center_y, center_x = 0, start_column

    # Phase 1. 골렘을 최대한 아래로 내려보낸다.
    while True:
        reset_golam(center_y, center_x)
        # 1. 아래로 내려간다.
        if is_next_golam_available(center_y, center_x, 2):
            center_y, center_x = move_golam(center_y, center_x, center_y + 1, center_x, value)
            continue

        # 2. 서쪽으로 한 칸, 아래로 한 칸 내려간다.
        if is_next_golam_available(center_y, center_x, 3) and \
                is_next_golam_available(center_y, center_x - 1, 2):
            center_y, center_x = move_golam(center_y, center_x, center_y + 1, center_x - 1, value)
            outlet_dir = rotate_outlet_reverse_clock_wise(outlet_dir)
            continue

        # 3. 동쪽으로 한 칸, 아래로 한 칸 내려간다.
        if is_next_golam_available(center_y, center_x, 1) and \
                is_next_golam_available(center_y, center_x + 1, 2):
            center_y, center_x = move_golam(center_y, center_x, center_y + 1, center_x + 1, value)
            outlet_dir = rotate_outlet_clock_wise(outlet_dir)
            continue

        # 더 이상 갈 수 없으므로 골렘의 이동을 멈춘다.
        # print("move end")
        move_golam(center_y, center_x, center_y, center_x, value)
        break

    # print("move result", center_y, center_x)

    # 최대한 내려갔는데도, 중심이 3보다 작다면 reset
    if center_y < 3:
        # print("reset\n")
        # print(*forest, sep="\n", end="\n\n")
        reset_forest()
        continue


    # Phase 2. 골렘 내의 정령을 이동 시킨다.
    # 출구에서 시작해서, 모든 연결요소를 탐색한다. 그때의 최대 행 값을 구하자.
    def find_maximum_row(y, x) -> int:
        global forest, R, C

        visited = [
            [False for _ in range(C)]
            for __ in range(R + 2)
        ]

        q = deque([(y, x)])
        visited[y][x] = True

        max_ret = -1

        while q:
            cy, cx = q.popleft()

            max_ret = max(max_ret, cy)

            for dy, dx in zip(dys[:4], dxs[:4]):
                ny, nx = cy + dy, cx + dx

                if not is_available(ny, nx):
                    continue

                if visited[ny][nx]:
                    continue

                if forest[ny][nx] == 0:
                    continue

                # 1. 같은 골렘 내에서 움직일 때
                # 2. 다른 골렘으로 나갈 때
                if abs(forest[ny][nx]) == abs(forest[cy][cx]) or forest[cy][cx] < 0:
                    q.append(
                        (ny, nx)
                    )

                    visited[ny][nx] = True

        return max_ret

    outlet_y, outlet_x = center_y + dys[outlet_dir], center_x + dxs[outlet_dir]
    forest[outlet_y][outlet_x] = -value

    max_row = max(center_y + 1, find_maximum_row(outlet_y, outlet_x))

    # print("도착", (center_y, center_x, outlet_dir), "max_row", max_row - 1, end="\n\n")

    # print(*forest, sep="\n", end="\n\n")

    ret += (max_row - 1)

print(ret)