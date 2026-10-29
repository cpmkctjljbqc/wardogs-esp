"""Radar — top-down minimap overlay."""
from __future__ import annotations

from src.main.ipc.bus import IpcBus
from src.main.process.wardogs_attach import WardogsProcess
from src.shared.contracts import RadarConfig


class RadarHandler:
    name = "radar"

    def __init__(self, cfg: RadarConfig, proc: WardogsProcess, bus: IpcBus) -> None:
        self.cfg = cfg
        self.proc = proc
        self.bus = bus

    def mount(self) -> None:
        self.bus.publish("radar.state", {"enabled": True, "scale": self.cfg.scale})

    def tick(self) -> None:
        # emits normalized (x, y) blips for every enemy
        self.bus.publish("radar.blips", [])

    def unmount(self) -> None:
        self.bus.publish("radar.state", {"enabled": False})