"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import execute, plan_moves
from .manifest import undo, write_manifest
from .rules import load_rules


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="organizer",
        description="Smart File Organizer — tidy any folder automatically.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Folder to organize (default: current).")
    parser.add_argument(
        "-m", "--mode",
        choices=["category", "extension", "date"],
        default="category",
        help="How to group files (default: category).",
    )
    parser.add_argument("-r", "--recursive", action="store_true", help="Include sub-folders.")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Preview without moving anything.")
    parser.add_argument("-c", "--config", type=Path, help="Path to a custom rules JSON file.")
    parser.add_argument("--undo", type=Path, metavar="MANIFEST", help="Undo a previous run via its manifest.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _force_utf8_output() -> None:
    """Ensure non-ASCII output works on legacy Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass


def main(argv: list[str] | None = None) -> int:
    _force_utf8_output()
    args = build_parser().parse_args(argv)

    if args.undo:
        restored = undo(args.undo)
        print(f"↩️  Restored {restored} file(s).")
        return 0

    source = Path(args.path).expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Not a directory: {source}")

    rules = load_rules(args.config)
    moves = plan_moves(source, mode=args.mode, recursive=args.recursive, rules=rules)

    if not moves:
        print("✨ Nothing to organize — the folder is already tidy.")
        return 0

    prefix = "[dry-run] " if args.dry_run else ""
    for move in moves:
        print(f"{prefix}{move.src.name}  →  {move.dst.parent.name}/")

    performed = execute(moves, dry_run=args.dry_run)
    verb = "Would move" if args.dry_run else "Moved"
    print(f"\n{verb} {len(performed)} file(s).")

    if not args.dry_run:
        manifest = write_manifest(source, performed)
        print(f"\U0001f4dd Manifest saved: {manifest.name}")
        print(f"   Undo with:  organizer --undo \"{manifest}\"")
    return 0
