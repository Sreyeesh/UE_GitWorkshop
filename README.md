# UEGitWorkshop (UE5.6)

UEGitWorkshop is a minimal Unreal Engine 5.6 project set up to demonstrate clean Git practices for UE teams: correct ignore rules, Git LFS for binary assets, consistent naming conventions, and a simple CI pipeline to publish prebuilt game builds.

This README explains the repo layout, prerequisites, how to run/build locally, and how CI is configured.

**Highlights**
- Clean Git setup for UE projects (ignore rules + LFS)
- Consistent naming (e.g., maps use `L_` prefix: `L_Main`)
- Cross-checked source/module/targets naming (`UEGitWorkshop`)
- One‑shot build script to generate project files and build once
- GitHub Actions workflow to publish a prebuilt Windows game zip

**Requirements**
- Windows 10/11
- Unreal Engine 5.6 (installed via Epic Games Launcher)
  - Example path: `C:\Program Files\Epic Games\UE_5.6`
- Visual Studio 2022 with:
  - Desktop development with C++
  - Game development with C++ (MSVC, Windows SDK, C++ profiling tools)
- Python 3.11+ in `PATH` (for `build_ue.py`)
- Git + Git LFS (`git lfs install`)

## Project Structure

Top‑level, simplified (generated folders like `Intermediate/`, `DerivedDataCache/`, `Saved/`, and `Binaries/` are ignored by Git):

```
.
├── .clangd
├── .editorconfig
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── game-build.yml
├── Config/
│   ├── DefaultEngine.ini        ← Startup/Game map set to L_Main
│   └── DefaultGame.ini          ← Project metadata
├── Content/
│   ├── Maps/
│   │   └── L_Main.umap          ← Main level (rename done in Editor)
│   ├── Materials/
│   └── SimBlank/
│       ├── Blueprints/
│       └── Levels/
├── Source/
│   ├── UEGitWorkshop/
│   │   ├── Public/
│   │   │   ├── GitWorkshopHello.h
│   │   │   ├── HelloWorldSubsystem.h
│   │   │   └── UEGitWorkshopLog.h
│   │   ├── Private/
│   │   │   ├── GitWorkshopHello.cpp
│   │   │   ├── HelloWorldSubsystem.cpp
│   │   │   └── UEGitWorkshopLog.cpp
│   │   ├── UEGitWorkshop.Build.cs
│   │   └── UEGitWorkshop.cpp
│   ├── UEGitWorkshop.Target.cs
│   └── UEGitWorkshopEditor.Target.cs
├── UEGitWorkshop.uproject
└── build_ue.py
```

## Local Setup

1) Clone and enable LFS
- `git clone <your-repo-url>`
- `cd UEGitWorkshop`
- `git lfs install`

2) Configure Unreal Engine path
- Option A: Set an environment variable (recommended):
  - `UE_ENGINE_ROOT="C:\\Program Files\\Epic Games\\UE_5.6"`
- Option B: Pass `--engine` argument to the build script.

3) Ensure Visual Studio 2022 with C++ components is installed.

## Build & Run

Generate project files and build once via the helper script:
- `python build_ue.py --engine "C:\\Program Files\\Epic Games\\UE_5.6" --config Development --platform Win64`
  - The script tries `UnrealVersionSelector.exe` or falls back to UBT `-ProjectFiles`
  - Builds the Editor target by default; use `--game` to build game target

Open the project:
- Double‑click `UEGitWorkshop.uproject`, or
- Open the generated solution in Visual Studio and start the Editor target.

Default maps (configured in `Config/DefaultEngine.ini`):
- `EditorStartupMap=/Game/Maps/L_Main.L_Main`
- `GameDefaultMap=/Game/Maps/L_Main.L_Main`

If you just renamed maps in the filesystem, open the project and choose “Fix Up Redirectors” in the Content Browser to preserve references.

## CI/CD (GitHub Actions)

Workflow file: `.github/workflows/game-build.yml`
- Runs on GitHub-hosted `ubuntu-latest` (no Unreal install required)
- Publishes an existing Windows game zip provided via secret or found in the repo
- Steps:
  - Checkout (with LFS) and ensure real files
  - Download Windows build zip from `secrets.WINDOWS_GAME_ZIP_URL` (optional SHA256 via `secrets.WINDOWS_GAME_ZIP_SHA256`), or fall back to the first zip under `Builds/Windows/`, `Releases/`, or `windows/`
  - Upload the zip as artifact `Windows-Game`
  - Optional: compute a tag and create a GitHub Release attaching the zip when running on `main`/`master` or `workflow_dispatch`

Setup required:
- Repository secret `WINDOWS_GAME_ZIP_URL` pointing to your private packaged Windows build zip (recommended)
- Optional repository secret `WINDOWS_GAME_ZIP_SHA256` for checksum verification

Manual dispatch with optional tag:
- In GitHub → Actions → Game Build → Run workflow → optionally provide a tag (otherwise auto-generated)

## Naming Conventions

- Maps: `L_Example` (e.g., `L_Main`)
- Blueprints: `BP_Example`
- Materials: `M_Example`, Material Instances: `MI_Example`
- Textures: `T_Example`
- C++ classes: `A`/`U`/`F`/`I` prefix by type (e.g., `AActor`, `UObject`)
- Module/Targets/Project: `UEGitWorkshop` (PascalCase, no underscores)
- Logging: dedicated category `LogUEGitWorkshop` instead of `LogTemp`

## Troubleshooting

- “Could not locate Unreal Engine root”: set `--engine` or `UE_ENGINE_ROOT`.
- UBT/Generator errors: ensure Visual Studio 2022 with C++ workloads is installed.
- Missing binaries after build: check `Saved/Logs/` artifacts and runner environment.
- Asset renames: always rename inside the Unreal Editor and then “Fix Up Redirectors”.

## License

This repository is for workshop/training purposes. Add your license terms here if you plan to distribute.
