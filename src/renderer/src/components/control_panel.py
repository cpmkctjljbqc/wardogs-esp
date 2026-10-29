"""Control panel — toggles for aimbot / esp / wallhack / radar."""
from __future__ import annotations

import tkinter as tk

from src.preload.bridge import PreloadBridge


class ControlPanel:
    def __init__(self, root: tk.Tk, bridge: PreloadBridge) -> None:
        self.bridge = bridge
        frame = tk.Frame(root, bg="#111", padx=8, pady=8)
        frame.pack(side="right", anchor="ne")

        tk.Label(frame, text="WARDDOGS ESP", fg="#00ff88", bg="#111",
                 font=("Consolas", 12, "bold")).pack(anchor="w")

        self.aimbot_var = tk.BooleanVar(value=True)
        self.esp_var = tk.BooleanVar(value=True)
        self.wallhack_var = tk.BooleanVar(value=False)

        tk.Checkbutton(frame, text="Aimbot [F1]", variable=self.aimbot_var,
                       command=self._sync, bg="#111", fg="white",
                       selectcolor="#222").pack(anchor="w")
        tk.Checkbutton(frame, text="ESP [F2]", variable=self.esp_var,
                       command=self._sync, bg="#111", fg="white",
                       selectcolor="#222").pack(anchor="w")
        tk.Checkbutton(frame, text="Wallhack [F3]", variable=self.wallhack_var,
                       command=self._sync, bg="#111", fg="white",
                       selectcolor="#222").pack(anchor="w")

    def _sync(self) -> None:
        self.bridge.emit("aimbot.toggle", {"on": self.aimbot_var.get()})
        self.bridge.emit("esp.toggle", {"on": self.esp_var.get()})
        self.bridge.emit("wallhack.toggle", {"on": self.wallhack_var.get()})