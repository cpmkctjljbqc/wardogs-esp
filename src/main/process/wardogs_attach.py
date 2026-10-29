"""Attach to the Wardogs game process and hand out a memory reader."""
from __future__ import annotations

from dataclasses import dataclass

import pymem
from loguru import logger

from src.main.memory.offsets import OFFSETS, OFFSETS_VERSION


@dataclass
class ProcessInfo:
    pid: int
    base: int
    module: str


class WardogsProcess:
    PROCESS_NAME = "Wardogs.exe"

    def __init__(self) -> None:
        self._pm: pymem.Pymem | None = None
        self.info: ProcessInfo | None = None

    def attach(self) -> bool:
        try:
            self._pm = pymem.Pymem(self.PROCESS_NAME)
            base = self._pm.base_address
            self.info = ProcessInfo(pid=self._pm.process_id, base=base, module=self.PROCESS_NAME)
            logger.info("attached to {} pid={} base=0x{:x} offsets={}",
                        self.PROCESS_NAME, self.info.pid, base, OFFSETS_VERSION)
            return True
        except pymem.exception.ProcessNotFound:
            return False

    def read_float(self, address: int) -> float:
        assert self._pm is not None
        return self._pm.read_float(address)

    def read_vec3(self, address: int) -> tuple[float, float, float]:
        assert self._pm is not None
        buf = self._pm.read_bytes(address, 12)
        import struct
        return struct.unpack("<fff", buf)

    def local_player(self) -> int:
        assert self._pm is not None
        return self._pm.read_int(self.info.base + OFFSETS["local_player"])

    def detach(self) -> None:
        self._pm = None
        self.info = None