#!/usr/bin/env python3
"""Update CHANGELOG.md from git history for a new tag."""

from __future__ import annotations

import argparse
import datetime as _dt
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = ROOT / "CHANGELOG.md"


def _git_log_subjects(range_spec: list[str]) -> list[str]:
    cmd = ["git", "-C", str(ROOT), "log", "--no-merges", "--pretty=format:%s", *range_spec]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    subjects = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return subjects


def _ensure_header(content: str | None) -> str:
    header = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n"
    if content is None or not content.strip():
        return header
    if not content.lstrip().startswith("# Changelog"):
        return header + "\n" + content
    return content


def update_changelog(prev_tag: str | None, new_tag: str) -> bool:
    if prev_tag:
        range_spec = [f"{prev_tag}..HEAD"]
    else:
        range_spec = []

    subjects = _git_log_subjects(range_spec)
    if not subjects:
        # Nothing to record for this range.
        print("No commits found for changelog; skipping update.")
        return False

    today = _dt.date.today().isoformat()
    section_lines: list[str] = [
        f"## {new_tag} - {today}",
        "",
    ]
    section_lines.extend(f"- {s}" for s in subjects)
    section_lines.append("")
    section_text = "\n".join(section_lines)

    if CHANGELOG_PATH.exists():
        existing = CHANGELOG_PATH.read_text(encoding="utf-8")
    else:
        existing = None

    existing = _ensure_header(existing)
    lines = existing.splitlines()

    # Insert new section after the header and any following blank lines.
    insert_index = 0
    if lines and lines[0].startswith("# Changelog"):
        insert_index = 1
        while insert_index < len(lines) and not lines[insert_index].strip():
            insert_index += 1

    new_lines = lines[:insert_index] + [""] + section_lines + lines[insert_index:]
    CHANGELOG_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Updated CHANGELOG.md for {new_tag}.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Update CHANGELOG.md from git history.")
    parser.add_argument("--from-tag", dest="from_tag", default="", help="Previous tag (exclusive range start).")
    parser.add_argument("--to-tag", dest="to_tag", required=True, help="New tag name being created.")
    args = parser.parse_args()

    prev = args.from_tag.strip() or None
    updated = update_changelog(prev, args.to_tag)
    if not updated:
        raise SystemExit(0)


if __name__ == "__main__":
    main()

