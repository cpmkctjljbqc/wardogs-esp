"""Math helpers — angle, clamp, world-to-screen."""
from __future__ import annotations

import math
from typing import Optional


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def angle_between(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    dist = math.sqrt(dx * dx + dy * dy + dz * dz)
    if dist < 1e-6:
        return 0.0
    return math.degrees(math.atan2(dy, dx))


def world_to_screen(
    world: tuple[float, float, float],
    view_matrix_addr: int,
) -> Optional[tuple[float, float]]:
    """Placeholder — real impl multiplies by the 4x4 view matrix."""
    x, y, _z = world
    if x == 0 and y == 0:
        return None
    return (x, y)
</｜｜DSML｜｜ parameter>
</invoke>