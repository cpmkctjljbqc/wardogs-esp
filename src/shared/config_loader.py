"""YAML → AppConfig loader with sane defaults."""
from __future__ import annotations

from pathlib import Path

import yaml

from src.shared.contracts import (
    AimbotConfig, EspConfig, WallhackConfig, RadarConfig, MiscConfig, AppConfig,
)


def _section(data: dict, key: str) -> dict:
    return data.get(key, {}) or {}


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        return AppConfig()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig(
        aimbot=AimbotConfig(**_section(raw, "aimbot")),
        esp=EspConfig(**_section(raw, "esp")),
        wallhack=WallhackConfig(**_section(raw, "wallhack")),
        radar=RadarConfig(**_section(raw, "radar")),
        misc=MiscConfig(**_section(raw, "misc")),
    )