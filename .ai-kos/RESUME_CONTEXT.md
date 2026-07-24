# RESUME_CONTEXT（最新）

**更新：** 2026-07-24 晚 Handoff

## 上次停在

- 貝加爾足跡圖國名排版已定（Owner BINGO）
- 圖檔三原則已入 `CLAUDE.md`／cursor rules
- Baltic Day5 等先前改動仍可能未全部 commit（見 STATUS）

## 下一步

1. 若需上線足跡圖：rebuild＋deploy `baikal-rail`
2. Daily Travel Update 依 Photos SSOT 繼續
3. 遵守三原則配圖

---
# Resume Context — travel-site

**Read `.ai-kos/WORKSPACE.md` first, then this file.**  
Knowledge-only governance doc — no build, deploy, or code changes implied by reading it.

> **Note:** `SESSION.md` is stale (last Baltic session). Prefer `WORKSPACE.md` + this file + `.ai-kos/STATUS.md` for current state.

## Workspace Path（HARD RULE — read before any work）

**SSOT：** `.ai-kos/WORKSPACE.md`

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

- **Cursor workspace** 必須開啟 Documents 路徑；若目前 workspace 指向 Desktop，**立即停止**並要求使用者重新開啟正確資料夾
- `~/Desktop/旅遊/` 僅允許導向文件；**不得**存在可開啟的 `travel-site/` 子目錄（2026-07-16 Integrity：已移除）

---

## Resume — Read First

### Operational Phase（PRIORITY — 2026-07-16 正式生效）

Travel Site 已進入 **Operational Phase**。

> **原則：** AI-KOS 服務旅行書；旅行書不再繼續服務 AI-KOS。  
> 自 **2026-07-17** 起，預設工作是把斌哥的旅途變成可瀏覽的書，不是擴充治理文件或重構基礎設施。

**Daily rule：** 開工或排程 session 時，讀 `.ai-kos/DAILY_TRAVEL_UPDATE.md` — 每日 08:00 主動執行 Daily Travel Update 全流程，結尾輸出固定營運摘要。

**Current focus（只做這些）：**

- Daily sync 斌哥 travel photos（Drive SSOT → manifest 增量）
- Update daily travel journal（旅行札記，CONTENT_STYLE 第一人稱）
- Build → Verify → Deploy
- Commit → Push → 固定營運摘要 Handoff

**NOT primary work（除非使用者明確要求）：**

- 新增／重寫 AI-KOS 治理文件
- site feature development、architecture、workflow refactor
- 舊旅程 bulk rewrite
- Workspace / 路徑再遷移（Integrity 已完成）
- **景點點擊播放音樂**（計畫已入庫 `content/bldh-trio/source/MUSIC_CLICK_PLAN.md`；行程＋合法音檔就緒前不實作、不為此改部署）

### Wake commands

| 指令 | 行為 |
|------|------|
| **開工** / `/start` | 讀斷點 + `RESUME_CONTEXT`；預設跑 Daily Travel Update |
| **收工** / `/end` | 寫輕量斷點至父層 `CLAUDE.md` 後道別 |
| **Ingest** | **跨文件相關內容同步**：找出本次修改牽涉的相關文件並一併改一致（見 `DECISIONS.md`） |

**Ingest 一句話：** 修改跨文件中的相關內容。不是新功能，是知識／設定一致性修補。

---

### Content Style

Travel Site adopts **Content Style v1.0 (旅行札記)** — see `.ai-kos/CONTENT_STYLE.md`

| 原則 | 說明 |
|------|------|
| 第一人稱旅行者視角 | 親眼所見、親身體驗、當下感受為主；可自然省略主詞 |
| 體驗優先 | 景點歷史/文化/建築僅作背景，篇幅約 **20–30%**，不可喧賓奪主 |
| 一圖一故事 | 每張照片有自己的故事，不重複同一段景點介紹 |
| 照片融入情境 | 斌哥入鏡時自然融入當下，不描述「這是一張合影」 |
| 保留結構 | 維持既有 Markdown 區塊（`## 歷史`、`## 古蹟`、`###` 卡片、`![...](path)`），不更動 CSS 或 build 模板 |

**增量採用政策：**

- 自 v1.0 起，所有**新增或修改**的內容遵循本規範
- **不全面重寫** — 既有旅程（山西、西伯利亞大鐵路等）維持原狀，除非該檔案被主動編輯
- **試點** — `content/bldh-trio/day01.md`（Baltic Day 1）已套用；新天次與旅程逐步擴及
- **編輯觸發** — 僅在觸及某檔案時才改寫該檔

**避免：** Wikipedia 式條目、旅遊書導覽、百科介紹、年代表堆砌、建築規格羅列。  
**偏好：** 漫步……、穿過……、抬頭望見……、停下腳步……、忍不住拍下……、留下這張照片……

**BLDH Trio 排版模板（HARD RULE）：** `bldh-trio` 專案所有排版／生成／合併／渲染，一律套用根目錄 `city-magazine-template.md`「城市雜誌風排版器模板」。排版器 `scripts/build_bldh_magazine.py` → 輸出 `content/bldh-trio/bldh-trio-magazine.html`（standalone，`build.py` 不處理）。詳見 `.ai-kos/DECISIONS.md`（2026-07-18）。

---

### Infrastructure Quick Reference (facts)

| 項目 | 值 |
|------|-----|
| **Transitional browse URL** | https://cluttered-breath.surge.sh/ |
| **Blocked legacy domain** | cluttered-breath-prototype.surge.sh — **404**；勿再部署至此 |
| **GitHub** | https://github.com/slimgril/travel-site (`origin` configured) |
| **Local path check** | `git rev-parse --show-toplevel` → Canonical Root |
| **Deploy pitfall** | Run `sips` / `package_preview_deploy` **OUTSIDE sandbox** or images go black |

---

### Daily Travel Update Workflow

**Canonical rule：** `.ai-kos/DAILY_TRAVEL_UPDATE.md`（含固定營運摘要、Error Policy、08:00 觸發）

摘要：Drive SSOT（見 `.ai-kos/INFRASTRUCTURE.md`）→ 增量 sync → 更新 dayXX.md → build → verify → deploy → commit/push（有變更）→ handoff

**Handoff 結尾必出固定摘要：** Date / Trip / New Photos / Updated Day / Travel Notes / Build / Deploy / Live Verification / Commit / Production / Status（完整欄位見該規則 § 輸出模板）

---

### Active Trips

| Slug | 狀態 | 備註 |
|------|------|------|
| `shanxi` | done | legacy style — do not mass-rewrite |
| `bldh-trio` | **operational** | Baltic；Day 4 已上線；回饋修正（文學街／meta／額外推薦）已 deploy；下一步 Day 5（07/15） |
| `baikal-rail` | upcoming | 71 images; sync script exists (`scripts/sync_baikal_photos.py`) |

---

### Do NOT on Resume (unless user explicitly asks)

- Modify `build.py` workflow
- Change CSS / templates
- Retry production surge domain (`cluttered-breath-prototype.surge.sh`) repeatedly
- Mass rewrite old trip content (shanxi, baikal-rail, etc.)

---

## Related Documents

- **Daily operational rule:** `.ai-kos/DAILY_TRAVEL_UPDATE.md`
- Drive SSOT & paths: `.ai-kos/INFRASTRUCTURE.md`
- Content style spec: `.ai-kos/CONTENT_STYLE.md`
- BLDH Trio 排版模板: `city-magazine-template.md`（排版器 `scripts/build_bldh_magazine.py`）
- Project status: `.ai-kos/STATUS.md`
- Governance index: `.ai-kos/INDEX.md`
- Baikal photo sync: `content/baikal-rail/source/PHOTO_SYNC.md`
