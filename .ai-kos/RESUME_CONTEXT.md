# Resume Context — travel-site

**Read this file first on every resume.**  
Knowledge-only governance doc — no build, deploy, or code changes implied by reading it.

> **Note:** `SESSION.md` is stale (last Baltic session). Prefer this file + `.ai-kos/STATUS.md` for current state.

**Canonical workspace（git 有效）：** `/Users/mac/Documents/Projects/旅遊/travel-site/`（`~/Documents/Projects/旅遊/travel-site/`）

> **2026-07-16**：專案已自 Desktop 移至 Documents。Agent 一律使用上述路徑；`~/Desktop/旅遊/travel-site/` 為空殼目錄（勿作為工作區）。

---

## Resume — Read First

### Operational Mode (PRIORITY)

Travel Site moved from **Development Mode → Operational Mode** (2026-07-13).

**Daily rule（2026-07-16 起）：** 開工或排程 session 時，**第二讀** `.ai-kos/DAILY_TRAVEL_UPDATE.md` — 每日 08:00 主動執行 Daily Travel Photo Sync 全流程。

**Current focus:**

- Daily sync 斌哥 travel photos（Drive SSOT → manifest 增量）
- Update daily travel journal (旅行札記，CONTENT_STYLE 第一人稱)
- Build → Verify → Deploy
- Commit → Push → Handoff

**NOT primary work anymore:** site feature development, architecture changes, workflow refactors, mass rewrites of old content.

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

---

### Infrastructure Quick Reference (facts)

| 項目 | 值 |
|------|-----|
| **Transitional browse URL** | https://cluttered-breath.surge.sh/ |
| **Temp validation** | cluttered-breath-prototype-v2.surge.sh |
| **Production domain BLOCKED** | cluttered-breath-prototype.surge.sh — **404**, not on wangjohnsonwt@gmail.com account; **do NOT** update `REPOSITORY.md` / `STATUS.md` deploy URL until restored |
| **GitHub** | https://github.com/slimgril/travel-site (`origin` configured) |
| **Local HEAD** | `cddf2af` — `feat(baltic): update Day 1 travel journal with storytelling style`; likely **1 commit ahead** of `origin/main` if not pushed |
| **Deploy pitfall** | Run `sips` / `package_preview_deploy` **OUTSIDE sandbox** or images go black |

---

### Daily Travel Update Workflow

**Canonical rule：** `.ai-kos/DAILY_TRAVEL_UPDATE.md`（含輸出模板、Error Policy、08:00 觸發）

摘要：Drive SSOT（見 `.ai-kos/INFRASTRUCTURE.md`）→ 增量 sync → 更新 dayXX.md → build → verify → deploy → commit/push（有變更）→ handoff

---

### Active Trips

| Slug | 狀態 | 備註 |
|------|------|------|
| `shanxi` | done | legacy style — do not mass-rewrite |
| `bldh-trio` | **operational** | Baltic; Day 1 complete with 10 photos (旅行札記 v1.0) |
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
- Project status: `.ai-kos/STATUS.md`
- Governance index: `.ai-kos/INDEX.md`
- Baikal photo sync: `content/baikal-rail/source/PHOTO_SYNC.md`
