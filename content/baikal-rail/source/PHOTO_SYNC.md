# Baikal Rail Photo Sync

Google Drive → Travel Site 增量照片同步（僅 `baikal-rail`）。

**相關文件**：[DRIVE_FOLDER_CONVENTION.md](./DRIVE_FOLDER_CONVENTION.md) · [photo-sync-config.json](./photo-sync-config.json) · [photo-sync.json](./photo-sync.json)

---

## Architecture

```text
Google Drive (shared folder)
        │
        ▼
photo-sync-config.json          ← 設定：Drive URL、路徑、deploy 參數
        │
        ▼
scripts/sync_baikal_photos.py   ← 增量 orchestrator（不修改 build.py）
        │
        ├── gdown / Drive API / rclone   ← 列出 & 下載
        ├── photo-sync.json              ← manifest（已同步、待審、hash）
        ├── drive-originals/             ← 原始下載保留
        ├── photos/baikal-rail/dayXX/    ← 正式網站圖片
        └── content/baikal-rail/dayXX.md ← 僅在 gray card 時插入 ![...]
        │
        ▼
scripts/build_prototype.py      ← 既有 build，未修改
        │
        ▼
dist-prototype/ → dist-preview-deploy/ → Surge
```

**設計原則**（見 `.ai-kos/DECISIONS.md`）：

- 增量同步，不重複下載
- 不覆寫既有圖片與已有 `![...]` 的 markdown
- 無法判定 Day → `review_required`，不猜

---

## Folder Structure

| 路徑 | 用途 |
|------|------|
| `content/baikal-rail/source/photo-sync-config.json` | 同步設定（Drive URL、路徑、deploy） |
| `content/baikal-rail/source/photo-sync.json` | Manifest：已同步、來源清單、review_required |
| `content/baikal-rail/source/drive-originals/` | 從 Drive 下載的原始檔（依 Drive 路徑鏡像） |
| `photos/baikal-rail/dayXX/` | 網站正式圖片（`*-downloaded.jpg` 命名） |
| `content/baikal-rail/dayXX.md` | 行程 Markdown；landmark 標題決定配對 |

**Drive 端結構**（必讀 [DRIVE_FOLDER_CONVENTION.md](./DRIVE_FOLDER_CONVENTION.md)）：

```text
<Shared Folder>/
├── Day 02 - 烏蘭巴托市景/
│   └── IMG_2423.JPG
├── Day 04 - 蒙古國民族舞蹈與馬頭琴表演/
│   └── ...
└── ...
```

---

## Config

`photo-sync-config.json` 主要欄位：

| 欄位 | 說明 |
|------|------|
| `drive.folder_url` | Google Drive 共用資料夾 URL |
| `drive.folder_id` | 資料夾 ID（`1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`） |
| `paths.sync_state` | Manifest 路徑 → `photo-sync.json` |
| `paths.source_originals` | 原始檔目錄 |
| `paths.photos_root` | 正式圖片根目錄 |
| `paths.content_root` | Markdown 根目錄 |
| `access_methods` | 嘗試順序：`gdown` → `google_drive_api` → `rclone` |
| `deploy.*` | Surge 域名、`dist-prototype` / `dist-preview-deploy`、sips 壓縮參數 |
| `naming.*` | 文件化命名慣例（腳本內建 regex，非 runtime 讀取） |

可選：`credentials`（Service Account JSON）、`rclone_remote`。

---

## Manifest（photo-sync.json）

### 頂層欄位

| 欄位 | 說明 |
|------|------|
| `source` | Drive URL 與 folder_id |
| `last_sync` | 上次同步 ISO 時間 |
| `summary` | 計數摘要（synced_count、review_required_count 等） |
| `synced[]` | 已成功匯入的檔案紀錄 |
| `source_inventory[]` | 歷史來源掃描（consumed 狀態） |
| `review_required[]` | 待人工處理的 Drive 檔案 |

### synced 項目範例

```json
{
  "day": 4,
  "dest": "photos/baikal-rail/day04/foo-downloaded.jpg",
  "filename": "foo-downloaded.jpg",
  "hash": "sha256...",
  "drive_file_id": "abc123",
  "source_folder": "Day 04 - 景點名",
  "synced_at": "2026-07-13T10:00:00+00:00",
  "status": "imported"
}
```

### status 值

| status | 意義 |
|--------|------|
| `seeded_existing` | 建立 manifest 時專案內已有圖片 |
| `imported` | 本次從 Drive 新匯入 |

### review_required 原因

| reason | 意義 |
|--------|------|
| `no_day_folder_match` | 路徑無 `Day XX - 景點名` 資料夾 |
| `no_landmark_match_in_day_md` | Day 可解析但資料夾名對不上 dayXX.md 標題 |
| `invalid_image_file` | 下載後非有效圖片 |
| `no_download_url` | gdown 未提供下載 URL |

---

## Incremental Sync

去重機制（可重複執行、安全）：

1. **`drive_file_id`** — 已在 `synced`、`source_inventory` 或 `review_required` 中 → 跳過
2. **dest 檔案存在** — `photos/baikal-rail/dayXX/*.jpg` 已存在 → 跳過，不覆寫
3. **SHA-256 hash** — 與 manifest 中任一 hash 相同 → 跳過重複內容
4. **dayXX.md** — 僅在 landmark 標題**尚無** `### ![...]` 時插入引用

```bash
# 每日同步
python3 scripts/sync_baikal_photos.py

# 預覽（不寫入、不 build）
python3 scripts/sync_baikal_photos.py --dry-run

# 跳過 Surge
python3 scripts/sync_baikal_photos.py --skip-deploy
```

**注意**：不得使用本機 `Siberian_Railway_Landmarks` 作為 Drive 失敗時的 fallback。

---

## Review Required

當 AI / 腳本**無法可靠判定 Day 或景點**時，檔案進入 `review_required`，**不會下載到 `photos/`**。

常見案例：

- Drive 路徑為 `0711/`、`0712/` 等日期資料夾（目前 15 張 Baltic 照片）
- 資料夾名與 `dayXX.md` landmark 標題不符

### 處理步驟

1. 執行 sync，檢視 Report §3 或 `photo-sync.json` → `review_required`
2. **方案 A**：在 Drive 將照片移至正確 `Day XX - 景點名` 資料夾，刪除 manifest 中該項的 `review_required` 紀錄（或保留，腳本會因 drive_file_id 已記錄而跳過 — 需移除 review 項並清除 drive_file_id 才會重試）
3. **方案 B**：手動下載至 `photos/baikal-rail/dayXX/`，更新 `dayXX.md`，在 `synced[]` 新增紀錄（含 hash）避免下次重複

> **重試提示**：若已從 Drive 修正資料夾後要重新匯入，須自 `review_required` 移除該 `drive_file_id` 條目。

---

## Daily Workflow

```text
1. 使用者上傳照片至 Drive（依 DRIVE_FOLDER_CONVENTION.md 命名資料夾）
2. python3 scripts/sync_baikal_photos.py
3. 檢視 Sync Report
   - New imported > 0 → 確認 dist 預覽
   - Review Required > 0 → 人工整理 Drive 或手動匯入
   - Gray cards → 對照 dayXX.md 缺圖 landmark
4. （可選）Surge 自動部署至 cluttered-breath-prototype.surge.sh
```

---

## Failure Recovery

### Drive 存取失敗

Report 顯示 `Drive Access: BLOCKED`。依序檢查：

**方案 A — gdown**（最簡單）

- 共用資料夾設為「知道連結的任何人可檢視」
- `pip3 install gdown`

**方案 B — Google Drive API**

1. Google Cloud Console 建立專案，啟用 Drive API
2. Service Account JSON → `content/baikal-rail/source/google-service-account.json`（勿提交 git）
3. 將 SA  email 加入 Drive 共用（檢視者）
4. `photo-sync-config.json` 加入 `"credentials": "content/baikal-rail/source/google-service-account.json"`

**方案 C — rclone**

```bash
rclone config
# photo-sync-config.json: "rclone_remote": "gdrive:SharedFolderName"
```

### Build / Deploy 失敗

- Build 失敗：先 `python3 scripts/build_prototype.py` 單獨排查
- Surge CLI crash：為 CLI 已知問題；可 `--skip-deploy`，手動 `surge dist-preview-deploy cluttered-breath-prototype.surge.sh`
- 部署前確認 `dist-preview-deploy` 無 0-byte 或 `* 2.jpg` 重複檔名

### 中斷後恢復

Manifest 在每次成功 sync 後更新。中斷後直接重跑即可；已記錄的 `drive_file_id` 不會重複下載。

---

## Build

```bash
python3 scripts/build_prototype.py
```

- 輸出：`dist-prototype/`
- **不修改** `scripts/build.py` 或 `scripts/build_prototype.py`

Sync 腳本在 import 後可自動執行 build 並檢查：

- 缺圖、壞圖、壞連結
- `dist-prototype/trips/baikal-rail.html` 存在且非空
- dist 完整性（index.html、base.css）

---

## Deploy

檢查全部 PASS 後（可用 `--skip-deploy` 略過）：

1. 從 `dist-prototype/` 複製 HTML/CSS 與引用的 `photos/` → `dist-preview-deploy/`
2. `sips` 壓縮（最長邊 1200px、JPEG 品質 82）
3. `surge dist-preview-deploy cluttered-breath-prototype.surge.sh`

預覽：https://cluttered-breath-prototype.surge.sh/

---

## 約束（必須遵守）

- 僅修改 `baikal-rail` 相關檔案
- 不重新命名既有圖片
- 不覆寫 `dayXX.md` 中已有 `![...]` 的手動編輯
- 不重複下載已記錄於 manifest 的檔案
- 不修改 `scripts/build.py`、`scripts/build_prototype.py`、templates、base.css、其他 trip
