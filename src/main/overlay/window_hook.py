"""Overlay window hook — attaches a transparent click-through window
on top of the Wardogs render surface (Windows only).
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes

from loguru import logger

user32 = ctypes.WinDLL("user32", use_last_error=True)

WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOPMOST = 0x00000008
GWL_EXSTYLE = -20


class OverlayWindow:
    def __init__(self, title: str = "wardogs-esp-overlay") -> None:
        self.title = title
        self.hwnd: int | None = None

    def create(self) -> int:
        self.hwnd = user32.FindWindowW(None, self.title)
        if not self.hwnd:
            logger.warning("overlay hwnd not found; renderer must create it first")
            return 0
        style = user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(self.hwnd, GWL_EXSTYLE,
                              style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST)
        return self.hwnd

    def destroy(self) -> None:
        if self.hwnd:
            user32.DestroyWindow(self.hwnd)
            self.hwnd = None