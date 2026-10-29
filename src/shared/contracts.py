"""Shared dataclasses — the contract between core and renderer."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AimbotConfig:
    enabled: bool = True
    key: str = "F1"
    fov: float = 120.0
    smooth: float = 4.5
    bone: str = "head"
    prediction: bool = True


@dataclass
class EspConfig:
    enabled: bool = True
    key: str = "F2"
    box: bool = True
    skeleton: bool = True
    health_bar: bool = True
    name_tags: bool = True
    max_distance: int = 350
    team_filter: bool = True


@dataclass
class WallhackConfig:
    enabled: bool = False
    key: str = "F3"
    transparency: float = 0.35


@dataclass
class RadarConfig:
    enabled: bool = True
    key: str = "F4"
    scale: float = 1.0


@dataclass
class MiscConfig:
    no_recoil: bool = True
    no_flash: bool = False
    streamer_mode: bool = False


@dataclass
class AppConfig:
    aimbot: AimbotConfig = field(default_factory=AimbotConfig)
    esp: EspConfig = field(default_factory=EspConfig)
    wallhack: WallhackConfig = field(default_factory=WallhackConfig)
    radar: RadarConfig = field(default_factory=RadarConfig)
    misc: MiscConfig = field(default_factory=MiscConfig)