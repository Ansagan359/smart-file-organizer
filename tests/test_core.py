"""Tests for the organizer core."""

from __future__ import annotations

from organizer.core import execute, plan_moves
from organizer.manifest import undo, write_manifest


def _touch(path):
    path.write_text("x", encoding="utf-8")


def test_groups_by_category(tmp_path):
    _touch(tmp_path / "photo.png")
    _touch(tmp_path / "report.pdf")
    execute(plan_moves(tmp_path))
    assert (tmp_path / "Images" / "photo.png").exists()
    assert (tmp_path / "Documents" / "report.pdf").exists()


def test_unknown_extension_goes_to_other(tmp_path):
    _touch(tmp_path / "mystery.xyz")
    execute(plan_moves(tmp_path))
    assert (tmp_path / "Other" / "mystery.xyz").exists()


def test_dry_run_moves_nothing(tmp_path):
    _touch(tmp_path / "photo.png")
    execute(plan_moves(tmp_path), dry_run=True)
    assert (tmp_path / "photo.png").exists()
    assert not (tmp_path / "Images").exists()


def test_name_collisions_are_deduped(tmp_path):
    _touch(tmp_path / "a.png")
    (tmp_path / "Images").mkdir()
    _touch(tmp_path / "Images" / "a.png")
    execute(plan_moves(tmp_path))
    assert (tmp_path / "Images" / "a.png").exists()
    assert (tmp_path / "Images" / "a (1).png").exists()


def test_undo_restores_files(tmp_path):
    _touch(tmp_path / "photo.png")
    performed = execute(plan_moves(tmp_path))
    manifest = write_manifest(tmp_path, performed)
    restored = undo(manifest)
    assert restored == 1
    assert (tmp_path / "photo.png").exists()
    assert not (tmp_path / "Images" / "photo.png").exists()
