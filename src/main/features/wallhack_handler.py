"""Wallhack — dumps render-pass transparency overrides."""
from __future__ import annotations

from loguru import logger

from src.main.ipc.bus import IpcBus
from src.main.process.wardogs_attach import WardogsProcess
from src.shared.contracts import WallhackConfig


class WallhackHandler:
    name = "wallhack"

    def __init__(self, cfg: WallhackConfig, proc: WardogsProcess, bus: IpcBus) -> None:
        self.cfg = cfg
        self.proc = proc
        self.bus = bus
        self._patched: list[int] = []

    def mount(self) -> None:
        if not self.cfg.enabled:
            return
        logger.info("wallhack active | transparency={}", self.cfg.transparency)
        # placeholder: real impl patches material transparency floats
        self.bus.publish("wallhack.state", {"enabled": True})

    def unmount(self) -> None:
        for addr in self._patched:
            logger.debug("would restore 0x{:x}", addr)
        self._patched.clear()