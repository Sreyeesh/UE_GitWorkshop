PYTHON ?= python3
BUILD_SCRIPT ?= build_ue.py
UPROJECT ?= UEGitWorkshop.uproject
UE_EDITOR ?= UnrealEditor
SNAPSHOT_SCRIPT ?= scripts/update_tree_snapshot.py

.PHONY: build launch run snapshot

build:
	$(PYTHON) $(BUILD_SCRIPT)

launch:
	"$(UE_EDITOR)" "$(UPROJECT)"

run: build launch

snapshot:
	$(PYTHON) $(SNAPSHOT_SCRIPT)
