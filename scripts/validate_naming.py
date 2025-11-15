import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BLUEPRINT_HINTS: tuple[str, ...] = ("blueprint", "blueprints", "actor", "actors")
MATERIAL_HINTS: tuple[str, ...] = ("material", "materials")
TEXTURE_HINTS: tuple[str, ...] = ("texture", "textures", "thumbnail", "thumbnails")
PREFIX_TYPE_ORDER: tuple[tuple[str, str], ...] = (
    ("WBP_", "blueprint"),
    ("ABP_", "blueprint"),
    ("BP_", "blueprint"),
    ("MI_", "material"),
    ("M_", "material"),
    ("T_", "texture"),
)


@dataclass
class Issue:
    path: Path
    message: str
    suggested_filename: str | None = None

    def target_path(self) -> Path | None:
        if not self.suggested_filename:
            return None
        return self.path.with_name(self.suggested_filename)


def detect_asset_type(asset_name: str) -> str | None:
    """Return a logical asset type inferred from its prefix."""
    for prefix, asset_type in PREFIX_TYPE_ORDER:
        if asset_name.startswith(prefix):
            return asset_type
    return None


def has_hint(parts: Iterable[str], hints: tuple[str, ...]) -> bool:
    """Best-effort match for folder keywords (e.g., Blueprints, Actors, Textures)."""
    return any(hint in part for part in parts for hint in hints)


def prefixed_filename(path: Path, prefix: str) -> str:
    stem = path.stem
    if stem.startswith(prefix):
        return path.name
    return f"{prefix}{stem}{path.suffix}"


def check_conventions(content_root: Path) -> list[Issue]:
    problems: list[Issue] = []

    for path in content_root.rglob("*"):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(content_root).parts
        folder_parts = [p.lower() for p in relative_parts[:-1]]
        stem = path.stem
        suffix = path.suffix.lower()
        asset_type = detect_asset_type(stem)

        # Maps must be L_*.umap
        if suffix == ".umap":
            if not stem.startswith("L_"):
                problems.append(
                    Issue(
                        path=path,
                        message=f"Map without L_ prefix: {path.as_posix()}",
                        suggested_filename=prefixed_filename(path, "L_"),
                    )
                )
            continue

        if suffix != ".uasset":
            continue

        # Heuristic by folder names (blueprints/actors/widgets/etc.)
        if has_hint(folder_parts, BLUEPRINT_HINTS) and asset_type != "blueprint":
            problems.append(
                Issue(
                    path=path,
                    message=f"Blueprint without BP_ prefix: {path.as_posix()}",
                    suggested_filename=prefixed_filename(path, "BP_"),
                )
            )

        if has_hint(folder_parts, MATERIAL_HINTS) and asset_type != "material":
            problems.append(
                Issue(
                    path=path,
                    message=f"Material without M_/MI_ prefix: {path.as_posix()}",
                    suggested_filename=prefixed_filename(path, "M_"),
                )
            )

        if has_hint(folder_parts, TEXTURE_HINTS) and asset_type != "texture":
            problems.append(
                Issue(
                    path=path,
                    message=f"Texture/thumbnail without T_ prefix: {path.as_posix()}",
                    suggested_filename=prefixed_filename(path, "T_"),
                )
            )

    return problems


def apply_renames(issues: list[Issue]) -> list[str]:
    """Attempt to rename assets using suggested filenames; return log lines."""
    logs: list[str] = []
    for issue in issues:
        target = issue.target_path()
        if not target:
            continue

        source_display = issue.path.as_posix()
        target_display = target.as_posix()

        if target.exists():
            logs.append(f"Skipped rename (target exists): {source_display} -> {target_display}")
            continue

        try:
            issue.path.rename(target)
            logs.append(f"Renamed {source_display} -> {target_display}")
        except OSError as exc:
            logs.append(f"Failed to rename {source_display} -> {target_display}: {exc}")

    return logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Unreal asset naming conventions by folder heuristics")
    parser.add_argument("--content", default="Content", help="Content root path (default: Content)")
    parser.add_argument("--report", help="Optional path to write a report file")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically rename assets that are missing required prefixes (may break references; use with caution)",
    )
    args = parser.parse_args()

    content_root = Path(args.content)
    if not content_root.exists():
        print(f"Content root not found: {content_root}")
        return 0

    issues = check_conventions(content_root)
    rename_logs: list[str] = []

    if args.fix and issues:
        rename_logs = apply_renames(issues)
        # Re-run checks in case fixes resolved issues
        issues = check_conventions(content_root)

    lines: list[str] = []
    if issues:
        lines.append("Naming convention issues detected:")
        lines.extend(f"- {issue.message}" for issue in issues)
    else:
        lines.append("No naming convention issues detected.")

    if rename_logs:
        lines.append("Auto-fix actions:")
        lines.extend(f"- {entry}" for entry in rename_logs)

    output = "\n".join(lines) + "\n"

    # Write optional report file
    if args.report:
        try:
            Path(args.report).write_text(output, encoding="utf-8")
        except Exception as e:
            print(f"Failed to write report {args.report}: {e}")

    # Always print to stdout for CI tee/appends
    print(output, end="")

    # Non-zero exit to indicate problems when used as a blocking check
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
