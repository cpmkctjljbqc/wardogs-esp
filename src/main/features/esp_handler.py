"""ESP — box, skeleton, health bars, name tags."""
from __future__ import annotations

from loguru import logger

from src.main.memory.offsets import OFFSETS
from src.main.ipc.bus import IpcBus
from src.main.process.wardogs_attach import WardogsProcess
from src.shared.contracts import EspConfig
from src.shared.math_utils import world_to_screen


class EspHandler:
    name = "esp"

    def __init__(self, cfg: EspConfig, proc: WardogsProcess, bus: IpcBus) -> None:
        self.cfg = cfg
        self.proc = proc
        self.bus = bus
        self._running = False

    def mount(self) -> None:
        self._running = True
        logger.info("esp active | box={} skel={} max_dist={}",
                    self.cfg.box, self.cfg.skeleton, self.cfg.max_distance)

    def _build_overlay_payload(self) -> list[dict]:
        out: list[dict] = []
        if self.proc.info is None:
            return out
        view = self.proc.info.base + OFFSETS["view_matrix"]
        for ent in self._iter_enemies():
            pos = self.proc.read_vec3(ent + OFFSETS["position"])
            head = self.proc.read_vec3(ent + OFFSETS["bone_head"])
            screen = world_to_screen(pos, view)
            screen_head = world_to_screen(head, view)
            if screen is None or screen_head is None:
                continue
            out.append({
                "box": self.cfg.box,
                "skeleton": self.cfg.skeleton,
                "health": self.proc._pm.read_int(ent + OFFSETS["health"]) if self.proc._pm else 0,
                "head_y": screen_head[1],
                "feet_y": screen[1],
            })
        return out

    def _iter_enemies(self):
        return []

    def tick(self) -> None:
        if not self._running:
            return
        self.bus.publish("esp.frame", self._build_overlay_payload())

    def unmount(self) -> None:
        self._running = False