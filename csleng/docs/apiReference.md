# Csleng API Reference

## System

### WIDTH - variable

The width of the screen.

- **Type:** `int`
- **Value:** `79`

### HEIGHT - variable

The height of the screen.

- **Type:** `int`
- **Value:** `24`

### Color - class

Win32 API foreground color constants ranging from `0` to `15`.

- **Type:** `class`
- **Constants:**
  - Standard: `BLACK`, `BLUE`, `GREEN`, `CYAN`, `RED`, `MAGENTA`, `YELLOW`, `WHITE`, `GREY`
  - High Intensity: `LIGHT_BLUE`, `LIGHT_GREEN`, `LIGHT_CYAN`, `LIGHT_RED`, `LIGHT_MAGENTA`, `LIGHT_YELLOW`, `LIGHT_WHITE`

### setup() - function

Initializes and configures the low-level Windows console environment (hides cursor, creates buffer).

- **Parameters:** None
- **Returns:** `int` - The stdout handle ID.

### clearBuffer() - function

Flushes the off-screen double buffer by resetting all elements to blank space characters.

- **Parameters:** None
- **Returns:** `None`

### moveCursor(x, y) - function

Moves the console cursor to the specified coordinates.

- **Parameters:**
  - `x` (*int*) - Column index.
  - `y` (*int*) - Row index.
- **Returns:** `None`

### start(userMainFunction) - function

Bootstraps the engine, executes the user's main function, and handles safe exit.

- **Parameters:**
  - `userMainFunction` (*Callable[[], int]*) - Entry point function returning an exit code.
- **Returns:** `None`

### exit(exitCode) - function

Cleans up resources and terminates the application.

- **Parameters:**
  - `exitCode` (*int*, optional) - Exit status code. Defaults to `0`.
- **Returns:** `None`

---

## Time

### limitFPS(targetFPS) - function

Calculates game logic execution time and caps the framerate accurately.

- **Parameters:**
  - `targetFPS` (*int*) - Target frames per second.
- **Returns:** `None`

---

## Graphics

### renderPixel(x, y, char) - function

Writes a single character "pixel" to the off-screen double buffer if within boundary constraints.

- **Parameters:**
  - `x` (*int*) - X coordinate.
  - `y` (*int*) - Y coordinate.
  - `char` (*str*) - Single character string.
- **Returns:** `None`

### renderStr(x, y, string) - function

Writes a horizontal sequence of characters into the off-screen double buffer at the target position.

- **Parameters:**
  - `x` (*int*) - Starting X coordinate.
  - `y` (*int*) - Y coordinate.
  - `string` (*str*) - String to render.
- **Returns:** `None`

### renderColorStr(x, y, string, colorCode) - function

Writes a colored string into the off-screen double buffer at the target position.

- **Parameters:**
  - `x` (*int*) - Starting X coordinate.
  - `y` (*int*) - Y coordinate.
  - `string` (*str*) - String to render.
  - `colorCode` (*int*) - Color constant from `Color` class.
- **Returns:** `None`

### setColor(colorCode) - function

Sets the default text attribute of the console.

- **Parameters:**
  - `colorCode` (*int*) - Color code from 0 to 15.
- **Returns:** `None`

### renderConsoleFrame() - function

Commits the off-screen buffer to the console screen using pure Win32 API calls.

- **Parameters:** None
- **Returns:** `None`

---

## Input (`csleng.input`)

### isKeyPressed(vkCode) - function

Checks real-time key press and hold status via Windows API.

- **Parameters:**
  - `vkCode` (*int*) - Virtual key code (e.g., `Keys.SPACE`, `Keys.A`).
- **Returns:** `bool` - `True` if the key is currently pressed down, `False` otherwise.

### Keys - class

A frozen dataclass containing standard Virtual Keycodes.

- **Type:** `dataclass`
- **Fields:**
  - **Directional:** `UP`, `DOWN`, `LEFT`, `RIGHT`
  - **System:** `ESCAPE`, `ENTER`, `SPACE`, `BACKSPACE`, `TAB`, `SHIFT`, `CONTROL`, `ALT`, `PAUSE`, `CAPSLOCK`
  - **Navigation:** `PRIOR`, `NEXT`, `END`, `HOME`, `SELECT`, `PRINT`, `EXECUTE`, `SNAPSHOT`, `INSERT`, `DELETE`, `HELP`
  - **Alphabet:** `A` through `Z`
  - **Number Row:** `NUM_0` through `NUM_9`
  - **Numpad:** `Numpad.NUM_0`–`9`, `MULTIPLY`, `ADD`, `SEPARATOR`, `SUBTRACT`, `DECIMAL`, `DIVIDE`
  - **Function Keys:** `F1` through `F12`
  - **OEM Punctuation:** `PLUS`, `COMMA`, `MINUS`, `PERIOD`, `OEM_1`–`7`

---

## Audio (`csleng.audio`)

### beep(frequency, durationMs) - function

Generates an asynchronous motherboard beep without freezing the application loop.

- **Parameters:**
  - `frequency` (*int*) - Tone frequency in Hertz.
  - `durationMs` (*int*) - Duration in milliseconds.
- **Returns:** `None`

### playAudio(filePath, alias, loop) - function

Asynchronously plays audio files (MP3, WAV, etc.) via Windows MCI driver.

- **Parameters:**
  - `filePath` (*str*) - Path to the audio file.
  - `alias` (*str*, optional) - Unique identifier for track management. Defaults to `"_bgMusic"`.
  - `loop` (*bool*, optional) - Loop infinitely if `True`. Defaults to `False`.
- **Returns:** `None`

### stopAudio(alias) - function

Immediately stops a specific audio track using its alias.

- **Parameters:**
  - `alias` (*str*, optional) - Identifier of the track. Defaults to `"_bgMusic"`.
- **Returns:** `None`

### pauseAudio(alias) - function

Pauses the current audio playback for a given track.

- **Parameters:**
  - `alias` (*str*, optional) - Identifier of the track. Defaults to `"_bgMusic"`.
- **Returns:** `None`

### resumeAudio(alias) - function

Resumes playback of the audio track from the exact point it was paused.

- **Parameters:**
  - `alias` (*str*, optional) - Identifier of the track. Defaults to `"_bgMusic"`.
- **Returns:** `None`

### stopAllAudio() - function

Stops and terminates all audio playbacks currently managed by MCI.

- **Parameters:** None
- **Returns:** `None`