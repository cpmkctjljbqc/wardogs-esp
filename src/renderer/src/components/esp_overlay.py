"""Canvas-based ESP overlay — draws boxes, skeletons, health bars."""
from __future__ import annotations

import tkinter as tk
from typing import Any


class EspOverlay:
    def __init__(self, root: tk.Tk) -> None:
        self.canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self._tick = 0

    def _draw_box(self, x: int, y: int, w: int, h: int, color: str = "#00ff88") -> None:
        self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=1)

    def render_frame(self, entities: list[dict[str, Any]]) -> None:
        self.canvas.delete("all")
        for ent in entities:
            if ent.get("box"):
                self._draw_box(10, int(ent["head_y"]), 40, int(ent["feet_y"] - ent["head_y"]))
            if ent.get("skeleton"):
                self.canvas.create_line(30, ent["head_y"], 30, ent["feet_y"], fill="#ff3355")

    def render_radar(self, blips: list[tuple[float, float]]) -> None:
        self._tick += 1
        for bx, by in blips:
            self.canvas.create_oval(bx - 3, by - 3, bx + 3, by + 3, fill="#ffcc00")