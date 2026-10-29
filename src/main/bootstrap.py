"""Wardogs ESP — desktop bootstrap.

Creates the Qt/Electron-style shell, wires the IPC bus, and mounts the
feature registry. Everything downstream assumes this ran first.
"""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from src.main.ipc.bus import IpcBus
from src.main.process.wardogs_attach import WardogsProcess
from src.main.features.registry import FeatureRegistry
from src.shared.contracts import AppConfig
from src.shared.config_loader import load_config


def _setup_logging() -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(log_dir / "wardogs-esp.log", rotation="10 MB", level="DEBUG")


def main() -> int:
    _setup_logging()
    cfg: AppConfig = load_config(Path("config/toggles.default.yaml"))
    logger.info("wardogs-esp starting | aimbot={} esp={}", cfg.aimbot.enabled, cfg.esp.enabled)

    proc = WardogsProcess()
    if not proc.attach():
        logger.error("could not attach to Wardogs.exe — is the game running?")
        return 1

    bus = IpcBus()
    registry = FeatureRegistry(cfg, proc, bus)
    registry.mount_all()

    try:
        bus.run_forever()
    except KeyboardInterrupt:
        logger.info("shutdown requested")
    finally:
        registry.unmount_all()
        proc.detach()
    return 0


if __name__ == "__main__":
    sys.exit(main())