# HISTORY

## 2026-07-16 — Baltic daily travel update

- **Production URL**: https://cluttered-breath.surge.sh/
- 同步 5 張 bldh-trio 照片 + 更新 day01／day03／day04 札記
- Build PASS：`scripts/build_prototype.py`；deploy bundle `dist-preview-deploy/`（343 files, sips）
- Deploy：global `surge` 失敗；`npx surge dist-preview-deploy cluttered-breath.surge.sh` 成功
- Live 驗證：首頁、bldh-trio 頁、5 張新圖 HTTP 200
- Drive 本機：`0712/` 13 檔、`0713/` 2 檔；`0712/` 內 3 張 7/13 凌晨圖尚未入 `photos/`

## 2026-07-15 — Desktop 全面整理

- 桌面 28 項專案／檔案全部移入 `~/Documents/Projects/` 及對應子資料夾
- 索引文件：`~/Documents/Projects/DESKTOP_INDEX.md`
- 旅遊專案：`~/Documents/Projects/旅遊/travel-site/`
- 桌面僅剩系統檔（`.DS_Store`、`.localized`、Google Drive 暫存）

## 2026-07-15 — Baikal Rail 照片暫存區移入專案

- **Cyprian Railroad 20 日**（`baikal-rail`）桌面暫存夾 `Siberian_Railway_Landmarks` 整體移入 `content/baikal-rail/source/`
- 153 張有效照片搬入 `photos/baikal-rail/day02~day19/`；網站正式用圖現共 235 張，build 缺圖 0
- 更新路徑紀錄：`.ai-kos/INFRASTRUCTURE.md`、`STATUS.md`、`INDEX.md`、`PHOTO_SYNC.md`、`DRIVE_FOLDER_CONVENTION.md`
- **Resume 規則**：查圖先看 `photos/baikal-rail/dayXX/`；新下載暫存放 `source/Siberian_Railway_Landmarks/`；**勿查 Desktop**

## 2026-07-13 — Travel Site v0.3 Release

- **Release URL**: https://cluttered-breath-prototype.surge.sh/
- 三趟旅程正式可瀏覽：山西 (#001)、波羅的海三小國 (#002)、西伯利亞大鐵路 (#003)
- Build PASS：`scripts/build_prototype.py` → 3 trips, 0 missing images
- Deploy bundle：`dist-preview-deploy/`（294 files, ~93 MB, sips 壓縮）
- 驗證 PASS：broken image/link 0、Baikal Day 1–16、homepage journey cards、mobile viewport
- 新增 Google Drive 增量照片同步 + manifest（見下方條目）
- Baikal Rail release ready：78 張已同步；4 gray card、15 review_required 為已知待辦
- Surge redeploy 本次 CLI 失敗；先前部署仍 LIVE（curl HTTP 200）

## 2026-07-13 — Google Drive Incremental Photo Sync（Baikal Rail）

- 完成 `scripts/sync_baikal_photos.py`：Google Drive → 增量同步 → manifest → build 檢查 → deploy 打包
- 建立 manifest：`content/baikal-rail/source/photo-sync.json`（78 張已同步、15 張 review_required）
- 撰寫操作文件：`content/baikal-rail/source/PHOTO_SYNC.md`
- 實作 Review Required 流程：路徑非 `Day XX - 景點名` 時不猜 Day，寫入待審清單
- 設定 Drive 共用資料夾 URL（folder_id `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`）於 `photo-sync-config.json`
- 新增 Drive 資料夾命名慣例：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
- 治理文件：`.ai-kos/STATUS.md`、`.ai-kos/DECISIONS.md` 記錄能力、限制與決策
- 觀察：15 張 Baltic 相關照片因 `0711/`、`0712/` 資料夾結構進入 review_required；4 個 baikal gray card 仍待補圖
- 觀察：Surge CLI 偶發 deploy 失敗，先前部署仍可用

## 2026-07-10 — Homepage Restore And Prototype Packaging Fix

- Restored the homepage hero / About Ben section onto the canonical prototype site.
- Confirmed `bldh-trio` is the canonical Baltic Trio trip; removed the legacy
  `content/baltic.md` path to avoid duplicate `World Journey #002` output.
- Separated homepage portraits in `photos/site/` from trip assets and preserved
  unassigned future-trip assets in `photos/unassigned/`.
- Fixed deployment packaging by filtering hidden files, 0-byte files, and macOS
  duplicate copy names such as `* 2.jpg` / `* 3.jpg`.
- Observation: unclear canonical reference caused agents to patch the wrong
  output, non-target assets were modified during diagnosis, and 0-byte assets
  were not blocked until this fix.
- Deployment observation: Surge may report a generic `filename` processing error
  when the deploy package contains bad assets; validate locally before deploy.
