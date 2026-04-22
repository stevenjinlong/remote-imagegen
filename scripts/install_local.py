#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def remove_existing_target(target: Path) -> None:
    if not target.exists() and not target.is_symlink():
        return
    if target.is_symlink() or target.is_file():
        target.unlink()
        return
    shutil.rmtree(target)


def install_target(source: Path, target: Path, mode: str, force: bool) -> str:
    source = source.resolve()
    if target.is_symlink():
        current = Path(os.readlink(target))
        if not current.is_absolute():
            current = (target.parent / current).resolve()
        if current == source:
            return "unchanged"

    if target.exists() or target.is_symlink():
        if not force:
            raise FileExistsError(f"Target already exists: {target}. Use --force to replace it.")
        remove_existing_target(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        target.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(
            source,
            target,
            symlinks=True,
            ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
        )
    return mode


DEFAULT_SKILL_NAME = "remote-imagegen"
DEFAULT_CODEX_SKILL_ROOT = Path.home() / ".codex" / "skills"


def default_skill_source(repo_root: Path) -> Path:
    return repo_root / "skills" / DEFAULT_SKILL_NAME


def build_skill_target(skill_root: Path, skill_name: str) -> Path:
    return skill_root / skill_name


def validate_skill_source(source: Path) -> None:
    if not (source / "SKILL.md").is_file():
        raise RuntimeError(f"Source does not look like a skill directory: {source}")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Install the remote-imagegen skill into ~/.codex/skills.")
    parser.add_argument("--source", type=Path, default=default_skill_source(repo_root), help="Skill source directory.")
    parser.add_argument("--skill-name", default=DEFAULT_SKILL_NAME, help="Installed skill directory name.")
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink", help="Install mode.")
    parser.add_argument("--force", action="store_true", help="Replace the target skill directory if it already exists.")
    parser.add_argument("--codex-skill-root", type=Path, default=DEFAULT_CODEX_SKILL_ROOT, help="Codex skills root directory.")
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    validate_skill_source(source)
    target = build_skill_target(args.codex_skill_root.expanduser(), args.skill_name)

    results: dict[str, Any] = {
        "source": str(source),
        "skill_name": args.skill_name,
    }
    results["codex_skill_dir"] = {
        "path": str(target),
        "status": install_target(source, target, args.mode, args.force),
    }
    results["restart_codex"] = True

    print(json.dumps(results, indent=2))
    return 0


def main() -> int:
    try:
        return run()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
