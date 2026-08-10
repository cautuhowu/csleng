import ctypes
from dataclasses import dataclass

def isKeyPressed(vkCode: int) -> bool:
    """Real-time key press and hold status checking via Windows API"""
    return (ctypes.windll.user32.GetAsyncKeyState(vkCode) & 0x8000) != 0

@dataclass(frozen=True)
class Keys:
    # DIRECTIONAL / NAVIGATION KEYS
    UP      = 0x26
    DOWN    = 0x28
    LEFT    = 0x25
    RIGHT   = 0x27

    # SYSTEM / CONTROL KEYS
    ESCAPE    = 0x1B  # Esc
    ENTER     = 0x0D  # Enter / Return
    SPACE     = 0x20  # Spacebar
    BACKSPACE = 0x08  # Backspace
    TAB       = 0x09  # Tab
    SHIFT     = 0x10  # Shift
    CONTROL   = 0x11  # Ctrl
    ALT       = 0x12  # Alt
    PAUSE     = 0x13  # Pause
    CAPSLOCK  = 0x14  # Caps Lock

    # PAGE NAVIGATION KEYS
    PRIOR     = 0x21  # Page Up
    NEXT      = 0x22  # Page Down
    END       = 0x23  # End
    HOME      = 0x24  # Home
    SELECT    = 0x29  # Select key
    PRINT     = 0x2A  # Print key
    EXECUTE   = 0x2B  # Execute key
    SNAPSHOT  = 0x2C  # Print Screen
    INSERT    = 0x2D  # Insert
    DELETE    = 0x2E  # Delete
    HELP      = 0x2F  # Help key

    # ALPHABET KEYS
    A = 0x41; B = 0x42; C = 0x43; D = 0x44; E = 0x45; F = 0x46; G = 0x47;
    H = 0x48; I = 0x49; J = 0x4A; K = 0x4B; L = 0x4C; M = 0x4D; N = 0x4E;
    O = 0x4F; P = 0x50; Q = 0x51; R = 0x52; S = 0x53; T = 0x54; U = 0x55;
    V = 0x56; W = 0x57; X = 0x58; Y = 0x59; Z = 0x5A;

    # NUMPAD KEYS
    @dataclass(frozen=True)
    class Numpad:
        NUM_0 = 0x60; NUM_1 = 0x61; NUM_2 = 0x62; NUM_3 = 0x63;
        NUM_4 = 0x64; NUM_5 = 0x65; NUM_6 = 0x66; NUM_7 = 0x67;
        NUM_8 = 0x68; NUM_9 = 0x69;
        MULTIPLY = 0x6A  # *
        ADD      = 0x6B  # +
        SEPARATOR = 0x6C # Separator
        SUBTRACT = 0x6D  # -
        DECIMAL  = 0x6E  # .
        DIVIDE   = 0x6F  # /

    # FUNCTION KEYS
    F1 = 0x70; F2 = 0x71; F3 = 0x72; F4 = 0x73; F5 = 0x74; F6 = 0x75;
    F7 = 0x76; F8 = 0x77; F9 = 0x78; F10 = 0x79; F11 = 0x7A; F12 = 0x7B;

    # NUMBER ROW KEYS
    NUM_0 = 0x30; NUM_1 = 0x31; NUM_2 = 0x32; NUM_3 = 0x33; NUM_4 = 0x34;
    NUM_5 = 0x35; NUM_6 = 0x36; NUM_7 = 0x37; NUM_8 = 0x38; NUM_9 = 0x39;

    # OEM PUNCTUATION KEYS (Các phím ký tự đặc biệt)
    PLUS      = 0xBB  # (= / +)
    COMMA     = 0xBC  # (,)
    MINUS     = 0xBD  # (- / _)
    PERIOD    = 0xBE  # (.)
    OEM_1     = 0xBA  # (; / :)
    OEM_2     = 0xBF  # (/ / ?)
    OEM_3     = 0xC0  # (` / ~)
    OEM_4     = 0xDB  # ([ / {)
    OEM_5     = 0xDC  # (\ / |)
    OEM_6     = 0xDD  # (] / })
    OEM_7     = 0xDE  # (' / ")