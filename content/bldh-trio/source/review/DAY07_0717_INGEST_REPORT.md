# Baltic Day 7（07/17）讀取與入站報告

**日期：** 2026-07-26  
**旅程：** `bldh-trio`｜Day 7｜07/17（五）｜里加 → 錫古爾達 → 塔圖 → 維爾揚迪  
**指令來源：** Drive `0717/CLAUDE.txt`＋專案 Photos SSOT／有圖全上  
**本機原圖：** `content/bldh-trio/source/drive-originals/0717/`

---

## 1. Cloud CLAUDE 指令（已採納）

| 檔案 | 要點 |
|------|------|
| `IMG_20260726_112851` | 午餐是**拉脫維亞式火雞餐** |
| `IMG_20260726_120351` | 顛倒屋內部家具陳設**非常真實** |
| `IMG20260717220426` | 維爾揚迪湖跳台：上層大人、下層小朋友；湖畔運動氣息 |
| `VID_20260717_154807` | 動畫：登上圖雷達主塔俯瞰加烏亞河谷（**已入站**點擊播放卡） |

---

## 2. Drive 同步

| 項目 | 結果 |
|------|------|
| SSOT | `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD` → `0717/` |
| Drive 清單 | 21 項（19 JPG＋`CLAUDE.txt`＋1 MP4） |
| 已下載照片 | **19／19** JPG |
| 影片 | `VID_20260717_154807.mp4` **已入站** → `photos/.../turaida-tower-gauja.mp4`（原片 52MB 存 drive-originals；站上 9.4MB 部署壓縮） |

---

## 3. 入站一覽（19 卡 · 時間序）

| # | 原檔 | 時間 | 辨識 | 入站檔名 |
|---|------|------|------|----------|
| 1 | `IMG20260717101827` | 10:18 | 圖雷達木造教堂 | `turaida-wooden-church.jpg` |
| 2 | `IMG_20260726_115300` | 10:54 | 塔樓眺望加烏亞河谷＋斌哥 | `turaida-tower-view-bingge.jpg` |
| 3 | `IMG_20260726_115206` | 11:10 | TURAIDAS PILS 招牌＋斌哥 | `turaida-pils-sign-bingge.jpg` |
| 4 | `IMG_20260726_114915` | 11:53 | 古特曼洞穴岩壁題字＋斌哥 | `gutmann-cave-inscriptions-bingge.jpg` |
| 5 | `IMG_20260726_112851` | 午 | 拉脫維亞式火雞午餐拼圖 | `latvia-turkey-lunch.jpg` |
| 6 | `IMG20260717170546` | 17:05 | 顛倒屋外觀（Tartu 標註） | `upside-down-house-exterior.jpg` |
| 7 | `IMG_20260726_120351` | — | 顛倒屋內部四格拼圖 | `upside-down-house-interior-collage.jpg` |
| 8 | `IMG_20260726_114014` | 17:54 | AHHAA 火箭＋斌哥 | `ahhaa-rocket-bingge.jpg` |
| 9 | `IMG20260717181101` | 18:11 | 塔圖市政廳廣場 | `tartu-town-hall-square.jpg` |
| 10 | `IMG20260717181436` | 18:14 | 接吻學生噴泉＋斌哥 | `kissing-students-fountain-bingge.jpg` |
| 11 | `IMG20260717181736` | 18:17 | 塔圖大學主樓 | `tartu-university.jpg` |
| 12 | `IMG20260717182529` | 18:25 | 巨釘雕塑 | `tartu-thumbtack-sculpture.jpg` |
| 13 | `IMG20260717183034` | 18:30 | 主教座堂遺址＋斌哥 | `tartu-cathedral-ruins-bingge.jpg` |
| 14 | `IMG20260717183529` | 18:35 | 主教座堂塔樓廊道＋斌哥 | `tartu-cathedral-tower-bingge.jpg` |
| 15 | `IMG20260717184720` | 18:47 | 塔圖市政廳＋斌哥 | `tartu-town-hall-bingge.jpg` |
| 16 | `IMG20260717220426` | 22:04 | 維爾揚迪湖跳台 | `viljandi-lake-diving-board.jpg` |
| 17 | `IMG20260717222637` | 22:26 | 人與狗雕像 | `viljandi-man-and-dog-sculpture.jpg` |
| 18 | `IMG20260717222731` | 22:27 | 維爾揚迪水塔 | `viljandi-water-tower.jpg` |
| 19 | `IMG20260717225436` | 22:54 | 貓雕像＋斌哥 | `viljandi-cat-sculpture-bingge.jpg` |

**備註：** 行程原文「顛倒屋＝Smārde」；實拍浮水印為 Tartu 一帶顛倒屋，札記依實拍。

---

## 4. 實作結果

| 項目 | 結果 |
|------|------|
| 政策 | 資料夾內照片**全部**上站（19 JPG） |
| `day07.md` | 19 卡；Cloud CLAUDE 要點已寫入午餐／顛倒屋內／湖跳台／塔樓眺望 |
| Build | PASS（19 day07 refs，0 missing） |
| Deploy bundle | `dist-preview-deploy/`（363 files / 356 images） |
| Deploy | （進行中／見營運摘要） |
