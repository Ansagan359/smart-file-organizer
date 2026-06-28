"""Undo support via a JSON manifest of performed moves."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path


def write_manifest(source: Path | str, moves: list[dict[str, str]]) -> Path:
    """Write a timestamped manifest into ``source`` and return its path."""
    name = f"organizer-manifest-{time.strftime('%Y%m%d-%H%M%S')}.json"
    path = Path(source) / name
    path.write_text(json.dumps({"moves": moves}, indent=2), encoding="utf-8")
    return path


def undo(manifest_path: Path | str) -> int:
    """Move files back to their original locations. Returns the count restored."""
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    restored = 0
    for move in reversed(data.get("moves", [])):
        current, original = Path(move["dst"]), Path(move["src"])
        if current.exists():
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current), str(original))
            restored += 1
    return restored
