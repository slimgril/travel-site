# RESUME_CONTEXT（最新）

**更新：** 2026-07-30 commit+push Cutover（`0103b8c`）

## 上次停在

- Production Cutover → https://travel-site-quarter.pages.dev/（Surge＝fallback）
- Git：`faab4cf` Cutover + `0103b8c` STATUS · 已 push `origin/main`
- 跨文件關聯檢查完成（歷史 Surge 連結刻意保留）

## 下一步

1. 西伯利亞新圖／新日文案一律 CONTENT_STYLE **v1.2**
2. **Landmark Layer Rule**：斌哥照片只能附加於 Landmark 卡下方，**禁止替換或刪除** Landmark（見 `DECISIONS.md` 2026-08-08 · `CONTENT_STYLE.md` § Landmark Layer Rule）
3. 本季 Deploy：`npm run deploy:pages`（或 `bash scripts/deploy_cloudflare_pages.sh`）
4. 西伯利亞收工後：Owner 指定下季 **Pages project**
5. （可選）清理未追蹤：map preview 重複檔、brochure PDF、drive-originals 大檔；考慮 Git LFS（遠端警告 >50MB mp4）

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

Travel Site adopts **Content Style v1.2（資深旅遊作家 · 描述區）** — see `.ai-kos/CONTENT_STYLE.md`

| 原則 | 說明 |
|------|------|
| 身在現場 | 從感官細節切入；禁「這是 XXX」開頭 |
| 資訊嵌入 | 史實順口帶出，不條列 |
| 禁導覽／流水帳 | 禁「值得一遊」「我們去了然後……」 |
| 結尾感受 | 畫面或幽默的個人頓悟；禁總結式結論 |
| 篇幅 | **4–6 句**，精簡有畫面 |
| 一圖一故事／不拆兩卡 | 同前 |

**增量採用政策：**

- 自 v1.0／v1.1 起，所有**新增或修改**的內容遵循本規範
- **不全面重寫** — 既有旅程維持原狀，除非該檔案被主動編輯
- **BLDH Day 7–10** — 2026-07-30 已依 v1.1 批次改寫
- **編輯觸發** — 其餘天次僅在觸及某檔案時才改寫

**避免：** Wikipedia、導遊詞、流水帳、設計論文、建築規格羅列。  
**偏好：** 現場感受 × 短故事 × 團走雜記 × 情緒收尾。

**BLDH Trio 排版模板（HARD RULE）：** `bldh-trio` 專案所有排版／生成／合併／渲染，一律套用根目錄 `city-magazine-template.md`「城市雜誌風排版器模板」。排版器 `scripts/build_bldh_magazine.py` → 輸出 `content/bldh-trio/bldh-trio-magazine.html`（standalone，`build.py` 不處理）。詳見 `.ai-kos/DECISIONS.md`（2026-07-18）。

---

### Infrastructure Quick Reference (facts)

| 項目 | 值 |
|------|-----|
| **Production（本季）** | https://travel-site-quarter.pages.dev/ |
| **Deploy bundle** | `dist-surge-upload`（sips 壓縮）；禁止 deploy 未壓縮 `dist`／`photos/` 原圖 |
| **Deploy 指令** | `bash scripts/deploy_cloudflare_pages.sh` · Pages project `travel-site-quarter` |
| **Quarterly** | 本季＝波羅的海＋西伯利亞共用上列；**下季新旅程必須新 Pages project**（`DECISIONS.md` Cutover） |
| **Surge fallback** | cluttered-breath.surge.sh — 非預設；見 `DEPLOY_MIGRATION.md` Rollback |
| **Blocked legacy domain** | cluttered-breath-prototype.surge.sh — **404**；勿再部署至此 |
| **GitHub** | https://github.com/slimgril/travel-site (`origin` configured) |
| **Local path check** | `git rev-parse --show-toplevel` → Canonical Root |
| **Deploy pitfall** | Run `sips` / `package_preview_deploy` **OUTSIDE sandbox** or images go black |
| **Wrangler** | 須 `wrangler login`；OAuth 存在 `~/Library/Preferences/.wrangler/config/` |
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
| `baikal-rail` | upcoming | 西伯利亞；新日／新圖一律 **CONTENT_STYLE v1.1 壓縮四拍**（旅行書，非導覽）；sync：`scripts/sync_baikal_photos.py` |

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
