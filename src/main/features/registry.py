"""Feature registry — mounts/unmounts every cheat module."""
from __future__ import annotations

from typing import Protocol

from loguru import logger

from src.main.ipc.bus import IpcBus
from src.main.process.wardogs_attach import WardogsProcess
from src.shared.contracts import AppConfig

from src.main.features.aimbot_handler import AimbotHandler
from src.main.features.esp_handler import EspHandler
from src.main.features.wallhack_handler import WallhackHandler
from src.main.features.radar_handler import RadarHandler


class Feature(Protocol):
    name: str
    def mount(self) -> None: ...
    def unmount(self) -> None: ...


class FeatureRegistry:
    def __init__(self, cfg: AppConfig, proc: WardogsProcess, bus: IpcBus) -> None:
        self.cfg = cfg
        self.proc = proc
        self.bus = bus
        self._mounted: list[Feature] = []

    def _build(self) -> list[Feature]:
        return [
            AimbotHandler(self.cfg.aimbot, self.proc, self.bus),
            EspHandler(self.cfg.esp, self.proc, self.bus),
            WallhackHandler(self.cfg.wallhack, self.proc, self.bus),
            RadarHandler(self.cfg.radar, self.proc, self.bus),
        ]

    def mount_all(self) -> None:
        for feat in self._build():
            if getattr(self.cfg, feat.name, None) and getattr(self.cfg, feat.name).enabled:
                feat.mount()
                self._mounted.append(feat)
                logger.debug("mounted feature {}", feat.name)

    def unmount_all(self) -> None:
        for feat in reversed(self._mounted):
            try:
                feat.unmount()
            except Exception as exc:  # noqa: BLE001
                logger.warning("unmount {} failed: {}", feat.name, exc)
        self._mounted.clear()