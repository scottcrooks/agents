#!/usr/bin/env python3
"""Emit a JSON manifest of committable working-tree files, excluding thoughts/."""

from __future__ import annotations

import json
import argparse
import subprocess
import sys
from pathlib import Path, PurePosixPath


EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def git(*args: str, check: bool = True) -> bytes:
    result = subprocess.run(
        ["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def decode(value: bytes) -> str:
    return value.decode("utf-8", "surrogateescape")


def under_thoughts(path: str) -> bool:
    return "thoughts" in PurePosixPath(path).parts


def parse_status() -> list[dict[str, object]]:
    fields = git("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0")
    files: list[dict[str, object]] = []
    index = 0
    while index < len(fields) and fields[index]:
        record = fields[index]
        index += 1
        xy = decode(record[:2])
        path = decode(record[3:])
        original_path = None
        if "R" in xy or "C" in xy:
            if index >= len(fields):
                raise RuntimeError("malformed rename record from git status")
            original_path = decode(fields[index])
            index += 1
        if under_thoughts(path) or (original_path and under_thoughts(original_path)):
            continue
        files.append(
            {
                "path": path,
                "original_path": original_path,
                "index_status": xy[0],
                "worktree_status": xy[1],
                "staged": xy[0] not in {" ", "?"},
                "unstaged": xy[1] not in {" ", "?"},
                "untracked": xy == "??",
            }
        )
    return files


def parse_changes_from_base(base: str) -> list[dict[str, object]]:
    fields = git(
        "diff",
        "--name-status",
        "-z",
        "--find-renames",
        base,
        "--",
        ".",
        ":(exclude)thoughts/**",
    ).split(b"\0")
    files: list[dict[str, object]] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = decode(fields[index])
        index += 1
        original_path = None
        if status.startswith(("R", "C")):
            original_path = decode(fields[index])
            index += 1
        path = decode(fields[index])
        index += 1
        if under_thoughts(path) or (original_path and under_thoughts(original_path)):
            continue
        files.append(
            {
                "path": path,
                "original_path": original_path,
                "index_status": status[0],
                "worktree_status": " ",
                "staged": False,
                "unstaged": True,
                "untracked": False,
            }
        )

    known_paths = {str(entry["path"]) for entry in files}
    for entry in parse_status():
        if entry["untracked"] and str(entry["path"]) not in known_paths:
            files.append(entry)
    return files


def diff_stats(base: str, entry: dict[str, object], root: Path) -> tuple[int | None, int | None, bool]:
    path = str(entry["path"])
    if entry["untracked"]:
        target = root / path
        if not target.is_file():
            return 0, 0, False
        data = target.read_bytes()
        if b"\0" in data:
            return None, None, True
        return len(data.splitlines()), 0, False

    paths = [path]
    if entry["original_path"]:
        paths.append(str(entry["original_path"]))
    output = decode(git("diff", "--numstat", "--no-renames", base, "--", *paths))
    added = deleted = 0
    binary = False
    for line in output.splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 2:
            continue
        if parts[0] == "-" or parts[1] == "-":
            binary = True
            continue
        added += int(parts[0])
        deleted += int(parts[1])
    return (None, None, True) if binary else (added, deleted, False)


def main() -> int:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--base")
        args = parser.parse_args()
        root = Path(decode(git("rev-parse", "--show-toplevel")).strip())
        has_head = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
        base = args.base or ("HEAD" if has_head else EMPTY_TREE)
        files = parse_changes_from_base(base) if args.base else parse_status()
        total_added = total_deleted = 0
        for entry in files:
            added, deleted, binary = diff_stats(base, entry, root)
            entry.update({"added": added, "deleted": deleted, "binary": binary})
            total_added += added or 0
            total_deleted += deleted or 0
        manifest = {
            "repository_root": str(root),
            "mode": "pinned" if args.base else "pre-commit",
            "base": base if args.base else ("HEAD" if has_head else "empty-tree"),
            "files": files,
            "totals": {
                "files": len(files),
                "added": total_added,
                "deleted": total_deleted,
            },
        }
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"collect_review_set: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
