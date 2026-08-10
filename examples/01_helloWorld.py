import csleng

def main():

    WIDTH = csleng.WIDTH // 2 - 5
    HEIGHT = csleng.HEIGHT // 2
    KEYS = csleng.Keys
    COLOR = csleng.Color

    while True:
        csleng.clearBuffer()

        if csleng.isKeyPressed(KEYS.ESCAPE):
            break

        csleng.renderColorStr(WIDTH, HEIGHT, "Hello World!", COLOR.LIGHT_GREEN)
        csleng.renderColorStr(WIDTH - 3, HEIGHT + 1, "Press ESC to exit...", COLOR.GREY)

        csleng.renderConsoleFrame()
        csleng.limitFPS(60)

if __name__ == "__main__":
    csleng.start(main)