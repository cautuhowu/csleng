import os
import ctypes
import sys
import time
from typing import Optional, Callable, List

_stdoutHandle  : Optional[int]    = None
_screenBuffer  : List[List[List]] = []
_lastFrameTime : float            = 0.0
WIDTH          : int              = 79
HEIGHT         : int              = 24

class COORD(ctypes.Structure):
    """Win32 API structure defining the coordinates of a character cell in a console screen buffer."""
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class ConsoleCursorInfo(ctypes.Structure):
    """Win32 API structure containing information about the console's cursor size and visibility."""
    _fields_ = [("dwSize", ctypes.c_ulong), ("bVisible", ctypes.c_bool)]

class Color:
    """Win32 API color from 0-15."""
    # FOREGROUND
    BLACK         : int = 0x00 # 0
    BLUE          : int = 0x01 # 1
    GREEN         : int = 0x02 # 2
    CYAN          : int = 0x03 # 3
    RED           : int = 0x04 # 4
    MAGENTA       : int = 0x05 # 5
    YELLOW        : int = 0x06 # 6
    WHITE         : int = 0x07 # 7
    GREY          : int = 0x08 # 8

    # FOREGROUND INTENSITY
    LIGHT_BLUE    : int = 0x09 # 9
    LIGHT_GREEN   : int = 0x0A # 10
    LIGHT_CYAN    : int = 0x0B # 11
    LIGHT_RED     : int = 0x0C # 12
    LIGHT_MAGENTA : int = 0x0D # 13
    LIGHT_YELLOW  : int = 0x0E # 14
    LIGHT_WHITE   : int = 0x0F # 15

def setup() -> int:
    """Initialize and configure the low-level Windows Console environment."""
    global _stdoutHandle, _screenBuffer

    _screenBuffer = [[[" ", Color.LIGHT_WHITE] for _ in (range(WIDTH))] for _ in (range(HEIGHT))]
    kernel32 = ctypes.windll.kernel32

    os.system("cls")

    kernel32.GetStdHandle.restype = ctypes.c_void_p;
    STD_OUTPUT_HANDLE : int = -11;
    _stdoutHandle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE);

    cursorInfo: ConsoleCursorInfo = ConsoleCursorInfo(dwSize=20, bVisible=False);
    kernel32.SetConsoleCursorInfo(_stdoutHandle, ctypes.byref(cursorInfo));
    kernel32.SetConsoleTextAttribute(_stdoutHandle, Color.LIGHT_WHITE);

    return _stdoutHandle;

def clearBuffer() -> None:
    """Flush the off-screen double buffer by resetting all elements to blank space characters."""
    global _screenBuffer
    _screenBuffer = [[[" ", Color.LIGHT_WHITE] for _ in (range(WIDTH))] for _ in (range(HEIGHT))]

def renderConsoleFrame() -> None:
    """Commit the off-screen buffer using pure Windows API."""
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleCursorPosition(_stdoutHandle, COORD(0, 0))

    currentColor = -1

    for y in range(HEIGHT):
        rowStr = ""
        for x in range(WIDTH):
            char, color = _screenBuffer[y][x]
            if (color != currentColor):
                if (rowStr):
                    kernel32.WriteConsoleW(_stdoutHandle, rowStr, len(rowStr), None, None)
                    rowStr = ""
                kernel32.SetConsoleTextAttribute(_stdoutHandle, color)
                currentColor = color
            rowStr += char

        if (rowStr):
            kernel32.WriteConsoleW(_stdoutHandle, rowStr, len(rowStr), None, None)

        kernel32.WriteConsoleW(_stdoutHandle, "\n", 1, None, None)
    kernel32.SetConsoleTextAttribute(_stdoutHandle, Color.LIGHT_WHITE)

def moveCursor(x: int, y: int) -> None:
    """Move the console cursor to the specified (x, y) coordinates."""
    ctypes.windll.kernel32.SetConsoleCursorPosition(_stdoutHandle, COORD(x, y));

def setColor(colorCode: int) -> None:
    """Set the text attribute of the console."""
    ctypes.windll.kernel32.SetConsoleTextAttribute(_stdoutHandle, colorCode);

def renderPixel(x: int, y: int, char: str) -> None:
    """Write a single character 'pixel' to the off-screen double buffer if within boundary constraints."""
    if (0 <= x < WIDTH and 0 <= y < HEIGHT):
        _screenBuffer[y][x][0] = char
        _screenBuffer[y][x][1] = 15

def renderStr(x: int, y: int, string: str) -> None:
    """Write a horizontal sequence of characters into the off-screen double buffer at the target position."""
    for i, char in (enumerate(string)):
        renderPixel(x + i, y, char)

def renderColorStr(x: int, y: int, string: str, colorCode: int) -> None:
    """Write a colored string into the off-screen double buffer at the target position."""
    for i, char in (enumerate(string)):
        targetX = x + i
        if (0 <= targetX < WIDTH and 0 <= y < HEIGHT):
            _screenBuffer[y][targetX][0] = char
            _screenBuffer[y][targetX][1] = colorCode

def exit(exitCode: int = 0) -> None:
    """Clean up resources and terminate the application."""
    sys.exit(exitCode);

def start(userMainFunction: Callable[[], int]) -> None:
    """Bootstraps the engine, executes the user's main, and handles safe exit."""
    global _lastFrameTime

    try:
        setup();
        _lastFrameTime = time.perf_counter()
        status = userMainFunction();
        exit(status);
    except Exception as err:
        sys.stderr.write(str(err));
        exit(1);

def limitFPS(targetFPS: int) -> None:
    """Calculates game logic execution time and caps the framerate accurately."""
    global _lastFrameTime
    currentTime = time.perf_counter()

    if (_lastFrameTime == 0.0):
        _lastFrameTime = currentTime
        return

    frameTime = 1.0 / targetFPS
    elapsedTime = currentTime - _lastFrameTime
    sleepTime = frameTime - elapsedTime

    if (sleepTime > 0):
        time.sleep(sleepTime)
        _lastFrameTime += frameTime
    else:
        _lastFrameTime = time.perf_counter()

from .input import *
from .audio import *