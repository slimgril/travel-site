---
project: bldh-trio
checkpoint:
  type: deploy
  ref: https://cluttered-breath-prototype.surge.sh/
phase: "Homepage restore + prototype packaging stabilization"
status: ready_to_commit
approval_gate: level-1
pending:
  - "Commit and push homepage restore / asset cleanup / deployment packaging fixes."
  - "Safari CSS issue remains browser-specific; Chrome validates deployment content."
blockers: none
updated: 2026-07-10
---

# SESSION — Baltic Trio (bldh-trio)

## 2026-07-10 Handoff — Homepage Restore + Prototype Deployment

### Goal

Restore the homepage hero / About Ben section onto the same prototype that already
contained the corrected Baltic Trio (`bldh-trio`) landmark photos, then make the
prototype deployable and traceable.

### Current State

- Prototype URL: `https://cluttered-breath-prototype.surge.sh/`
- The prototype homepage now includes the restored traveler hero and About Ben
  section.
- The prototype trip page `trips/bldh-trio.html` keeps the corrected landmark
  photos, including `三姊妹之屋`, `顛倒屋`, `AKROPOLIS`, and Taoyuan airport cards.
- Legacy `content/baltic.md` was removed so future builds do not generate a stale
  duplicate Baltic trip (`baltic.html`) beside canonical `bldh-trio.html`.
- `photos/site/` is the site-level portrait asset folder for homepage images.
  `photos/unassigned/` is retained as a non-deployed archive for future trips.

### Commands And Validation

- `python3 scripts/build_prototype.py` generated 2 trips (`shanxi`, `bldh-trio`)
  with `缺图 0`.
- `dist-prototype/` was scanned for deployment blockers:
  0-byte files, `.DS_Store`, logs, and ` 2.jpg` / ` 3.jpg` duplicate copy files.
- Deployment succeeded to `cluttered-breath-prototype.surge.sh` after removing
  stale/duplicate assets; package size dropped to about 159 MB.

### Observations

- Canonical reference was unclear: both legacy `baltic` and canonical
  `bldh-trio` content existed, which caused agents to patch or deploy the wrong
  output.
- AI work exceeded the requested scope earlier by touching non-target assets and
  mixing unrelated generated output into deployable folders.
- 0-byte assets were not rejected by the build; `photos/site/yabin-dalat.jpg`
  was empty and contributed to Surge deployment instability.
- macOS duplicate copy files (`* 2.jpg`, `* 3.jpg`) and `.DS_Store` files can
  enter deploy folders unless explicitly filtered.
- Surge CLI can mask the real processing error with
  `Cannot read properties of undefined (reading 'filename')`, so local asset
  hygiene checks are required before deploy.

### Fixes Landed

- Restored homepage hero / About Ben section in `scripts/build.py`.
- Separated site assets (`photos/site/`) from trip assets and unassigned archive
  assets (`photos/unassigned/`).
- Retired legacy Baltic single-file trip by removing `content/baltic.md`.
- Updated production copy logic to exclude internal asset folders and skip
  hidden files, 0-byte files, and duplicate copy filenames.
- Updated prototype overlay logic to apply the same asset hygiene rules.
- Fixed `photos/site/yabin-dalat.jpg` by copying the valid archive image from
  `photos/unassigned/`.

### Remaining Risks

- Safari may cache or fail to apply external CSS while Chrome renders correctly.
  The deployed content is valid; if Safari support remains a hard requirement,
  test a non-experimental fix separately before committing.

Last updated: 2026-07-05
Baseline commit: `568f0ad` (unchanged — prototype work is additive, no new commit yet)

## Prototype Image Pipeline (added 2026-07-05)

- New per-slug folders: `photos/<slug>/source/`, `cooked/matched/`, `cooked/review/`, `cooked/review.csv` — see `CONVENTIONS.md` §7.
- New build: `python3 scripts/build_prototype.py` → `dist-prototype/`. Overlays `cooked/matched/*` onto a *copy* of `reference/` inside `dist-prototype/photos/<slug>/reference/` only. Verified byte-identical production `dist/` before/after (sha256 of full `dist/` tree unchanged), and verified `photos/bldh-trio/reference/` on disk is never written by either build script.
- `photos/bldh-trio/source/` and `cooked/*` currently empty (scaffolding only) — no candidate images have been supplied yet, so the current `dist-prototype/` build is content-identical to production. This is the same "source cannot be verified" gap flagged earlier in this session; architecture is now ready but has nothing to diff against until candidate images arrive.
- Approval gate: **level-2** — nothing gets copied into `photos/bldh-trio/reference/` without explicit human approval after reviewing `dist-prototype/`.

## Current Phase

**Phase 3G — Landmark Presentation: COMPLETE**

`render_plan()` renders verified hero images (CSS background-image) + attribution /
license / official-link meta + 「參考圖片」badge into plan cards, consuming the
`landmarks` dict threaded through `render_trip_page()`. Non-verified landmarks
(顛倒屋) stay image-less. Build PASS, 缺图 0, all 25 verified heroes render.

Note: the presentation logic was already present in code at `568f0ad` (SESSION.md
had wrongly described 3F as infrastructure-only). This session **verified 3G and
fixed three defects it had shipped with**:
1. Hero background-image path was `../../photos/...` (one `../` too many; every other
   image uses `../photos/...`). Only masked today because the Surge deploy is
   root-hosted so browsers clamp the excess `..`. Fixed to `../photos/...`.
2. The build's missing-image checker only scanned `src="../photos/..."`, so every
   hero (a CSS `background-image`) bypassed validation — a broken hero path would
   still report 缺图 0. Checker now also scans `background-image:url('../photos/...')`.
   Verified with a negative test (a fake path is now caught).
3. day09 combined two verified landmarks in one card heading
   (`聖歐拉夫教堂・三姊妹之屋`); fuzzy-match resolved only 聖歐拉夫, so 三姊妹之屋's
   verified image never rendered (25 verified → 24 heroes). Split into two cards;
   now 25 heroes render.

## Completed Phases

- **Phase 3E — Hero Image Acquisition: COMPLETE**
  25 legal hero images acquired (Wikimedia Commons; CC BY-SA 2.0/3.0/4.0, CC0, Public Domain).
  1 landmark skipped (顛倒屋 / Upside Down House — UNVERIFIED location).
  `landmarks.yaml` annotated with `hero_image`, `image_source`, `license`, `attribution`, `wikimedia_file`, `image_verification_status`.
- **Phase 3F (infrastructure) — COMPLETE**
  Loader `load_landmarks_yaml()` added; parameter threaded through
  `render_trip_page()` → `render_day()` → `render_plan()`.
  Committed as `568f0ad`.
- **Phase 3G — Landmark Presentation — COMPLETE (this session)**
  Verified hero images + attribution/meta render in plan cards. Three defects
  fixed (see Current Phase). Not yet committed — pending your review.

## Current Project Status

- Trip: 波羅的海三小國 {11} 日 (World Journey #002), status = `upcoming`, 2026-07-11 → 07-21
- Build: PASS (3 trips generated, 0 missing images)
- Deploy: LIVE — https://cluttered-breath.surge.sh/trips/bldh-trio.html (HTTP 200); live output synced to current build (bldh-trio + baltic pages redeployed 2026-07-04)

## Verified Deliverables

| Artifact | Status |
|----------|--------|
| `content/bldh-trio/trip.md` | ✓ present |
| `content/bldh-trio/day01.md … day11.md` | ✓ 11 files present |
| `content/bldh-trio/landmarks.yaml` | ✓ 26 entries (25 verified + 1 UNVERIFIED) |
| `photos/bldh-trio/reference/` hero images | ✓ 25 images |
| Build output `dist/trips/bldh-trio.html` | ✓ generated (build exit 0) |
| Deployment | ✓ live, HTTP 200 |
| Landmark infra in `scripts/build.py` | ✓ committed `568f0ad` |

## Remaining Work

- Commit this session's 3G verification + fixes (`scripts/build.py` hero path +
  checker, `content/bldh-trio/day09.md` card split, `SESSION.md`) — pending your review.
- Resolve UNVERIFIED landmark 顛倒屋 (Upside Down House) — confirm location or drop.
- `gutmanis-cave.jpg` uses an 1810 public-domain artwork; replace if a modern CC photo becomes available.
- Candidate-image pipeline (source/cooked/ + `build_prototype.py`) remains ready but idle — no candidate images supplied yet.

## Known Blockers

- None blocking. One data caveat: 顛倒屋 remains UNVERIFIED (`hero_image: null`), intentionally excluded from rendering.

## Next Recommended Task

Review this session's diff and commit if satisfied. After that, the open items are
data-quality only: resolve or drop 顛倒屋, and optionally replace `gutmanis-cave.jpg`.
