# WORKSPACE — travel-site Integrity SSOT

**狀態**：Canonical（2026-07-16 Workspace Integrity）  
**Phase**：Operational — AI-KOS 服務旅行書；路徑衝突時以此文件為準，但**不再**以擴充本文件為每日目標。

---

## Canonical Paths（唯一合法）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
WORKSPACE PARENT:       /Users/mac/Documents/Projects/旅遊/
FORBIDDEN:              /Users/mac/Desktop/旅遊/
```

| 項目 | 值 |
|------|-----|
| **Git toplevel** | 必須等於 Canonical Project Root |
| **Cursor folderUri** | `file:///Users/mac/Documents/Projects/旅遊/travel-site` |
| **GitHub** | `https://github.com/slimgril/travel-site` |
| **Deploy URL（過渡）** | `https://cluttered-breath.surge.sh/` |

---

## Agent Preflight（每次開工）

1. `pwd` / `git rev-parse --show-toplevel` → 必須是 Canonical Root  
2. 若路徑含 `/Desktop/旅遊` → **STOP**，要求使用者重新開啟 Documents  
3. 讀本文件 → `.ai-kos/RESUME_CONTEXT.md` → `.ai-kos/DAILY_TRAVEL_UPDATE.md`  
4. 不詢問、不 fallback 至 Desktop

---

## What Must Never Hardcode Absolute Desktop Paths

| 層級 | 規則 |
|------|------|
| **Scripts** | 一律 `ROOT = Path(__file__).resolve().parent.parent`（相對 repo） |
| **photo-sync-config** | 僅相對路徑（`content/…`、`photos/…`） |
| **Deploy** | `surge_domain` = `cluttered-breath.surge.sh`（過渡）；勿寫本機絕對路徑 |
| **Knowledge** | 可寫 Canonical / FORBIDDEN 對照；不得把 Desktop 標成 active |

---

## Desktop Residue Policy

- `~/Desktop/旅遊/` 若存在：僅允許 `DEPRECATED.md` / 導向 `CLAUDE.md`  
- **禁止**存在可被 Cursor 開啟的 `~/Desktop/旅遊/travel-site/` 專案目錄  
- Cursor 舊專案快取 `~/.cursor/projects/Users-mac-Desktop-travel-site/` 為 IDE 殘留；不作為工作區

---

## Integrity Checks

```bash
cd /Users/mac/Documents/Projects/旅遊/travel-site
test "$(git rev-parse --show-toplevel)" = "/Users/mac/Documents/Projects/旅遊/travel-site"
git fsck --no-full
python3 scripts/build_prototype.py
python3 scripts/sync_baikal_photos.py --dry-run
```

---

## Related

- Resume：`.ai-kos/RESUME_CONTEXT.md`  
- Infra / Drive SSOT：`.ai-kos/INFRASTRUCTURE.md`  
- Daily ops：`.ai-kos/DAILY_TRAVEL_UPDATE.md`  
- Decision：`.ai-kos/DECISIONS.md` — Canonical workspace path  
