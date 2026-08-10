import random
from typing import List, Dict
import csleng

BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 20
START_X: int = 34
START_Y: int = 2

SHAPES: List[List[List[int]]] = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS: List[int] = [
    csleng.Color.LIGHT_CYAN,
    csleng.Color.LIGHT_MAGENTA,
    csleng.Color.LIGHT_YELLOW,
    csleng.Color.LIGHT_BLUE,
    csleng.Color.LIGHT_WHITE,
    csleng.Color.LIGHT_GREEN,
    csleng.Color.LIGHT_RED
]

board: List[List[int]] = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
currentShape: List[List[int]] = []
currentColor: int = 0
currentX: int = 0
currentY: int = 0
score: int = 0
gameOver: bool = False
fallCounter: int = 0
fallSpeed: int = 10

keyStates: Dict[int, bool] = {
    csleng.Keys.LEFT: False,
    csleng.Keys.RIGHT: False,
    csleng.Keys.UP: False,
    csleng.Keys.DOWN: False
}

def checkKeyPress(keyCode: int) -> bool:
    global keyStates
    isDown: bool = csleng.isKeyPressed(keyCode)
    if isDown and not keyStates[keyCode]:
        keyStates[keyCode] = True
        return True
    if not isDown:
        keyStates[keyCode] = False
    return False

def createNewPiece() -> None:
    global currentShape, currentColor, currentX, currentY, gameOver
    randomIndex: int = random.randint(0, len(SHAPES) - 1)
    currentShape = SHAPES[randomIndex]
    currentColor = COLORS[randomIndex]
    currentX = BOARD_WIDTH // 2 - len(currentShape[0]) // 2
    currentY = 0
    if checkCollision(currentX, currentY, currentShape):
        gameOver = True

def checkCollision(offsetX: int, offsetY: int, shape: List[List[int]]) -> bool:
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                boardX: int = offsetX + x
                boardY: int = offsetY + y
                if boardX < 0 or boardX >= BOARD_WIDTH or boardY >= BOARD_HEIGHT:
                    return True
                if boardY >= 0 and board[boardY][boardX]:
                    return True
    return False

def lockPiece() -> None:
    global score
    for y, row in enumerate(currentShape):
        for x, cell in enumerate(row):
            if cell and currentY + y >= 0:
                board[currentY + y][currentX + x] = currentColor
    
    clearedRows: int = 0
    y: int = BOARD_HEIGHT - 1
    while y >= 0:
        if all(board[y]):
            clearedRows += 1
            del board[y]
            board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        else:
            y -= 1
            
    if clearedRows > 0:
        score += (clearedRows * 100)
    createNewPiece()

def rotatePiece() -> None:
    global currentShape
    rows: int = len(currentShape)
    cols: int = len(currentShape[0])
    rotated: List[List[int]] = [[currentShape[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]
    if not checkCollision(currentX, currentY, rotated):
        currentShape = rotated

def handleInput() -> None:
    global currentX, currentY
    if checkKeyPress(csleng.Keys.LEFT):
        if not checkCollision(currentX - 1, currentY, currentShape):
            currentX -= 1
    if checkKeyPress(csleng.Keys.RIGHT):
        if not checkCollision(currentX + 1, currentY, currentShape):
            currentX += 1
    if checkKeyPress(csleng.Keys.UP):
        rotatePiece()
    if csleng.isKeyPressed(csleng.Keys.DOWN):
        if not checkCollision(currentX, currentY + 1, currentShape):
            currentY += 1

def drawGame() -> None:
    csleng.clearBuffer()
    
    for y in range(BOARD_HEIGHT + 2):
        csleng.renderColorStr(START_X - 1, START_Y - 1 + y, "|", csleng.Color.GREY)
        csleng.renderColorStr(START_X + BOARD_WIDTH * 2, START_Y - 1 + y, "|", csleng.Color.GREY)
    
    for x in range(BOARD_WIDTH * 2 + 1):
        csleng.renderColorStr(START_X - 1 + x, START_Y + BOARD_HEIGHT, "-", csleng.Color.GREY)

    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x]:
                csleng.renderColorStr(START_X + x * 2, START_Y + y, "[]", board[y][x])

    if not gameOver:
        for y, row in enumerate(currentShape):
            for x, cell in enumerate(row):
                if cell and currentY + y >= 0:
                    csleng.renderColorStr(START_X + (currentX + x) * 2, START_Y + currentY + y, "[]", currentColor)

    csleng.renderColorStr(10, 5, "TETRIS GAME", csleng.Color.LIGHT_GREEN)
    csleng.renderColorStr(10, 7, f"SCORE: {score}", csleng.Color.LIGHT_YELLOW)
    csleng.renderColorStr(10, 10, "CONTROLS:", csleng.Color.LIGHT_WHITE)
    csleng.renderColorStr(10, 11, "Left/Right: Move", csleng.Color.GREY)
    csleng.renderColorStr(10, 12, "Up: Rotate", csleng.Color.GREY)
    csleng.renderColorStr(10, 13, "Down: Drop Fast", csleng.Color.GREY)
    csleng.renderColorStr(10, 15, "ESC: Quit", csleng.Color.GREY)

    if gameOver:
        csleng.renderColorStr(START_X + 4, START_Y + 9, "GAME OVER", csleng.Color.LIGHT_RED)

    csleng.renderConsoleFrame()

def main() -> int:
    global fallCounter, currentX, currentY
    createNewPiece()
    
    while True:
        if csleng.isKeyPressed(csleng.Keys.ESCAPE):
            break
            
        if not gameOver:
            handleInput()
            fallCounter += 1
            if fallCounter >= fallSpeed:
                if not checkCollision(currentX, currentY + 1, currentShape):
                    currentY += 1
                else:
                    lockPiece()
                fallCounter = 0
                
        drawGame()
        csleng.limitFPS(30)
        
    return 0

if __name__ == "__main__":
    csleng.start(main)