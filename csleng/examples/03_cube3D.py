import math
import csleng

VERTICES = [
    [-0.5, -0.5, -0.5], [ 0.5, -0.5, -0.5], [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5],
    [-0.5, -0.5,  0.5], [ 0.5, -0.5,  0.5], [ 0.5,  0.5,  0.5], [-0.5,  0.5,  0.5]
]

EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw(x0, y0, x1, y1, char="#", color=csleng.Color.LIGHT_CYAN):
    dX = abs(x1 - x0)
    dY = abs(y1 - y0)
    sX = 1 if x0 < x1 else -1
    sY = 1 if y0 < y1 else -1
    _err = dX - dY

    while True:
        csleng.renderColorStr(x0, y0, char, color)
        if x0 == x1 and y0 == y1:
            break
        _e2 = 2 * _err
        if _e2 > -dY:
            _err -= dY
            x0 += sX
        if _e2 < dX:
            _err += dX
            y0 += sY

def main():
    angleX = 0.0
    angleY = 0.0
    angleZ = 0.0

    FOV = 60 
    distance = 4.5

    while True:
        if csleng.isKeyPressed(csleng.Keys.ESCAPE):
            break

        csleng.clearBuffer()

        angleX += 0.03
        angleY += 0.04
        angleZ += 0.02

        projectedVertices = []

        for vertex in VERTICES:
            x, y, z = vertex[0], vertex[1], vertex[2]

            rad = angleX
            yNew = y * math.cos(rad) - z * math.sin(rad)
            zNew = y * math.sin(rad) + z * math.cos(rad)
            y, z = yNew, zNew

            rad = angleY
            xNew = x * math.cos(rad) + z * math.sin(rad)
            zNew = -x * math.sin(rad) + z * math.cos(rad)
            x, z = xNew, zNew

            rad = angleZ
            xNew = x * math.cos(rad) - y * math.sin(rad)
            yNew = x * math.sin(rad) + y * math.cos(rad)
            x, y = xNew, yNew

            z += distance

            screenX = int(csleng.WIDTH / 2 + (x * FOV / z) * 2.0) 
            screenY = int(csleng.HEIGHT / 2 + (y * FOV / z))

            projectedVertices.append((screenX, screenY))

        for edge in EDGES:
            p1 = projectedVertices[edge[0]]
            p2 = projectedVertices[edge[1]]

            draw(p1[0], p1[1], p2[0], p2[1], char="*", color=csleng.Color.LIGHT_GREEN)

        csleng.renderConsoleFrame()
        csleng.limitFPS(60)

    return 0

if __name__ == "__main__":
    csleng.start(main)