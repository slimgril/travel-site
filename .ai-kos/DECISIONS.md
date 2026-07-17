# DECISIONS — travel-site

架構與流程決策紀錄。新增決策時在最上方追加條目。

---

## 2026-07-18 — 排版風格＝Knowledge（Template Library 原則）

**性質**：架構原則（使用者明確陳述，記錄／同步，非我主動 scaffold）。

**原則：** AI-KOS 將**排版風格（Layout）視為 Knowledge，而非 Prompt**。所有模板皆為**可重複使用的 Knowledge Asset**。Project **不直接描述排版**，而是**指定使用哪一個 Template**。

**知識流：**

```
Knowledge → Template → Renderer → Output
```

**首個具體實例（已驗證）：**

| 層 | 實體 |
|----|------|
| Knowledge | 旅程內容 `content/bldh-trio/day*.md`（旅行札記 v1.0） |
| Template | `city-magazine-template.md`（城市雜誌風，根目錄 SSOT） |
| Renderer | `scripts/build_bldh_magazine.py` |
| Output | `content/bldh-trio/bldh-trio-magazine.html` |

**含義：**
- Project 端只需「指定 Template」，不再在 prompt 內描述排版細節
- 同一 Template 可被多個 Project／旅程重用
- 模板規格變更 = 修改 Template（Knowledge），Renderer 依模板產出

**待批准（Suggestion，未執行）：** 是否新開 `.ai-kos/TEMPLATES.md` 作為正式 Template Library 登錄（依 `INDEX.md` 治理原則，新增治理文件需明確批准）。

---

## 2026-07-18 — BLDH Trio 指定「城市雜誌風排版器模板」為正式排版規格

**性質**：專案排版規格決策（僅限 `bldh-trio`，不影響其他旅程或 `build.py` 主流程）。

**決策：** 波羅的海三小國 11 天（`bldh-trio`）專案，所有**排版、生成、合併、渲染**流程一律套用「城市雜誌風排版器模板」。

| 角色 | 檔案 |
|------|------|
| **模板（SSOT）** | 根目錄 `city-magazine-template.md` |
| **排版器** | `scripts/build_bldh_magazine.py`（header 已標註以模板為準） |
| **輸出** | `content/bldh-trio/bldh-trio-magazine.html`（standalone，`build.py` 不處理） |

**模板規格摘要：** 大標題＋斜體副標（原文首句）· 行距 1.75 · 字重 300–400 · 全寬圖片不裁切／不變形 · 上下留白 · `---` 細線分隔 · `✦` 金線側註 · Day kicker（Day 01）· meta 卡片（航班／住宿／領隊／午晚餐）· 歷史／古蹟／預告分節標。

**約束：**
- 排版器必須可重複執行，且產出恆依 `city-magazine-template.md`
- 只調整排版，不改動 `day*.md` 原始文字（layout only）
- 未來新增的「城市散步類」旅程沿用同一模板

**參考**：`city-magazine-template.md` · `scripts/build_bldh_magazine.py`

---

## 2026-07-17 — Knowledge First 營運驗證（Baltic Day 3）

**性質**：營運驗證紀錄（非新規則、非流程重設計）。記於此處而非 AI-KOS 憲法——憲法不放營運範例。

**背景**：Baltic Day 3（07/13 維爾紐斯）以一個真實案例驗證了 AI-KOS **Rule 0：Knowledge First**。

**觀察到的工作流：**

1. 先驗證來源完整性（Drive SSOT 掃描）
2. 偵測到同步落差（Drive `0713/` 約 27 張，本機僅 2 張）
3. 先修復知識完整性（增量同步補齊 Day 3 照片）
4. 才生成旅行內容（札記 + build + deploy）

**關鍵教訓：**

> **正確的知識，先於正確的內容（Correct knowledge precedes correct content）。**

若當時直接就本機既有 2 張照片撰稿，會漏掉整天的維爾紐斯行程；先補知識再產出，才得到完整交付。

**參考**：`.ai-kos/STATUS.md`（2026-07-17 Day 3 entry）· `AI-KOS.md` Rule 0 / Rule -1（真實專案驗證）

---

## 2026-07-17 — Observability 原則 + Operational Confidence 選填欄位

**決策**：對齊已被真實營運驗證的知識，於文件層面同步（不改行為、不重設計流程）。

1. **Observability** 確立為 AI-KOS **營運設計原則**，記於 `AI-KOS.md`（哲學層級，無實作細節）：讓人類理解 AI 正在做什麼、進度、營運健康、是否需介入。其具體展現即既有的**固定營運摘要**與 **Optional Safety Layer** 批准前摘要——屬同一原則的展現，故僅交叉引用、不另立新機制。
2. **Operational Confidence** 加入 `DAILY_TRAVEL_UPDATE.md`，為**選填**欄位（High/Medium/Low + Reason）。整合進既有「可選附註」區，不新增必填欄位、不取代 `Status`。

**一致性處理（發現的潛在衝突）：**

- `AI-KOS/CLAUDE.md`：「Prefer evidence-backed conclusions over self-reported confidence.」
- 為避免牴觸，Operational Confidence 明確定義為**由摘要既有證據彙整**（Source / Build / Deploy / Live / review_required），非主觀自評。

**理由**：兩項知識已由多次真實營運 session 驗證（符合 Rule -1）；以最小幅度落於最合適文件，維持一致、避免重複。

---

## 2026-07-16 — Wake command：Ingest（跨文件相關內容同步）

**決策**：新增喚醒／替代指令 **Ingest**（`ingest` 同等）。

**定義：**

> **Ingest** = 修改跨文件中的相關內容。

**行為：**

1. 以本次（或使用者指定）變更為中心，搜尋仍引用舊名稱、舊 URL、舊 Phase／Mode、舊模板的相關文件  
2. **一併修改**使 AI-KOS、操作手冊、父層 `CLAUDE.md`、現行 deploy／sync 指引一致  
3. 歷史 archive（如 STALE `SESSION.md`、已標 legacy 的舊敘事）可保留，但**可執行指令**必須改為現行正確值  
4. 不做無關功能開發、不做 bulk rewrite  
5. 完成後簡報：改了哪些檔、刻意未改哪些

**與其他指令關係：**

| 指令 | 用途 |
|------|------|
| **開工** | 恢復記憶 → 預設 Daily Travel Update |
| **收工** | 寫斷點 → 道別 |
| **Ingest** | 跨文件相關內容同步（知識一致性） |

**理由**：Operational Phase 下仍需偶爾對齊文件；用短指令代替長說明，避免漏改相關檔。

---

## 2026-07-16 — Operational Phase 正式生效

**決策**：自本日起 travel-site 正式進入 **Operational Phase**。`6779dac`（Workspace Integrity）已上遠端；治理基建凍結為夠用狀態。

**原則：**

> AI-KOS 服務旅行書，而不是旅行書繼續服務 AI-KOS。

**自 2026-07-17 起預設工作：** Daily Travel Update（照片 → 札記 → build → deploy → 固定營運摘要）。  
**非預設：** 擴充 AI-KOS、路徑再遷移、架構重構、舊內容 bulk rewrite（需使用者明確授權）。

**理由**：Integrity 與 Daily Update 模板已就緒；繼續打磨 KOS 會反客為主。

---

## 2026-07-16 — Daily Update 固定營運摘要（Handoff）

**決策**：Daily Travel Update 每次回報**結尾**必須輸出固定短摘要（欄位名不可改），格式見 `.ai-kos/DAILY_TRAVEL_UPDATE.md` § 輸出模板。

**必填欄位**：Date / Trip / New Photos / Updated Day / Travel Notes / Build / Deploy / Live Verification / Commit / Production / Status

**理由**：營運已穩定；固定摘要方便每日掃讀與跨 session 對帳，避免表格與敘事混雜。

**參考**：使用者核定範例（2026-07-13 Baltic，Commit `ce389e9`）

---

## 2026-07-16 — Canonical workspace path（Documents ONLY）

**決策**：travel-site 與所有旅遊子專案**唯一**工作區為 Documents。Desktop 路徑**永久禁止**。

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

**政策**：

1. Agent / 腳本 / 文件 / Cursor workspace **一律**使用 Documents 路徑
2. **禁止**「Desktop 或 Documents 擇一」「try both paths」等模糊指引
3. **禁止**在 Desktop 路徑讀寫、commit、push、deploy
4. 若 Cursor workspace 指向 Desktop → Agent **立即停止**並要求使用者重新開啟 Documents 資料夾
5. `~/Desktop/旅遊/` 僅允許導向文件（`DEPRECATED.md` / redirect `CLAUDE.md`）；**禁止**存在可被 Cursor 開啟的 `travel-site/` 子目錄
6. Workspace Integrity SSOT：`.ai-kos/WORKSPACE.md`（路徑衝突時以此為準）
7. 若本機 git 物件損壞，優先自 `origin/main` 還原；無法安全修復則 **rebuild clone**，不得沿用半壞 repo

**理由**：2026-07-15 桌面整理後專案已遷移；Cursor 若開錯 workspace 會導致 agent 在空殼或錯誤路徑工作，造成資料遺失。2026-07-16 Integrity 稽核確認：路徑已在 Documents，但 Desktop 假專案目錄與損壞 blob 仍會造成「看似還在舊路徑」的錯覺。

---

## 2026-07-16 — Daily Travel Photo Sync（Operational Phase · 08:00）

**決策**：自 2026-07-16 起，travel-site 進入 **Daily Travel Photo Sync** 營運規則 — 每日 **08:00（Asia/Taipei）** Agent **主動**執行 Daily Travel Update，無需使用者提醒。  
（舊稱 Operational Mode；正式名稱以 **Operational Phase** 為準，見上方條目。）

**流程**（canonical：`.ai-kos/DAILY_TRAVEL_UPDATE.md`）：

1. Drive SSOT 掃描（`.ai-kos/INFRASTRUCTURE.md`，不 re-ask Folder ID）
2. 增量同步（比對 `photo-sync.json` manifest）
3. 更新旅行札記（所有新照片，`.ai-kos/CONTENT_STYLE.md` 第一人稱視角）
4. Build → Verify → Deploy → Commit/Push（有變更時）→ **固定營運摘要** Handoff

**Error Policy**：auth / permission / infrastructure 錯誤 — **立即停止、不重試、回報根因**。

**理由**：

- Operational Phase 需固定節奏，避免照片與札記滞後
- 單一 canonical 規則供開工與排程 session 遵循
- 與既有 Drive SSOT、增量 sync 決策一致，不重複基礎設施定義

**Active path**：`/Users/mac/Documents/Projects/旅遊/travel-site/`

**參考**：`.ai-kos/DAILY_TRAVEL_UPDATE.md` · `.ai-kos/RESUME_CONTEXT.md` · `content/baikal-rail/source/PHOTO_SYNC.md`

---

## 2026-07-13 — Google Drive Shared Folder 永久 SSOT

**決策**：斌哥所有旅行照片以單一 Google Drive Shared Folder 為**永久唯一來源**（Single Source of Truth）。Folder ID 固定為 `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`，不因新旅程而更換。

**政策**：

1. **固定根資料夾** — Shared Folder URL / ID 不變；各次旅行以子資料夾區分
2. **Resume 不 re-ask** — 恢復 session 或旅行更新時，直接使用此 Folder，不再要求使用者提供路徑
3. **Daily Update 增量同步** — 每次日常更新由此 Folder 增量同步（見 Incremental Sync 決策）
4. **Photo Sync 統一入口** — 所有 trip 的照片同步一律從此 Shared Folder 開始

**理由**：

- 避免每次 session 重複確認 Drive 路徑，降低交接摩擦
- 單一 SSOT 便於跨 trip 管理與備份
- 子資料夾模型已於 baikal-rail 驗證（`DRIVE_FOLDER_CONVENTION.md`）

**參考**：`.ai-kos/INFRASTRUCTURE.md` · `content/baikal-rail/source/photo-sync-config.json`

---

## 2026-07-13 — Google Drive 採 Incremental Sync

**決策**：Baikal Rail 照片自 Google Drive 匯入時，採**增量同步**（manifest 驅動），而非每次全量重新下載。

**理由**：

1. **避免重複下載** — 以 `drive_file_id` 與 SHA-256 hash 去重，節省頻寬與時間
2. **保留手動策展** — 不覆寫 `dayXX.md` 中已有 `![...]` 的標題；不覆寫既有 `photos/` 檔案
3. **支援每日同步** — 使用者上傳新照片後，單一指令即可只處理增量
4. **不猜 Day** — 路徑無法解析時不強制歸類，改進 review 流程（見下一則決策）

**實作**：`scripts/sync_baikal_photos.py` + `content/baikal-rail/source/photo-sync.json`

**不修改**：`scripts/build.py`、`scripts/build_prototype.py`、網站 UI/CSS、其他 trip

---

## 2026-07-13 — AI 無法判定 Day 時 → Review Required

**決策**：當 Drive 路徑缺少 `Day XX - 景點名` 結構，或資料夾名無法對應 `dayXX.md` landmark 標題時，**不進行自動分類**，改寫入 `photo-sync.json` → `review_required`。

**理由**：

1. 日期資料夾（如 `0711/`、`0712/`）或 `IMG_xxxx` 檔名無法可靠對應行程天數
2. 錯誤自動歸類會污染 `photos/baikal-rail/` 與 `dayXX.md`，比待審更難修復
3. 人工將照片移至正確 Drive 資料夾後，下次 sync 即可自動匯入

**拒絕的替代方案**：依 EXIF 日期或檔名推測 Day — 準確率不足，且與「Knowledge First」衝突

**參考**：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
