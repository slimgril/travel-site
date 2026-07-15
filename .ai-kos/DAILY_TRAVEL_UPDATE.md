# Daily Travel Update — 每日旅行照片同步（Operational Rule）

**狀態**：Operational Mode 生效（2026-07-16 起）  
**觸發**：每日 **08:00（Asia/Taipei）**，Agent **主動執行**，無需使用者提醒  
**性質**：AI-KOS 營運規則 — Agent 於「開工」或排程 session 時必讀並遵循

---

## 目的

在 Operational Mode 下，以固定節奏維持 travel-site 與斌哥 Google Drive 照片 SSOT 同步，並更新旅行札記、建置、驗證、部署與版本控制。

**單一真相來源（Drive）**：見 `.ai-kos/INFRASTRUCTURE.md` — **不在此重複 Folder ID**。

---

## 適用時機

| 情境 | 行為 |
|------|------|
| 每日 08:00 排程 session | **立即**執行本規則全流程 |
| 使用者 `/start` 或「開工」且當日尚未執行 | **優先**執行本規則，再處理其他請求 |
| 使用者明確要求 Daily Travel Update | 執行本規則 |
| Development 任務（架構、CSS、build 重構） | **不在**本規則範圍；需使用者明確授權 |

**Active project path**（canonical，git 有效）：

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

所有步驟（sync、build、deploy、commit、push）**僅**在 Documents 路徑執行。若 Cursor workspace 指向 Desktop → STOP，要求使用者重新開啟 Documents 資料夾。

---

## 前置閱讀（Knowledge First）

執行前確認已讀：

| 文件 | 用途 |
|------|------|
| `.ai-kos/INFRASTRUCTURE.md` | Drive SSOT、本機照片路徑、Resume 不 re-ask |
| `.ai-kos/CONTENT_STYLE.md` | 旅行札記 v1.0 — **第一人稱旅行者視角** |
| `content/baikal-rail/source/PHOTO_SYNC.md` | 增量同步、manifest、build/deploy 細節 |
| `.ai-kos/RESUME_CONTEXT.md` | Operational Mode 優先序、活躍旅程 |
| `.ai-kos/STATUS.md` | 當前 trip 狀態、待審數量 |

---

## 全流程（依序執行）

```text
1. Drive SSOT 掃描
        ↓
2. 增量同步（比對 photo-sync manifest）
        ↓
3. 更新旅行札記（所有新照片 + CONTENT_STYLE）
        ↓
4. Build
        ↓
5. Verify
        ↓
6. Deploy
        ↓
7. Commit / Push（僅當有變更）
        ↓
8. Handoff
```

### Step 1 — Drive SSOT 掃描

- 使用 `.ai-kos/INFRASTRUCTURE.md` 記載的 **永久 Shared Folder**（不詢問使用者路徑）
- 列出各旅程子資料夾內新增或變更的檔案
- 依 `content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md` 理解資料夾結構

### Step 2 — 增量同步

- 比對 `content/baikal-rail/source/photo-sync.json` manifest（`drive_file_id`、SHA-256 hash）
- 執行：

```bash
cd ~/Documents/Projects/旅遊/travel-site
python3 scripts/sync_baikal_photos.py --dry-run   # 先預覽
python3 scripts/sync_baikal_photos.py           # 正式同步
```

- **只處理增量** — 不重複下載、不覆寫既有 `photos/` 與已有 `![...]` 的 markdown
- 無法判定 Day → 寫入 `review_required`，**不猜**（見 `.ai-kos/DECISIONS.md`）
- 詳細行為：`content/baikal-rail/source/PHOTO_SYNC.md`

### Step 3 — 更新旅行札記

對本次同步匯入的**每一張新照片**：

1. 找到對應 `content/<trip>/dayXX.md` landmark 區塊
2. 依 `.ai-kos/CONTENT_STYLE.md` 撰寫或補充**第一人稱旅行者視角**敘事
3. 確保 `![alt](photos/...)` 引用正確；一圖一故事
4. **增量採用** — 僅改動本次觸及的 day 檔；不批次重寫舊旅程

**活躍旅程**（以 `.ai-kos/STATUS.md` 為準，常見：`bldh-trio`、`baikal-rail`）

### Step 4 — Build

```bash
python3 scripts/build_prototype.py
```

- 輸出：`dist-prototype/`
- **不修改** `scripts/build.py`、`scripts/build_prototype.py`、templates、CSS（除非使用者明確要求）

### Step 5 — Verify

確認以下全部 PASS：

- Build Mapping Report：0 missing/broken images、0 broken links
- `dist-prototype/index.html` 與活躍 trip 頁面存在且非空
- 抽樣 HTTP 200（若已 deploy）或本機 dist 完整性
- `review_required` 數量已記錄於 handoff（不阻塞 deploy，但須報告）

### Step 6 — Deploy

```bash
# sips / package_preview_deploy 須在 sandbox 外執行，否則圖片可能變黑
# 詳見 PHOTO_SYNC.md § Deploy
surge dist-preview-deploy cluttered-breath.surge.sh
```

- 過渡瀏覽 URL：https://cluttered-breath.surge.sh/
- 生產域名若 BLOCKED — 見 `.ai-kos/RESUME_CONTEXT.md`，勿反覆重試

### Step 7 — Commit / Push

**僅當** git 有實質變更（content、photos、manifest、dist 相關設定）：

```bash
git add <relevant paths>
git commit -m "<簡述：例 feat(baltic): daily sync Day N photos + journal>"
git push origin main
```

- 無變更 → 跳過 commit/push，於 handoff 註明「No changes」
- **勿提交** credentials、`.env`、service account JSON

### Step 8 — Handoff

以下方 **輸出模板** 回報使用者；更新 `.ai-kos/STATUS.md` 若狀態有實質變化。

---

## 輸出模板（Handoff 必填）

Agent 完成（或中止）Daily Travel Update 後，**必須**以以下格式回報：

```markdown
## Daily Travel Update — YYYY-MM-DD HH:MM (Asia/Taipei)

| 項目 | 結果 |
|------|------|
| **新增照片數** | N 張（synced）/ M 張（review_required） |
| **更新 Day** | `<trip>` day01, day02, …（或「無」） |
| **Build** | PASS / FAIL — <摘要> |
| **Verify** | PASS / FAIL — <摘要> |
| **Deploy** | PASS / SKIP / FAIL — <URL 或原因> |
| **Commit** | `<hash>` / SKIP（無變更） |
| **Push** | origin/main OK / SKIP / FAIL |
| **Handoff** | <下一步或待人工事項> |

### 摘要
<1–3 句：今日同步重點、待審照片、阻塞原因>

### review_required（若有）
- `<filename>` — `<reason>` — 建議動作
```

---

## Error Policy（錯誤政策）

**遇以下類型錯誤 — 立即停止，不重試，回報根本原因：**

| 類型 | 範例 | 行為 |
|------|------|------|
| **Auth** | gdown / Drive API / Service Account 認證失敗 | STOP — 報告認證方式與錯誤訊息 |
| **Permission** | Drive 403、Shared Folder 無存取、Surge 帳號不符 | STOP — 報告所需權限與帳號 |
| **Infrastructure** | 網路中斷、git remote 不可達、磁碟滿、Surge CLI crash | STOP — 報告基礎設施根因 |

**禁止：**

- 對 auth / permission / infrastructure 錯誤自動重試或換路徑繞過
- 將 Drive 同步失敗改從非 canonical 本機資料夾 fallback 匯入
- 在錯誤未解決時仍 commit/push 半成品

**允許繼續（非阻塞）：**

- `review_required` 照片（記錄於 handoff，不猜 Day）
- 無新增照片（仍執行 verify；deploy/commit 依是否有變更決定）

**內容錯誤**（markdown 語法、單張缺圖）：修復後繼續；若無法在單次 session 修復，STOP 並報告。

---

## 與其他文件的關係

| 文件 | 關係 |
|------|------|
| `.ai-kos/INFRASTRUCTURE.md` | Drive SSOT、本機路徑 — **Folder ID 唯一定義處** |
| `.ai-kos/CONTENT_STYLE.md` | Step 3 札記文風 |
| `content/baikal-rail/source/PHOTO_SYNC.md` | Step 2 同步實作細節 |
| `.ai-kos/DECISIONS.md` | 增量同步、review_required 決策背景 |
| `.ai-kos/RESUME_CONTEXT.md` | 開工第一讀；指向本規則 |

---

## Agent 快速檢查清單

- [ ] 確認 Active path：`~/Documents/Projects/旅遊/travel-site/`
- [ ] 讀 INFRASTRUCTURE（Drive SSOT，不 re-ask）
- [ ] `--dry-run` 後正式 sync
- [ ] 每張新圖更新 dayXX.md（CONTENT_STYLE 第一人稱）
- [ ] build → verify → deploy（sips 在 sandbox 外）
- [ ] 有變更才 commit/push
- [ ] 填寫 Handoff 輸出模板
- [ ] auth/permission/infrastructure 錯誤 → STOP，不重試
