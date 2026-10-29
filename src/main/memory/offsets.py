"""Wardogs memory offsets — update per game patch.

Bump OFFSETS_VERSION whenever these change so users can tell which build
they're running against.
"""
OFFSETS_VERSION = "2026.02.14"

OFFSETS: dict[str, int] = {
    "local_player": 0x02F14C88,
    "entity_list": 0x02F3A900,
    "entity_count": 0x02F3A8F0,
    "view_matrix": 0x02F1B2C0,
    "camera_pos": 0x02F1B2A0,
    "team_id": 0x1B8,
    "health": 0x2A0,
    "position": 0x2C4,
    "bone_head": 0x3E0,
    "bone_chest": 0x3D8,
    "name": 0x120,
}

BONE_CHAIN = ("head", "neck", "chest", "pelvis")