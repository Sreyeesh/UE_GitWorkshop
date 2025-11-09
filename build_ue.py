import argparse
import os
import sys
import subprocess
from pathlib import Path


def log(msg: str) -> None:
    print(msg, flush=True)


def run(cmd):
    pretty = " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd)
    log(f">> {pretty}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def find_default_uproject() -> Path | None:
    here = Path.cwd()
    candidates = list(here.glob("*.uproject"))
    return candidates[0] if candidates else None


def find_engine_root(engine_arg: str | None) -> Path | None:
    if engine_arg:
        p = Path(engine_arg)
        return p if p.exists() else None

    # Environment variable hints
    for env_key in [
        "UE_ENGINE_ROOT",
        "UE5_ROOT",
        "UE4_ROOT",
        "UNREAL_ENGINE",
        "UE_ROOT",
    ]:
        val = os.environ.get(env_key)
        if val:
            p = Path(val)
            if p.exists():
                return p

    # Common Windows install location via Epic Games Launcher
    epic_root = Path(r"C:\Program Files\Epic Games")
    if epic_root.exists():
        ue_dirs = [d for d in epic_root.iterdir() if d.is_dir() and d.name.startswith("UE_")]
        if ue_dirs:
            # Pick the highest version-like directory (e.g., UE_5.4 over UE_5.3)
            def version_key(p: Path):
                try:
                    return tuple(int(x) for x in p.name.split("_")[1].split("."))
                except Exception:
                    return (0,)

            ue_dirs.sort(key=version_key, reverse=True)
            return ue_dirs[0]

    return None


def main():
    parser = argparse.ArgumentParser(description="Regenerate UE project files and build once")
    parser.add_argument("--project", dest="project", help="Path to .uproject (defaults to first in CWD)")
    parser.add_argument("--engine", dest="engine", help="Engine root, e.g. C:\\Program Files\\Epic Games\\UE_5.3")
    parser.add_argument("--config", dest="config", default="Development", help="Build config (Development/DebugGame/Shipping)")
    parser.add_argument("--platform", dest="platform", default="Win64", help="Build platform (Win64, etc.)")
    parser.add_argument("--game", dest="game", action="store_true", help="Build game target instead of Editor")
    args = parser.parse_args()

    # Resolve project
    proj_path = Path(args.project) if args.project else find_default_uproject()
    if not proj_path or not proj_path.exists():
        log("ERROR: Could not find .uproject. Use --project to specify a path.")
        sys.exit(2)
    proj_path = proj_path.resolve()

    # Resolve engine root
    engine_root = find_engine_root(args.engine)
    if not engine_root:
        log("ERROR: Could not locate Unreal Engine root. Set --engine or UE_ENGINE_ROOT.")
        sys.exit(3)
    engine_root = engine_root.resolve()

    proj_name = proj_path.stem
    target = proj_name if args.game else f"{proj_name}Editor"

    uvs = engine_root / "Engine" / "Binaries" / "Win64" / "UnrealVersionSelector.exe"
    ubt = engine_root / "Engine" / "Binaries" / "DotNET" / "UnrealBuildTool" / "UnrealBuildTool.exe"
    build_bat = engine_root / "Engine" / "Build" / "BatchFiles" / "Build.bat"

    # Generate project files
    if uvs.exists():
        run([str(uvs), "/projectfiles", str(proj_path)])
    elif ubt.exists():
        run([str(ubt), "-ProjectFiles", f"-Project={proj_path}", "-Game", "-Engine", "-VS2022"])
    else:
        log(f"ERROR: Could not find UnrealVersionSelector or UBT under: {engine_root}")
        sys.exit(4)

    # Build once
    if not build_bat.exists():
        log(f"ERROR: Build.bat not found: {build_bat}")
        sys.exit(5)

    run([
        str(build_bat),
        target,
        args.platform,
        args.config,
        f"-Project={proj_path}",
        "-WaitMutex",
        "-FromMsBuild",
    ])


if __name__ == "__main__":
    main()

