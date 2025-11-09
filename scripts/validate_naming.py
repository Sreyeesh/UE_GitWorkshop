import argparse
import sys
from pathlib import Path


def check_conventions(content_root: Path) -> list[str]:
    problems: list[str] = []

    for path in content_root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        lower_parts = [p.lower() for p in path.parts]
        suffix = path.suffix.lower()

        # Maps must be L_*.umap
        if suffix == ".umap":
            if not name.startswith("L_"):
                problems.append(f"Map without L_ prefix: {path.as_posix()}")
            continue

        if suffix != ".uasset":
            continue

        # Heuristic by folder names
        if "blueprints" in lower_parts and not name.startswith("BP_"):
            problems.append(f"Blueprint without BP_ prefix: {path.as_posix()}")
        if "materials" in lower_parts and not (name.startswith("M_") or name.startswith("MI_")):
            problems.append(f"Material without M_/MI_ prefix: {path.as_posix()}")
        if ("textures" in lower_parts or "thumbnails" in lower_parts) and not name.startswith("T_"):
            problems.append(f"Texture/thumbnail without T_ prefix: {path.as_posix()}")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Unreal asset naming conventions by folder heuristics")
    parser.add_argument("--content", default="Content", help="Content root path (default: Content)")
    parser.add_argument("--report", help="Optional path to write a report file")
    args = parser.parse_args()

    content_root = Path(args.content)
    if not content_root.exists():
        print(f"Content root not found: {content_root}")
        return 0

    problems = check_conventions(content_root)

    if problems:
        header = "Naming convention issues detected:\n"
        body = "\n".join(f"- {p}" for p in problems)
        output = header + body + "\n"
    else:
        output = "No naming convention issues detected.\n"

    # Write optional report file
    if args.report:
        try:
            Path(args.report).write_text(output, encoding="utf-8")
        except Exception as e:
            print(f"Failed to write report {args.report}: {e}")

    # Always print to stdout for CI tee/appends
    print(output, end="")

    # Non-zero exit to indicate problems when used as a blocking check
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

