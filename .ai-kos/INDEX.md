# Cursor Constitution

## Governance Creation Principle

Cursor is the Knowledge Maintainer for this repository.

Cursor maintains repository governance.

Cursor does not design repository governance.

Repository governance evolves only through explicit user-approved decisions.

Default workflow:

Observe

↓

Report

↓

Suggest

↓

Wait for Approval

↓

Synchronize

Rules

* Never infer repository structure.
* Never create governance documents proactively.
* Never create placeholder documents.
* Never scaffold governance.
* Never classify proposed documents as "missing."
* Report potential future governance only under **Suggestions**.
* Only `.ai-kos/INDEX.md` may be created automatically during repository initialization.
* Any additional governance document requires explicit user approval.
* INDEX.md may only reference governance documents that already exist.

This Constitution has higher priority than future synchronization tasks.

# AI-KOS Governance Index

Canonical entry point for repository governance.

## Scope

- Repository: `travel-site`
- Governance root: `.ai-kos/`
- Status: initialized

## Current Repository Documents

- **Resume context (read first):** `.ai-kos/RESUME_CONTEXT.md`
- **Daily operational rule (08:00 sync):** `.ai-kos/DAILY_TRAVEL_UPDATE.md`
- **Project infrastructure (permanent):** `.ai-kos/INFRASTRUCTURE.md`
- Content style (旅行札記 v1.0): `.ai-kos/CONTENT_STYLE.md`
- Project conventions: `CONVENTIONS.md`
- Session state: `SESSION.md`
- Asset and migration notes: `ASSET_CHECKLIST.md`
- Project status: `.ai-kos/STATUS.md`
- Repository record: `REPOSITORY.md`
- Architecture decisions: `.ai-kos/DECISIONS.md`
- Changelog: `HISTORY.md`

## Workspace Path（HARD RULE）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

## Daily Travel Update（Operational Mode）

- **Canonical rule:** `.ai-kos/DAILY_TRAVEL_UPDATE.md` — 每日 08:00 主動執行；Drive SSOT → 增量 sync → 旅行札記 → build → verify → deploy → commit/push → handoff
- Active project path: `/Users/mac/Documents/Projects/旅遊/travel-site/`
- Cross-ref: `.ai-kos/INFRASTRUCTURE.md` · `.ai-kos/CONTENT_STYLE.md` · `content/baikal-rail/source/PHOTO_SYNC.md`

## Baikal Rail Photo Sync

- Operations: `content/baikal-rail/source/PHOTO_SYNC.md`
- Drive folder convention: `content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
- Sync script: `scripts/sync_baikal_photos.py`
- Config / manifest: `content/baikal-rail/source/photo-sync-config.json`, `photo-sync.json`
- **Local staging (downloads):** `content/baikal-rail/source/Siberian_Railway_Landmarks/`
- **Site photos:** `photos/baikal-rail/day01/` … `day20/`

## Governance Backlog

- Repository overview
- Architecture map
- Workflow guide
- Decision log
- Recovery guide
- Changelog
- Prompt inventory

## Maintenance Notes

- This folder is reserved for AI-KOS governance.
- Existing project documents remain in place until synchronization is approved.
