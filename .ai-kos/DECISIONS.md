# DECISIONS — travel-site

架構與流程決策紀錄。新增決策時在最上方追加條目。

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
