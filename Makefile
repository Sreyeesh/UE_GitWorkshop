ENV_FILE ?= .env
ifneq ("$(wildcard $(ENV_FILE))","")
include $(ENV_FILE)
endif

# Python – use the Windows launcher
PYTHON ?= py -3

UPROJECT ?= $(CURDIR)/UEGitWorkshop.uproject
BUILD_SCRIPT ?= build_ue.py
SNAPSHOT_SCRIPT ?= scripts/update_tree_snapshot.py

ifeq ($(OS),Windows_NT)
UE_ENGINE_ROOT = C:/Program Files/Epic Games/UE_5.6
UE_EDITOR = $(UE_ENGINE_ROOT)/Engine/Binaries/Win64/UnrealEditor.exe
else
UE_EDITOR ?= UnrealEditor
endif

export UE_ENGINE_ROOT
export UE_EDITOR

.PHONY: build launch run snapshot

build:
	$(PYTHON) $(BUILD_SCRIPT)

launch:
ifeq ("$(wildcard $(UPROJECT))","")
	$(error Could not find $(UPROJECT). Run make from the folder with UEGitWorkshop.uproject or fix UPROJECT.)
endif
	"$(UE_EDITOR)" "$(UPROJECT)"

run: build launch

snapshot:
	$(PYTHON) $(SNAPSHOT_SCRIPT)
