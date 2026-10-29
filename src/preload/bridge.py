"""Bridge between the Python core and the renderer UI.

Exposes a narrow, typed surface — the renderer never touches the memory
reader directly.
"""
from __future__ import annotations

from typing import Any, Callable

from src.main.ipc.bus import IpcBus


class PreloadBridge:
    def __init__(self, bus: IpcBus) -> None:
        self._bus = bus
        self._handlers: dict[str, Callable[[Any], None]] = {}

    def on(self, topic: str, fn: Callable[[Any], None]) -> None:
        self._bus.subscribe(topic, fn)
        self._handlers[topic] = fn

    def emit(self, topic: str, payload: Any) -> None:
        self._bus.publish(topic, payload)

    def expose(self) -> dict[str, Any]:
        return {
            "toggleAimbot": lambda on: self.emit("aimbot.toggle", {"on": on}),
            "toggleEsp": lambda on: self.emit("esp.toggle", {"on": on}),
            "setFov": lambda v: self.emit("aimbot.fov", {"value": v}),
            "getState": lambda: self.emit("state.request", {}),
        }