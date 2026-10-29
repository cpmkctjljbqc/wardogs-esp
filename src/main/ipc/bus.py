"""Lightweight IPC bus between the Python core and the renderer UI."""
from __future__ import annotations

import json
import queue
import threading
from typing import Callable, Any

from loguru import logger


class IpcBus:
    def __init__(self) -> None:
        self._subs: dict[str, list[Callable[[Any], None]]] = {}
        self._out = queue.Queue()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def subscribe(self, topic: str, fn: Callable[[Any], None]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload: Any) -> None:
        self._out.put({"topic": topic, "payload": payload})

    def _pump(self) -> None:
        while not self._stop.is_set():
            try:
                msg = self._out.get(timeout=0.2)
            except queue.Empty:
                continue
            for fn in self._subs.get(msg["topic"], []):
                try:
                    fn(msg["payload"])
                except Exception as exc:  # noqa: BLE001
                    logger.exception("subscriber error on {}: {}", msg["topic"], exc)

    def run_forever(self) -> None:
        self._thread = threading.Thread(target=self._pump, daemon=True)
        self._thread.start()
        self._stop.wait()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def dump_state(self) -> str:
        return json.dumps({"subscribers": {k: len(v) for k, v in self._subs.items()}})