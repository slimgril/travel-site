# STATUS — travel-site

最後更新：2026-07-13

## 專案概況

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

### 目前狀態（2026-07-13）

- 已同步：78 張（manifest `synced`）
- 待審：`review_required` 15 張（Drive 路徑為 `0711/`、`0712/` 日期資料夾，非 Baikal Day 結構）
- 灰卡：Day 4、Day 6（烏蘭烏德）、Day 11（地方誌博物館、火車博物館）共 4 個 landmark 尚缺圖

### 相關文件

- 操作手冊：`content/baikal-rail/source/PHOTO_SYNC.md`
- Drive 資料夾慣例：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
- 設定：`content/baikal-rail/source/photo-sync-config.json`
- 腳本：`scripts/sync_baikal_photos.py`
