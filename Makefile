ENV_FILE ?= .env
ifneq ("$(wildcard $(ENV_FILE))","")
include $(ENV_FILE)
endif

# Python – prefer py on Windows, python3 elsewhere
ifeq ($(OS),Windows_NT)
PYTHON ?= py -3
else
PYTHON ?= python3
endif

BUILD_SCRIPT ?= build_ue.py
UPROJECT ?= UEGitWorkshop.uproject
SNAPSHOT_SCRIPT ?= scripts/update_tree_snapshot.py

# --- Unreal Engine discovery on Windows ---

UE_ENGINE_ROOT ?=

ifeq ($(OS),Windows_NT)
# NOTE: no backslashes to "escape" spaces – Make handles spaces fine in values
EPIC_WIN ?= C:/Program Files/Epic Games
PREFERRED_WIN_ENGINE := $(EPIC_WIN)/UE_5.6

# Prioritize UE_5.6 if it exists, otherwise fall back to the first UE_* folder
ifneq ($(strip $(wildcard $(PREFERRED_WIN_ENGINE))),)
UE_ENGINE_ROOT ?= $(PREFERRED_WIN_ENGINE)
else
WIN_ENGINE_CANDIDATE := $(firstword $(wildcard $(EPIC_WIN)/UE_*))
ifneq ($(strip $(WIN_ENGINE_CANDIDATE)),)
UE_ENGINE_ROOT ?= $(WIN_ENGINE_CANDIDATE)
endif
endif
endif

# --- Editor path ---

# If we have an engine root, build the full editor path
ifneq ($(strip $(UE_ENGINE_ROOT)),)
UE_EDITOR := $(UE_ENGINE_ROOT)/Engine/Binaries/Win64/UnrealEditor.exe
endif

# Fallback for non-Windows / custom setups: rely on UE_EDITOR being on PATH
UE_EDITOR ?= UnrealEditor

export UE_ENGINE_ROOT
export UE_EDITOR

.PHONY: build launch run snapshot

build:
	$(PYTHON) $(BUILD_SCRIPT)

launch:
ifeq ($(strip $(UE_EDITOR)),)
	$(error UE_EDITOR is not set. Provide UE_EDITOR=... or set UE_ENGINE_ROOT.)
endif
	"$(UE_EDITOR)" "$(UPROJECT)"

run: build launch

snapshot:
	$(PYTHON) $(SNAPSHOT_SCRIPT)
