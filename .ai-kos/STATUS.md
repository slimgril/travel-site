# STATUS — travel-site

最後更新：2026-07-24（晚間 Handoff：足跡圖國名排版＋三原則入規）

## 2026-07-24 晚 — 足跡圖標籤＋圖檔三原則

| 項目 | 狀態 |
|------|------|
| **足跡圖** | `baikal-route-map.svg`：中國貼底＋字距；蒙古左側直排；國名 46px；返程航線黃 |
| **三原則** | ①原圖不改 ②同圖不兩處 ③國名≥站名×2 → `CLAUDE.md`＋`.cursor/rules/bingge-photo-rules.mdc`＋父層 `旅遊/CLAUDE.md` |
| **Commit** | 進行中（本 Handoff） |

26-07-24 晚 — 足跡圖標籤＋圖檔三原則

| 項目 | 狀態 |
|------|------|
| **足跡圖** | `baikal-route-map.svg`：中國貼底＋字距；蒙古左側直排；國名 46px；返程航線黃 |
| **三原則** | ①原圖不改 ②同圖不兩處 ③國名≥站名×2 → `CLAUDE.md`＋`.cursor/rules/bingge-photo-rules.mdc`＋父層 `旅遊/CLAUDE.md` |
| **Commit** | 進行中（本 Handoff） |

## 2026-07-24 — Resume：不修圖政策＋足跡圖莫斯科→北京飛航

| 項目 | 狀態 |
|------|------|
| **政策** | 斌哥旅遊書照片**禁止修圖**；只忠實入站原圖（部署可 sips 縮圖，非美顏／AI 修圖） |
| **天次對照** | 07/13=Day3｜**07/14=Day4**｜**07/15=Day5**（非「七月十四＝第五天」） |
| **Day 5** | 已入站 10 張原圖→`photos/bldh-trio/day05/`＋`day05.md` |
| **Day 4 回饋** | 已刪重複「石階」；「磚拱廊」→「圓拱窗」向外望 |
| **足跡圖** | `baikal-route-map.svg`：莫斯科＝鐵路終點；新增紫虛線弧 **D20 ✈ 飛回北京**＋中點小飛機 |
| **Build** | PASS（`build_prototype.py`） |
| **Deploy** | PASS（Node 20＋surge · `dist-surge-upload` 40.3MB） |
| **Commit** | Pending |

## 2026-07-24 — Baltic Day 5（07/15）＋Day4 回饋修正

| 項目 | 狀態 |
|------|------|
| **Trip** | Baltic（`bldh-trio`）Day 5 ｜ 07/15 十字架山 → 隆黛爾 → 里加 |
| **Drive** | SSOT `0715/` 14 檔已下載；誤標 `IMG_20260715_*`（EXIF 實為 07/14）→ `review/day04-export-0715/` |
| **Day4 回饋** | 刪同景「石階」卡；「磚拱廊」→「圓拱窗」敘事 |
| **New Photos** | **10** 張 → `photos/bldh-trio/day05/` |
| **Travel Notes** | `day05.md` 10 卡 |
| **Skipped** | 團體花園照、宮殿戲水合影、白廳模特拍攝；`IMG_20260722_*` 仍 review |
| **莫斯科地圖** | 已補強：莫斯科鐵路終點＋飛回北京弧線 |
| **Build** | PASS |
| **Deploy** | 見上方 Resume 區塊 |
| **Live** | https://cluttered-breath.surge.sh/trips/bldh-trio.html#d5 |
| **Commit** | Pending |

## 2026-07-23 — Day 4＋回饋修正（handoff）

| 項目 | 狀態 |
|------|------|
| **Trip** | Baltic Day 4 已上線；Day1 meta／Day3 文學街／Day1 額外推薦 tip 已修 |
| **Build** | PASS |
| **Deploy** | PASS（Node 20＋surge@0.23.1＋`dist-surge-upload` 49MB） |
| **Live** | https://cluttered-breath.surge.sh/trips/bldh-trio.html |
| **Commit** | Pending |
| **Next** | Day 5（07/15）；可選全畫質 redeploy／commit+push |

## 2026-07-23 — Baltic Day 4（07/14）特拉凱 → 考納斯

| 項目 | 狀態 |
|------|------|
| **Trip** | Baltic（`bldh-trio`）Day 4 ｜ 07/14 水中古堡 |
| **Drive** | `0714/` 列出 24 檔；本次入站明確屬 07/14 的旅人照 |
| **New Photos** | **7** 張 → `photos/bldh-trio/day04/` |
| **Travel Notes** | `day04.md` 9 卡 |
| **Pending** | `IMG_20260715_*` → Day 5 |

## 2026-07-20 — Day 2 構圖 + 立陶宛黑膠民謠（定稿）

| # | 項目 | 狀態 |
|---|------|------|
| 1 | Day 1 黑圖救援：sandbox 外重打包＋正式 redeploy | Done（已上線） |
| 2 | Day 2 描述／小物重疊修復（souvenirs 改 grid 第二列） | Done（已上線） |
| 3 | 立陶宛小物集合圖入站＋斜放 −30°；尺寸＋⅓ | Done（已上線） |
| 4 | 黑膠唱片組件＋唱針動畫；尺寸 −¼ | Done（已上線） |
| 5 | 15s 民謠剪輯腳本（淡入／淡出）＋播放器串接 | Done（已上線） |
| 6 | Day 2 三塊往中收攏、邊距加大 | Done（已上線・使用者定稿） |
| 7 | 修復唱片消失（display:block）＋音檔部署 404（打包掃 `/photos/`） | Done（已上線） |
| 8 | 工作日誌：`HISTORY.md`＋本 STATUS＋父層斷點＋`.claude-progress` | Done |
| **Live** | 使用者確認「很完美／超出預期」；音檔 HTTP 200 |
| **Production** | https://cluttered-breath.surge.sh/trips/bldh-trio.html#d2 |

## 2026-07-19 — Baltic Day 3 維爾紐斯（Daily Travel Update）

| 項目 | 狀態 |
|------|------|
| **Trip** | Baltic（`bldh-trio`）Day 3 ｜ 07/13 維爾紐斯 |
| **Drive** | SSOT `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`（[20260711波羅的海](https://drive.google.com/drive/folders/1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD)） |
| **Sync** | 補下載先前 rate-limit 的照片；不確定／與既有卡同景重複者不入站 |
| **New Photos** | 4 張 → `photos/bldh-trio/day03/`（sips 1920/q88）：大教堂柱廊、佔領博物館大門、櫻桃酒店內、街角乾杯 |
| **Travel Notes** | `day03.md` 新增 4 卡；憲法牆一卡併寫 ELVIS；移除同景重複卡 |
| **原則** | 一圖不拆兩卡（`CLAUDE.md` + `CONTENT_STYLE.md`） |
| **Build** | PASS — `build_prototype.py`（缺圖 0） |
| **Deploy** | PASS — surge → cluttered-breath.surge.sh |
| **Live** | Homepage / bldh-trio / 新圖 HTTP 200 |
| **Commit** | 本機 `316c9c0`、`5a912b1` + 未 commit：CLAUDE／CONTENT_STYLE／憲法牆併寫等 |
| **Push** | Pending |

## 2026-07-18 — Baltic Day 1 黑圖修復（redeploy）

| 項目 | 狀態 |
|------|------|
| **問題** | Day 1 多數圖灰卡／全黑 — 先前在 sandbox 內跑 `sips` 導致 |
| **Mapping** | `day01.md` ↔ `photos/bldh-trio/day01/` 14 張檔名正確，非缺圖 |
| **Fix** | sandbox **外** 重跑 `package_preview_deploy`（308 檔／302 圖） |
| **Build** | PASS — `build_prototype.py`（缺圖 0） |
| **Deploy** | PASS — `npx surge dist-preview-deploy cluttered-breath.surge.sh` |
| **Live** | Day 1 抽查（含先前黑圖）HTTP 200、非黑圖 |
| **Commit** | SKIP（僅 rebuild／redeploy；內容未改） |
| **Git** | `main` ahead 1（`64654fb` magazine template，未 push） |

## 2026-07-17 — Baltic Day 3 維爾紐斯（Daily Travel Update）

| 項目 | 狀態 |
|------|------|
| **Trip** | Baltic（`bldh-trio`）Day 3 ｜ 07/13 維爾紐斯首都深度遊 |
| **Drive sync** | `0713/` 23/27 檔已同步（4 張 07/17 櫻桃酒店家 rate-limit，review_required 延後） |
| **New Photos** | 15 張旅人照片入站 `photos/bldh-trio/day03/`（sips 1920/q88） |
| **Travel Notes** | day03.md 由 2 卡 → 17 卡，旅行札記 v1.0（對岸共和國、聖安娜/伯納迪內、大教堂廣場、格迪米納斯塔俯瞰、佔領博物館、聖彼得保羅/聖卡濟米爾、櫻桃酒） |
| **Hero** | 聖安娜教堂（斌哥入鏡） |
| **Build** | PASS — `build_prototype.py`（缺圖 0） |
| **Deploy** | PASS — `dist-preview-deploy`（308 檔/302 圖）→ cluttered-breath.surge.sh |
| **Live** | Homepage / bldh-trio / Day 3 新圖 HTTP 200 |
| **Commit** | `313d0d5`（origin/main） |

- 已完成札記：day01、day03、day04
- review_required：4（`IMG_20260717_1620xx`–`1627xx` 櫻桃酒專賣店，Drive rate-limit 未下載；日期屬 07/17 需人工確認歸屬）



## 2026-07-16 — Operational Phase

| 項目 | 值 |
|------|-----|
| **Phase** | **Operational**（正式） |
| **原則** | AI-KOS 服務旅行書；旅行書不再服務 AI-KOS |
| **自** | 2026-07-17 起每日預設 = Daily Travel Update |
| **Integrity baseline** | `6779dac` on `origin/main` |
| **Production** | https://cluttered-breath.surge.sh/ |
| **Handoff** | 固定營運摘要（見 `DAILY_TRAVEL_UPDATE.md`） |

## 2026-07-16 — Workspace Integrity（Priority 0）

| 項目 | 結果 |
|------|------|
| **Cursor folderUri** | Documents Canonical — PASS |
| **Git toplevel** | `/Users/mac/Documents/Projects/旅遊/travel-site` — PASS |
| **Desktop `travel-site/` 假專案** | 已刪除 — PASS |
| **Missing git blobs** | 自 `origin/main` 還原 6 張照片 — PASS |
| **Deploy domain config** | `cluttered-breath.surge.sh`（sync config + REPOSITORY） |
| **SSOT** | 新增 `.ai-kos/WORKSPACE.md` |

## 2026-07-16 — Canonical workspace path（Documents ONLY）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

| 項目 | 值 |
|------|-----|
| **Active project root** | `/Users/mac/Documents/Projects/旅遊/travel-site/` |
| **Workspace parent** | `/Users/mac/Documents/Projects/旅遊/` |
| **Git HEAD** | sync with `origin/main`（見 `git status`） |
| **Desktop residue** | `~/Desktop/旅遊/` 僅導向文件（無 `travel-site/` 子目錄） |
| **Cursor 修正** | 必須 **File → Open Folder** → Canonical Root |

## 2026-07-16 — Baltic resume（開工 08:00）

| 項目 | 狀態 |
|------|------|
| **Drive scan** | OK（gdown）— Shared Folder 共 18 檔；無新 Day 資料夾候選 |
| **bldh-trio 增量** | 無新旅人照片可入站（0711–0714 已入 day01／03／04 或為同圖原檔） |
| **Build** | PASS — `python3 scripts/build_prototype.py`（缺圖 0） |
| **Deploy / Commit** | SKIP — 無札記變更；待你指示 |
| **本機修復** | 自 `cooked/matched/` 補回 `tallinn-town-hall-square.jpg`、`tartu-old-town.jpg`；baikal 3 張缺圖以同目錄備援檔補檔名 |

- 已完成札記：day01、day03、day04
- 待 Drive 新圖：day02（維爾紐斯抵達）、day05（十字架山／隆黛爾）起
- review_required：19（日期資料夾 `0711/`–`0714/`，非 `Day XX` 結構）

## 2026-07-16 — Baltic daily travel update（稍早）

| 項目 | 狀態 |
|------|------|
| **Production URL** | https://cluttered-breath.surge.sh/ |
| **Build** | PASS — `python3 scripts/build_prototype.py`（bldh-trio 缺圖 0；baikal 缺圖 3 為既有） |
| **Deploy** | PASS — `npx surge dist-preview-deploy cluttered-breath.surge.sh`（global `surge` 首次失敗） |
| **Live checks** | Homepage、`/trips/bldh-trio.html`、5 張新圖 HTTP 200 |

- 札記：`content/bldh-trio/day01.md`、`day03.md`、`day04.md`
- 新圖：`hippodrome-obelisk-sunset.jpg`；立陶宛午餐／晚餐；考納斯城堡 2 張
- Drive 本機鏡像：`content/bldh-trio/source/drive-originals/0712/`（13）、`0713/`（2）
## 2026-07-15 — Desktop 全面整理

- 桌面所有專案與檔案移入 `~/Documents/Projects/`（見 `DESKTOP_INDEX.md`）
- 旅遊專案新路徑：`~/Documents/Projects/旅遊/travel-site/`
- 健康管理：`~/Documents/健康管理/`

## Baikal Rail 照片路徑整理（2026-07-15）

**Cyprian Railroad 20 日**（slug `baikal-rail`）本機照片已集中於專案內，桌面不再保留暫存夾。

| 路徑 | 用途 |
|------|------|
| `photos/baikal-rail/day01~20/` | 網站正式用圖（235 張，build 缺圖 0） |
| `content/baikal-rail/source/Siberian_Railway_Landmarks/` | 下載暫存區（自 Desktop 移入；新圖先放此處） |

- 2026-07-15：153 張有效照片自暫存區搬入 `photos/baikal-rail/`；暫存資料夾整體移入 `source/`
- Resume 時查圖：見 `.ai-kos/INFRASTRUCTURE.md` § Local Photo Paths

## Content Style v1.0（2026-07-13）

**旅行札記** — 全站預設文風，由「旅遊景點介紹」轉型為旅行者第一人稱體驗敘事。

| 項目 | 狀態 |
|------|------|
| **規範文件** | `.ai-kos/CONTENT_STYLE.md` |
| **採用政策** | 增量更新；觸及才改寫，不批次重寫舊內容 |
| **試點** | `content/bldh-trio/day01.md`（Baltic Day 1，11 區塊已改寫） |

## Travel Site v0.3 Release (2026-07-13)

**正式瀏覽版** — 供斌哥 review 的三趟旅程原型站。

| 項目 | 狀態 |
|------|------|
| **Release URL（當時）** | cluttered-breath-prototype.surge.sh（**legacy；已 BLOCKED**） |
| **現行 Production** | https://cluttered-breath.surge.sh/ |
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
- **4 灰卡已修復**（`source/Siberian_Railway_Landmarks` → `photos/baikal-rail/`）：
  - Day 4：`mongolia-folk-dance-morin-khuur-downloaded.jpg`（IMG_2617, 1920×1440）
  - Day 6：`ulan-ude-city-center-downloaded.jpg`（IMG_2623, 1024×768）
  - Day 11：`novosibirsk-local-history-museum-downloaded.jpg`（IMG_2635）
  - Day 11：`novosibirsk-railway-museum-downloaded.jpg`（IMG_2629）
- Build 驗證：PASS（missing_image / broken_image / broken_link / html_build / dist_integrity）
- Deploy：PASS — `surge dist-preview-deploy cluttered-breath-prototype.surge.sh`（2026-07-13）

### 已知限制

- **現行重新部署**：`npx surge dist-preview-deploy cluttered-breath.surge.sh`
- 勿再使用 `cluttered-breath-prototype.surge.sh`（legacy BLOCKED）

---

## 專案概況


## GitHub Remote（2026-07-13）

| 項目 | 值 |
|------|-----|
| **Repository** | https://github.com/slimgril/travel-site.git |
| **Remote** | `origin` |
| **Default branch** | `main` |
| **Deployment** | https://cluttered-breath.surge.sh/ |
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
| **Release URL（當時）** | cluttered-breath-prototype.surge.sh（**legacy BLOCKED**） |
| **現行 Production** | https://cluttered-breath.surge.sh/ |
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
curl -sI https://cluttered-breath.surge.sh/
curl -sI https://cluttered-breath.surge.sh/trips/baikal-rail.html
```

### 已知問題（2026-07-13 Mapping Report 後）

1. **15 張 Drive 照片待人工歸類**（`photo-sync.json` → `review_required`；路徑為 `0711/`、`0712/` 日期資料夾，無 Day 結構）
2. **11 張磁碟備援圖未引用**（舊版/重複檔留存於 `photos/baikal-rail/`，不影響 build 或 HTML 輸出）

### 相關文件

- 操作手冊：`content/baikal-rail/source/PHOTO_SYNC.md`
- Drive 資料夾慣例：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
- 設定：`content/baikal-rail/source/photo-sync-config.json`
- 腳本：`scripts/sync_baikal_photos.py`
