#!/usr/bin/env python3
"""Update the README tree snapshot block."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
START_MARK = "<!-- TREE_SNAPSHOT_START -->"
END_MARK = "<!-- TREE_SNAPSHOT_END -->"


def list_entries(path: Path) -> list[Path]:
    return sorted(
        [p for p in path.iterdir() if not p.name.startswith(".")],
        key=lambda p: (not p.is_dir(), p.name.lower()),
    )


def build_tree(max_depth: int = 2) -> tuple[str, int, int]:
    lines = ["."]
    dir_count = 0
    file_count = 0

    def recurse(current: Path, prefix: str, depth: int) -> None:
        nonlocal dir_count, file_count
        entries = list_entries(current)
        total = len(entries)
        for idx, entry in enumerate(entries):
            connector = "└── " if idx == total - 1 else "├── "
            line = f"{prefix}{connector}{entry.name}"
            if entry.is_dir():
                dir_count += 1
                lines.append(line)
                if depth < max_depth:
                    next_prefix = prefix + ("    " if idx == total - 1 else "│   ")
                    recurse(entry, next_prefix, depth + 1)
            else:
                file_count += 1
                lines.append(line)

    recurse(ROOT, "", 1)
    lines.append("")
    lines.append(f"{dir_count} directories, {file_count} files")
    return "\n".join(lines), dir_count, file_count


def update_readme(tree_text: str) -> None:
    content = README_PATH.read_text(encoding="utf-8")
    start = content.find(START_MARK)
    end = content.find(END_MARK)
    if start == -1 or end == -1 or start >= end:
        raise SystemExit("Could not locate tree snapshot markers in README.md")

    block_start = content.find("```", start, end)
    block_end = content.rfind("```", start, end)
    if block_start == -1 or block_end == -1 or block_end <= block_start:
        raise SystemExit("Could not locate fenced block inside tree snapshot markers.")

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
