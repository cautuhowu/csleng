import ctypes
import threading
import time

kernel32 = ctypes.windll.kernel32
winmm = ctypes.windll.winmm

def beep(frequency: int, durationMs: int) -> None:
    """Asynchronous motherboard beep generation without freezing the application."""
    def __beep__():
        kernel32.Beep(frequency, durationMs)
    threading.Thread(target=__beep__, daemon=True).start()

def _send_mci_command(command: str) -> str:
    """Internal function for sending English command strings directly to the Windows Media Control Interface audio driver."""
    buffer = ctypes.create_unicode_buffer(256)
    winmm.mciSendStringW(command, buffer, 255, 0)
    return buffer.value

def playAudio(filePath: str, alias: str = "_bgMusic", loop: bool = False) -> None:
    """
    Asynchronously plays all audio formats.\n
    ___\n
    filePath: The path to the audio file.
    alias: A unique identifier assigned to the audio file for management purposes.
    loop: Set to True for infinite looping; False for a single playback.
    """
    def _playThread():
        targetAlias = alias

        # Avoiding alias conflicts with rapid sound effects playback
        if (not loop and alias == "_bgMusic"):
            targetAlias = f"sfx_{int(time.time() * 1000)}"

        _send_mci_command(f"close {targetAlias}")
        openCmd = f"open \"{filePath}\" type mpegvideo alias {targetAlias}"
        _send_mci_command(openCmd)

        if (loop):
            _send_mci_command(f"play {targetAlias} repeat")
        else:
            _send_mci_command(f"play {targetAlias}")

    threading.Thread(target=_playThread, daemon=True).start()

def stopAudio(alias: str = "_bgMusic") -> None:
    """Immediately stops a specific audio track using its alias."""
    _send_mci_command(f"stop {alias}")
    _send_mci_command(f"close {alias}")

def pauseAudio(alias: str = "_bgMusic") -> None:
    """Pauses the current audio playback."""
    _send_mci_command(f"pause {alias}")

def resumeAudio(alias: str = "_bgMusic") -> None:
    """Resumes playback of the audio track from the exact point it was paused."""
    _send_mci_command(f"resume {alias}")

def stopAllAudio():
    """Stops and terminates all audio playbacks currently managed by Windows Media Control Interface."""
    _send_mci_command("close all")