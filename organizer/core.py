"""Planning and executing file moves."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .rules import DEFAULT_RULES, OTHER, extension_to_category

Mode = str  # "category" | "extension" | "date"

# Files the organizer creates itself and must never touch.
_IGNORED_PREFIX = "organizer-manifest"


@dataclass(frozen=True)
class Move:
    """A single planned move from ``src`` to ``dst``."""

    src: Path
    dst: Path


def _category_for(file: Path, ext_map: dict[str, str]) -> str:
    return ext_map.get(file.suffix.lower().lstrip("."), OTHER)


def _target_dir(file: Path, source: Path, mode: Mode, ext_map: dict[str, str]) -> Path:
    if mode == "extension":
        return source / (file.suffix.lower().lstrip(".") or "no-extension")
    if mode == "date":
        stamp = datetime.fromtimestamp(file.stat().st_mtime)
        return source / stamp.strftime("%Y-%m")
    return source / _category_for(file, ext_map)


def _dedupe(dst: Path) -> Path:
    """Return a non-clashing path by appending ' (n)' if needed."""
    if not dst.exists():
        return dst
    counter = 1
    while True:
        candidate = dst.parent / f"{dst.stem} ({counter}){dst.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def plan_moves(
    source: Path | str,
    mode: Mode = "category",
    recursive: bool = False,
    rules: dict[str, list[str]] | None = None,
) -> list[Move]:
    """Compute the list of moves needed to organize ``source``."""
    source = Path(source)
    ext_map = extension_to_category(rules or DEFAULT_RULES)
    candidates = source.rglob("*") if recursive else source.glob("*")

    moves: list[Move] = []
    for file in sorted(candidates):
        if not file.is_file() or file.name.startswith(".") or file.name.startswith(_IGNORED_PREFIX):
            continue
        target_dir = _target_dir(file, source, mode, ext_map)
        if file.parent == target_dir:
            continue  # already in the right place
        moves.append(Move(file, _dedupe(target_dir / file.name)))
    return moves


def execute(moves: list[Move], dry_run: bool = False) -> list[dict[str, str]]:
    """Perform the moves (unless ``dry_run``) and return a manifest list."""
    performed: list[dict[str, str]] = []
    for move in moves:
        if not dry_run:
            move.dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move.src), str(move.dst))
        performed.append({"src": str(move.src), "dst": str(move.dst)})
    return performed
