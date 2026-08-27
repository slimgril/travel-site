# travel-site — Agent guidance

## Workspace（canonical — HARD RULE）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
WORKSPACE PARENT:       /Users/mac/Documents/Projects/旅遊/
FORBIDDEN:              /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
```

**知識讀序（每日／開工必循）：** 本檔（含下方 **Photos SSOT**）→ `.ai-kos/WORKSPACE.md` → `.ai-kos/RESUME_CONTEXT.md` → `.ai-kos/DAILY_TRAVEL_UPDATE.md`

## Photos SSOT — Google Drive 分享資料夾（每日必讀 · HARD RULE）

> **斌哥旅行照片唯一來源（Single Source of Truth）。**  
> Daily Travel Update／開工同步照片時 **必須先讀本節**，直接用此資料夾增量同步。  
> **禁止**再問使用者「分享資料夾在哪」；**禁止**從 Desktop 或其他本機路徑 fallback 匯入。

### 波羅的海三國（2026年7月）

| 項目 | 值 |
|------|-----|
| **名稱** | 20260711波羅的海（根目錄；內含 `0711/`、`0712/`、`0713/`… 子資料夾） |
| **URL** | https://drive.google.com/drive/folders/1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD |
| **Folder ID** | `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD` |
| **狀態** | 已完成 |

### 貝加爾鐵路／西伯利亞大鐵路（2026年8月3-22日）

| 項目 | 值 |
|------|-----|
| **名稱** | 西伯利亞大鐵路 20 日（斌哥每日更新至對應 Day XX folder） |
| **URL** | https://drive.google.com/drive/folders/1VnHEb_UrT7-MMOrTKfh80B6IBFzE6Ty |
| **Folder ID** | `1VnHEb_UrT7-MMOrTKfh80B6IBFzE6Ty` |
| **狀態** | 進行中（Day 02 製作中）|

**政策：**

- 每個行程有獨立的 Shared Folder
- 每次 Resume／Daily Update **直接使用上方對應行程的 URL／ID**，不要求使用者重貼連結
- 斌哥會將每日照片和 CLAUDE 檔案（備註/要求）存入對應的 Day XX folder
- 完整路徑／本機鏡像等細節見 `.ai-kos/INFRASTRUCTURE.md`

## 冰哥／斌哥圖檔與足跡圖三原則（2026-07-24 · HARD RULE）

> Owner 定稿。Agent **不得違反**。

| # | 原則 | 含義 |
|---|------|------|
| **1** | **原圖不可改** | 冰哥／斌哥提供的圖＝**原圖 100% 貼上**。禁止裁切、濾鏡、調色、壓字、AI 改圖、重繪、另存「優化版」取代原圖。 |
| **2** | **同圖不兩處** | **同一張照片不得出現在兩個地方**（兩卡、兩日、地圖＋內文、重複路徑各貼一次等皆禁止）。全站／全書同一檔只准用一次。 |
| **3** | **足跡圖國名 ≥ 站名 ×2** | 示意圖／足跡圖上，**國家名**字級必須至少為**站名**的 **兩倍**（例：站名 17px → 國名 ≥ 34px；現行貝加爾圖國名 46／站名 17）。 |

**執行：**

- 配圖前用檔名／內容檢查是否已在其他 day／卡／頁使用
- 需要「再講一次」→ 只改文字引用，**不要再貼同一張圖**
- 改足跡圖字級時：先看站名（`.sr-mark`／等價），再設國名（`.sr-country`）≥ 2×；不得為塞進區塊而把國名壓到低於 2×

與下方「一圖不拆兩卡」並存：本節第 2 條更硬（連不同敘事也不准同圖兩處）。

## 描述區寫法（2026-07-30 · Owner · HARD — CONTENT_STYLE v1.2）

> 角色：資深旅遊作家。將景點資訊改寫成**一段**旅遊札記。  
> SSOT：`.ai-kos/CONTENT_STYLE.md` v1.2。主站不顯示 emoji／區塊標題。

| # | 規則 |
|---|------|
| 1 | **身在現場**切入——從感官細節開始（光／聲／第一眼）；禁「這是 XXX」開頭 |
| 2 | 資訊**嵌入敘事**，像順口帶出；禁條列歷史／年代／特色 |
| 3 | 禁導覽詞：「值得一遊」「不容錯過」「是 XX 的代表」 |
| 4 | 禁流水帳：「我們去了…然後…接著…」 |
| 5 | 結尾一句個人感受／反思（畫面或幽默）；禁總結式結論 |
| 6 | **4–6 句**，精簡有畫面；禁堆砌形容詞 |

**內部節奏**（v1.1）：當下 → 知識順口帶 → 雜記 → 感受收尾。  
**下一旅程**：`baikal-rail` 每日每張照片同規則。

**定稿範例**（聖靈教堂古鐘）：

> 抬頭的瞬間，金色羅馬數字先攫住視線——十七世紀的日輪鐘鑲在白牆紅瓦之間，藍白放射紋像被時間反覆擦亮過。導遊說這是老城裡「會講故事的鐘」，我半信半疑，直到晨光斜斜切過鐘面，金屬的光澤忽然活了起來。按下快門的那一刻突然明白：在塔林，連時間都捨得慢下來讓人看清楚。

### 愛沙尼亞互動札記（同步）

| 要點 | 做法 |
|------|------|
| **呈現** | `estonia-journal.html`（點卡片展開）；主站 day07 EE–day10 同步同文案 |
| **重建** | `python3 scripts/build_estonia_journal.py` |
| **文風** | 同上 v1.2；`fact` 列最多一句知識 |
## 札記配圖原則 — 一圖不拆兩卡（2026-07-19 紀錄 · HARD）

> 詳見 `.ai-kos/CONTENT_STYLE.md` § 寫作原則第 6 條。此處為開工速記。

| 該做 | 不該做 |
|------|--------|
| 同一張照片若有兩層意思 → **併同一卡、精簡敘事** | 同景近重複圖拆成兩卡、各寫一段標題／描述 |
| 不確定是否同景／重複 → **寧可不上** | 為了不漏描述而硬加第二張幾乎一樣的圖 |

**當日記錄：** Day 3「憲法牆」保留一卡，將「我是貓王／NOBODY KNOWS I'M ELVIS!」併入同一段；已移除多餘第二卡。

## 每日版型（2026-08-28 · Owner · HARD）

每天的頁面結構固定為兩層，**不得顛倒、不得合併**：

```
┌─────────────────────────────────────────┐
│             LANDMARK（景點照）           │
│   ## 古蹟  ← 2–3 張乾淨景點圖，無遊客    │
├─────────────────────────────────────────┤
│              旅人區（旅遊照）            │
│   ## 旅人區 ← 斌哥實拍 + 影片卡         │
└─────────────────────────────────────────┘
```

| 層 | markdown 區塊 | 內容規則 |
|----|--------------|---------|
| **上層 LANDMARK** | `## 古蹟` | 純景點照，**無人入鏡**；出發前由斌哥預建，**禁止替換或刪除** |
| **下層 旅人區** | `## 旅人區`（或 `## 表演`、`## 住宿` 等） | 斌哥實拍（含人）、影片卡、住宿照 |

**執行要點：**

- Landmark 照片是行前由斌哥選定，存放於 `photos/baikal-rail/dayXX/`（無 `-downloaded` 後綴的純景圖）
- 影片卡即使是景點影片，也因有人物出現，放入**旅人區**，不放 LANDMARK 排
- 每天的 LANDMARK 通常 2–3 張，剛好填滿一排（3欄網格的一行）

## 版型試驗 — 斜對角動線（2026-07-19 · Day 2 首試）

> 旅行書要走十年、二十年，若長期只剩「左右並排、照片等大」會變乏味。  
> **寧可大膽試驗版型**，也勝過永遠同一格局。細節見 `city-magazine-template.md`。

| 試驗點 | 作法 |
|--------|------|
| 觸發 | BLDH Day 2（恰兩張：克格勃博物館 → AKROPOLIS） |
| 結構 | 左上主視覺（歷史）＋右下次視覺（現代）＋中間淡斜切線（時間／動線） |
| 原則 | 照片錯落、文字錨定；**先敢試，再談習慣與下一輪更大膽** |

主站 class：`sites-grid--diagonal`（由 `scripts/build.py` 輸出）

## 計畫書（非今日工 · 暫不部署配合）

| 計畫 | 路徑 | 何時執行 |
|------|------|----------|
| **景點點擊播放音樂** | `content/bldh-trio/source/MUSIC_CLICK_PLAN.md` | 行程走到對應城市＋備妥合法 15–30s 音檔後；**現階段不改部署** |

## Phase

**Operational Phase** — AI-KOS 服務旅行書；旅行書不再服務 AI-KOS。  
預設工作：Daily Travel Update（照片 → 札記 → build → deploy → 固定營運摘要）。

## Wake commands

| 指令 | 行為 |
|------|------|
| **開工** | 先讀本檔 **Photos SSOT**，再讀 `.ai-kos/RESUME_CONTEXT.md`；預設 Daily Travel Update |
| **收工** | 寫輕量斷點至父層 `旅遊/CLAUDE.md` 後道別 |
| **Ingest** | **跨文件相關內容同步**：找出本次修改牽涉的相關文件並一併改一致 |

### Ingest（知識維護，非功能開發）

> **Ingest** = 修改跨文件中的相關內容。

- 對齊舊名稱、舊 URL、舊 Phase／Mode、舊模板
- 歷史 archive 可保留；**可執行指令**必須改為現行正確值
- 不做無關功能、不做 bulk rewrite
- 詳見 `.ai-kos/DECISIONS.md` · `.ai-kos/RESUME_CONTEXT.md`
