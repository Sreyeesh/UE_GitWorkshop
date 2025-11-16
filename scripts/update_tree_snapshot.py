#!/usr/bin/env python3
"""Update the README tree snapshot block."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
START_MARK = "<!-- TREE_SNAPSHOT_START -->"
END_MARK = "<!-- TREE_SNAPSHOT_END -->"


def git_ls_tree(prefix: str | None = None) -> list[tuple[str, bool]]:
    cmd = ["git", "-C", str(ROOT), "ls-tree", "HEAD"]
    path_prefix = None
    if prefix:
        path_prefix = f"{prefix}/"
        cmd.append(path_prefix)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    entries: list[tuple[str, bool]] = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        meta, name = line.split("\t", 1)
        _mode, type_, _sha = meta.split(" ")
        if path_prefix and name.startswith(path_prefix):
            display_name = name[len(path_prefix):]
        else:
            display_name = name
        entries.append((display_name, type_ == "tree"))
    entries.sort(key=lambda item: (not item[1], item[0].lower()))
    return entries


def build_tree(max_depth: int = 2) -> tuple[str, int, int]:
    lines = ["."]
    dir_count = 0
    file_count = 0

    def recurse(prefix: str | None, display_prefix: str, depth: int) -> None:
        nonlocal dir_count, file_count
        entries = git_ls_tree(prefix)
        total = len(entries)
        for idx, (name, is_dir) in enumerate(entries):
            connector = "└── " if idx == total - 1 else "├── "
            lines.append(f"{display_prefix}{connector}{name}")
            if is_dir:
                dir_count += 1
                if depth < max_depth:
                    next_prefix = f"{prefix}/{name}" if prefix else name
                    next_display_prefix = display_prefix + ("    " if idx == total - 1 else "│   ")
                    recurse(next_prefix, next_display_prefix, depth + 1)
            else:
                file_count += 1

    recurse(None, "", 1)
    lines.append("")
    lines.append(f"{dir_count} directories, {file_count} files")
    return "\n".join(lines), dir_count, file_count


def update_readme(tree_text: str) -> None:
    content = README_PATH.read_text(encoding="utf-8")
    start = content.find(START_MARK)
    end = content.find(END_MARK)
    if start == -1 or end == -1 or start >= end:
        raise SystemExit("Could not locate tree snapshot markers in README.md")

    new_block = f"{START_MARK}\n```text\n{tree_text}\n```\n"
    new_content = content[:start] + new_block + content[end:]
    README_PATH.write_text(new_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README tree snapshot.")
    parser.add_argument("--depth", type=int, default=2, help="Tree depth limit (default: 2)")
    args = parser.parse_args()

    tree_text, _, _ = build_tree(args.depth)
    update_readme(tree_text)
    print("Updated README tree snapshot.")


if __name__ == "__main__":
    main()
