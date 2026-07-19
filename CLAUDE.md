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

| 項目 | 值 |
|------|-----|
| **名稱** | 20260711波羅的海（根目錄；內含 `0711/`、`0712/`、`0713/`… 子資料夾） |
| **URL** | https://drive.google.com/drive/folders/1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD |
| **Folder ID** | `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD` |

**政策：**

- Shared Folder **永久固定** — 新旅程只在此根目錄下加子資料夾，不換根 Folder ID
- 每次 Resume／Daily Update **直接使用上方 URL／ID**，不要求使用者重貼連結
- 完整路徑／Baikal 本機鏡像等細節見 `.ai-kos/INFRASTRUCTURE.md`（Folder ID 與此處一致，以此為入口提醒）

## 札記配圖原則 — 一圖不拆兩卡（2026-07-19 紀錄 · HARD）

> 詳見 `.ai-kos/CONTENT_STYLE.md` § 寫作原則第 6 條。此處為開工速記。

| 該做 | 不該做 |
|------|--------|
| 同一張照片若有兩層意思 → **併同一卡、精簡敘事** | 同景近重複圖拆成兩卡、各寫一段標題／描述 |
| 不確定是否同景／重複 → **寧可不上** | 為了不漏描述而硬加第二張幾乎一樣的圖 |

**當日記錄：** Day 3「憲法牆」保留一卡，將「我是貓王／NOBODY KNOWS I'M ELVIS!」併入同一段；已移除多餘第二卡。

## 版型試驗 — 斜對角動線（2026-07-19 · Day 2 首試）

> 旅行書要走十年、二十年，若長期只剩「左右並排、照片等大」會變乏味。  
> **寧可大膽試驗版型**，也勝過永遠同一格局。細節見 `city-magazine-template.md`。

| 試驗點 | 作法 |
|--------|------|
| 觸發 | BLDH Day 2（恰兩張：克格勃博物館 → AKROPOLIS） |
| 結構 | 左上主視覺（歷史）＋右下次視覺（現代）＋中間淡斜切線（時間／動線） |
| 原則 | 照片錯落、文字錨定；**先敢試，再談習慣與下一輪更大膽** |

主站 class：`sites-grid--diagonal`（由 `scripts/build.py` 輸出）

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
