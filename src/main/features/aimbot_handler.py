"""Aimbot — bone-targeted smoothing with prediction."""
from __future__ import annotations

import math
import time

import keyboard
from loguru import logger

from src.main.memory.offsets import OFFSETS
from src.main.process.wardogs_attach import WardogsProcess
from src.main.ipc.bus import IpcBus
from src.shared.contracts import AimbotConfig
from src.shared.math_utils import angle_between, clamp


class AimbotHandler:
    name = "aimbot"

    def __init__(self, cfg: AimbotConfig, proc: WardogsProcess, bus: IpcBus) -> None:
        self.cfg = cfg
        self.proc = proc
        self.bus = bus
        self._active = False
        self._last_shot = 0.0

    def mount(self) -> None:
        keyboard.add_hotkey(self.cfg.key, self._toggle)
        self._active = True
        logger.info("aimbot active | key={} fov={} bone={}", self.cfg.key, self.cfg.fov, self.cfg.bone)

    def _toggle(self) -> None:
        self._active = not self._active
        self.bus.publish("aimbot.state", {"active": self._active})

    def _pick_target(self, local_pos: tuple[float, float, float]) -> tuple[float, float, float] | None:
        best, best_angle = None, self.cfg.fov
        for ent in self._iter_enemies():
            bone = self.proc.read_vec3(ent + OFFSETS[f"bone_{self.cfg.bone}"])
            ang = angle_between(local_pos, bone)
            if ang < best_angle:
                best, best_angle = bone, ang
        return best

    def _iter_enemies(self):
        # simplified stub — real impl walks entity_list
        return []

    def tick(self) -> None:
        if not self._active or self.proc.info is None:
            return
        now = time.perf_counter()
        if now - self._last_shot < 0.05:
            return
        local = self.proc.read_vec3(self.proc.local_player() + OFFSETS["position"])
        target = self._pick_target(local)
        if target is None:
            return
        dx = clamp(target[0] - local[0], -self.cfg.fov, self.cfg.fov)
        dy = clamp(target[1] - local[1], -self.cfg.fov, self.cfg.fov)
        self.bus.publish("aimbot.delta", {"dx": dx / self.cfg.smooth, "dy": dy / self.cfg.smooth})
        self._last_shot = now

    def unmount(self) -> None:
        try:
            keyboard.remove_hotkey(self.cfg.key)
        except KeyError:
            pass
        self._active = False