"""Renderer entry — mounts the overlay UI and listens to core events."""
from __future__ import annotations

import tkinter as tk

from src.preload.bridge import PreloadBridge
from src.renderer.src.components.esp_overlay import EspOverlay
from src.renderer.src.components.control_panel import ControlPanel


class RendererApp:
    def __init__(self, bridge: PreloadBridge) -> None:
        self.bridge = bridge
        self.root = tk.Tk()
        self.root.title("wardogs-esp")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.esp = EspOverlay(self.root)
        self.panel = ControlPanel(self.root, bridge)

    def run(self) -> None:
        self.bridge.on("esp.frame", self.esp.render_frame)
        self.bridge.on("radar.blips", self.esp.render_radar)
        self.root.mainloop()