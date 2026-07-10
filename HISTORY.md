# HISTORY

## 2026-07-10 — Homepage Restore And Prototype Packaging Fix

- Restored the homepage hero / About Ben section onto the canonical prototype site.
- Confirmed `bldh-trio` is the canonical Baltic Trio trip; removed the legacy
  `content/baltic.md` path to avoid duplicate `World Journey #002` output.
- Separated homepage portraits in `photos/site/` from trip assets and preserved
  unassigned future-trip assets in `photos/unassigned/`.
- Fixed deployment packaging by filtering hidden files, 0-byte files, and macOS
  duplicate copy names such as `* 2.jpg` / `* 3.jpg`.
- Observation: unclear canonical reference caused agents to patch the wrong
  output, non-target assets were modified during diagnosis, and 0-byte assets
  were not blocked until this fix.
- Deployment observation: Surge may report a generic `filename` processing error
  when the deploy package contains bad assets; validate locally before deploy.
