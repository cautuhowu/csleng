import csleng

currentGrid = [[0 for _ in range(csleng.WIDTH)] for _ in range(csleng.HEIGHT)]
nextGrid = [[0 for _ in range(csleng.WIDTH)] for _ in range(csleng.HEIGHT)]

def countNeighbors(x, y):
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            nx = (x + i) % csleng.WIDTH
            ny = (y + j) % csleng.HEIGHT
            count += currentGrid[ny][nx]
    return count

def _setup():
    global currentGrid

    gunCoords = [
        (5,1), (5,2), (6,1), (6,2), (5,11), (6,11), (7,11), (4,12), (8,12),
        (3,13), (9,13), (3,14), (9,14), (6,15), (4,16), (8,16), (5,17), (6,17),
        (7,17), (6,18), (3,21), (4,21), (5,21), (3,22), (4,22), (5,22), (2,23),
        (6,23), (1,25), (2,25), (6,25), (7,25), (3,35), (4,35), (3,36), (4,36)
    ]
    for gy, gx in gunCoords:
        if gy < csleng.HEIGHT and gx < csleng.WIDTH:
            currentGrid[gy][gx] = 1

def main():
    global currentGrid, nextGrid
    
    _setup()

    while True:
        if csleng.isKeyPressed(csleng.Keys.ESCAPE):
            break

        csleng.clearBuffer()

        for y in range(csleng.HEIGHT):
            for x in range(csleng.WIDTH):
                neighbors = countNeighbors(x, y)
                state = currentGrid[y][x]

                if state == 1:
                    if neighbors in [2, 3]:
                        nextGrid[y][x] = 1
                    else:
                        nextGrid[y][x] = 0
                else:
                    if neighbors == 3:
                        nextGrid[y][x] = 1
                    else:
                        nextGrid[y][x] = 0

        for y in range(csleng.HEIGHT):
            for x in range(csleng.WIDTH):
                currentGrid[y][x] = nextGrid[y][x]

                if currentGrid[y][x] == 1:
                    csleng.renderColorStr(x, y, "O", csleng.Color.LIGHT_GREEN)

        csleng.renderConsoleFrame()
        csleng.limitFPS(20)

    return 0

if __name__ == "__main__":
    csleng.start(main)