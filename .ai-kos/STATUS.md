# STATUS — travel-site

最後更新：2026-07-13（GitHub remote `origin` → slimgril/travel-site）

## Travel Site v0.3 Release (2026-07-13)

**正式瀏覽版** — 供斌哥 review 的三趟旅程原型站。

| 項目 | 狀態 |
|------|------|
| **Release URL** | https://cluttered-breath-prototype.surge.sh/ |
| **Build** | PASS — `python3 scripts/build_prototype.py`（2026-07-13 Mapping Report：3 trips, 0 missing/broken images, 0 broken links, 0 gray cards） |
| **Deploy bundle** | `dist-preview-deploy/` — 298 files, ~94 MB（sips 壓縮後） |
| **Live checks** | Homepage / Baltic / Baikal Rail — HTTP 200 |

### 收錄旅程

| # | Slug | 名稱 | 天數 | 狀態 | 照片（source / deploy bundle） |
|---|------|------|------|------|-------------------------------|
| 001 | `shanxi` | 山西 | 15 | done | 163 / 192 |
| 002 | `bldh-trio` | 波羅的海三小國 | 11 | upcoming | 55 / 28 |
| 003 | `baikal-rail` | 西伯利亞大鐵路 | 20 | upcoming | 82 / 71 |

### 照片同步能力（v0.3 新增）

- **Google Drive Incremental Sync** — `scripts/sync_baikal_photos.py`
- **Photo Sync Manifest** — `content/baikal-rail/source/photo-sync.json`（82 synced, 15 review_required）
- 操作手冊：`content/baikal-rail/source/PHOTO_SYNC.md`

### Baikal Rail Release Ready（2026-07-13 Mapping Report 4d129fde）

| 項目 | 數量 |
|------|------|
| 古蹟 landmark 卡 | 71（20 天） |
| Markdown / HTML 圖片 ref | 71（`background-image`） |
| `photos/baikal-rail/` 磁碟檔 | 82（全部通過 `is_valid_image_file`） |
| 缺圖 / 壞圖 / 假圖 | 0 / 0 / 0 |
| `photo-sync.json` synced | 82 |
| `review_required` | 15（Drive `0711/`、`0712/` 日期資料夾） |
| 灰卡 | 0（原 4 張已配圖） |
| 磁碟未引用備援圖 | 11（舊版/重複檔，不影響 build） |

- 20 天行程 HTML 完整，全 20 天 nav 可達
- **4 灰卡已修復**（Desktop `Siberian_Railway_Landmarks` → `photos/baikal-rail/`）：
  - Day 4：`mongolia-folk-dance-morin-khuur-downloaded.jpg`（IMG_2617, 1920×1440）
  - Day 6：`ulan-ude-city-center-downloaded.jpg`（IMG_2623, 1024×768）
  - Day 11：`novosibirsk-local-history-museum-downloaded.jpg`（IMG_2635）
  - Day 11：`novosibirsk-railway-museum-downloaded.jpg`（IMG_2629）
- Build 驗證：PASS（missing_image / broken_image / broken_link / html_build / dist_integrity）
- Deploy：PASS — `surge dist-preview-deploy cluttered-breath-prototype.surge.sh`（2026-07-13）

### 已知限制

- 重新部署指令：`surge dist-preview-deploy cluttered-breath-prototype.surge.sh`

---

## 專案概況


## GitHub Remote（2026-07-13）

| 項目 | 值 |
|------|-----|
| **Repository** | https://github.com/slimgril/travel-site.git |
| **Remote** | `origin` |
| **Default branch** | `main` |
| **Deployment** | https://cluttered-breath-prototype.surge.sh/ |
| **紀錄** | `REPOSITORY.md` |

靜態旅遊網站，以 Markdown + 照片建置多趟旅程。主要 build 入口為 `scripts/build.py`（正式）與 `scripts/build_prototype.py`（原型預覽）。

## Google Drive Incremental Photo Sync — 已完成

Baikal Rail（`baikal-rail`）已具備 Google Drive 增量照片同步能力。

### 能力

| 能力 | 說明 |
|------|------|
| **Incremental Sync** | 比對 `photo-sync.json` 中的 `drive_file_id` 與 SHA-256 hash，只處理新檔 |
| **Manifest** | `content/baikal-rail/source/photo-sync.json` 記錄已同步、來源清單、待審項目 |
| **Review Required** | 路徑不符合 `Day XX - 景點名` 或無法對應 landmark 時，寫入 `review_required`，不自動歸類 |
| **Build Integration** | 同步後可選執行 `build_prototype.py` 與 dist 完整性檢查 |
| **Deploy Integration** | 檢查 PASS 後打包 `dist-preview-deploy` 並 Surge 部署 |

### 限制

- Drive 共用資料夾必須可存取（gdown / Google Drive API / rclone 擇一）
- 無法在 trip 未知或路徑無 Day 資料夾時自動匯入；須人工整理 Drive 或手動匯入
- Surge CLI 偶發 crash（`filename` 處理錯誤）為 CLI 問題，非本專案邏輯；網站仍可透過先前成功部署存取

### 目前狀態（2026-07-13 Mapping Report）

- 已同步：82 張（manifest `synced`，全部通過 JPEG/PNG header 驗證）
- Markdown 引用：71 張；HTML 輸出：71 張 `background-image` ref（一致）
- 待審：`review_required` 15 張（Drive 路徑為 `0711/`、`0712/` 日期資料夾，非 Baikal Day 結構）
- 灰卡：0（原 4 張已從 Desktop 配圖）
- 磁碟備援圖：11 張未在 markdown 引用（如 `chinggis-khaan-statue.jpg`、`erdene-zuu-monastery.jpg` 等舊版/重複檔）

## Baikal Rail Release Ready — v1（2026-07-13）

正式瀏覽版 release 驗證完成；build 通過，線上站點可正常瀏覽。

| 項目 | 狀態 |
|------|------|
| **Release URL** | https://cluttered-breath-prototype.surge.sh/ |
| **Build** | PASS（2026-07-13 Mapping Report：`python3 scripts/build_prototype.py` → `dist-prototype/`） |
| **Validation** | PASS — 0 missing image、0 broken image、0 broken link、0 gray card；全 20 天 nav 可達 |
| **Deploy** | PASS — Surge 部署成功（298 檔、94.1 MB） |
| **Baikal 圖片** | 71 ref（HTML）/ 82 檔（磁碟）/ 71 landmark / 0 灰卡 |
| **review_required** | 15 張（`photo-sync.json`，待人工歸類） |
| **打包** | `dist-preview-deploy/` 298 檔、sips 壓縮 292 張 |

### 驗證指令（可重跑）

```bash
python3 scripts/build_prototype.py
python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); from sync_baikal_photos import run_checks, SyncReport; r=SyncReport(); ok=run_checks(r); print(r.checks); sys.exit(0 if ok else 1)"
curl -sI https://cluttered-breath-prototype.surge.sh/
curl -sI https://cluttered-breath-prototype.surge.sh/trips/baikal-rail.html
```

### 已知問題（2026-07-13 Mapping Report 後）

1. **15 張 Drive 照片待人工歸類**（`photo-sync.json` → `review_required`；路徑為 `0711/`、`0712/` 日期資料夾，無 Day 結構）
2. **11 張磁碟備援圖未引用**（舊版/重複檔留存於 `photos/baikal-rail/`，不影響 build 或 HTML 輸出）

### 相關文件

- 操作手冊：`content/baikal-rail/source/PHOTO_SYNC.md`
- Drive 資料夾慣例：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
- 設定：`content/baikal-rail/source/photo-sync-config.json`
- 腳本：`scripts/sync_baikal_photos.py`
