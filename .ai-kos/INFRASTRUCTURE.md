# INFRASTRUCTURE — travel-site

專案基礎設施與永久資源。此文件為 **Knowledge Only** — 不涉及 build、deploy 或 session 狀態。

---

## Workspace Paths（Canonical — HARD RULE）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
WORKSPACE PARENT:       /Users/mac/Documents/Projects/旅遊/
FORBIDDEN:              /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects:           /Users/mac/Documents/Projects/旅遊/<project-name>/
```

| 項目 | 路徑 |
|------|------|
| **Git 有效 repo** | `/Users/mac/Documents/Projects/旅遊/travel-site/` |
| **旅遊工作區父目錄** | `/Users/mac/Documents/Projects/旅遊/` |
| **GitHub remote** | `https://github.com/slimgril/travel-site` |
| **Desktop residue（禁止開啟）** | `~/Desktop/旅遊/` — 僅導向文件；不得有 `travel-site/` 子目錄 |
| **Workspace SSOT** | `.ai-kos/WORKSPACE.md` |

Agent 行為：所有 `cd`、`git`、`commit`、`push`、`deploy`、檔案讀寫**僅限** Documents 路徑。不得 fallback 至 Desktop。

---

## Google Drive Shared Folder（Permanent）

| 項目 | 值 |
|------|-----|
| **URL** | https://drive.google.com/drive/folders/1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD |
| **Folder ID** | `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD` |

### Purpose

斌哥所有旅行照片唯一來源（Single Source of Truth）。

### Policy

- Shared Folder **固定不變** — 不因新旅程而更換根資料夾
- 每次 **Resume** 不需再詢問 Shared Folder
- 每次 **Daily Update** 直接由此 Folder 增量同步
- 各次旅行以**子資料夾**區分，不更換 Shared Folder
- **Photo Sync** 一律由此入口開始
- Resume 時若進行旅行更新，直接使用此 Shared Folder，**不再要求使用者提供路徑**

---

## Local Photo Paths — Baikal Rail（Cyprian Railroad 20 日）

**Canonical project root（2026-07-16）**：`/Users/mac/Documents/Projects/旅遊/travel-site/`。桌面暫存夾已移入專案（2026-07-15）；Resume 一律從下列路徑找圖。

| 路徑 | 用途 |
|------|------|
| `~/Documents/Projects/旅遊/travel-site/photos/baikal-rail/day01/` … `day20/` | **網站正式用圖**（build 引用、`*-downloaded.jpg` 命名） |
| `~/Documents/Projects/旅遊/travel-site/content/baikal-rail/source/Siberian_Railway_Landmarks/` | **下載暫存區**（依 `Day NN - 景點名` 分類；新圖先放這裡） |
| `~/Documents/Projects/旅遊/travel-site/content/baikal-rail/source/drive-originals/` | Drive 同步原始檔（依 Drive 路徑鏡像） |
| `~/Documents/Projects/旅遊/travel-site/content/baikal-rail/source/photo-sync.json` | 已匯入 manifest（hash、來源、待審） |

### 工作流程

1. 新下載照片 → `source/Siberian_Railway_Landmarks/Day NN - 景點名/`
2. 確認後搬入 → `photos/baikal-rail/dayNN/`（必要時重新命名為 `{slug}-downloaded.jpg`）
3. 桌面**不再**放置 `Siberian_Railway_Landmarks` 資料夾

---

## Related Paths（Read-Only Reference）

以下為既有實作與慣例文件，**本文件不修改它們**；僅作交叉引用。

| 路徑 | 說明 |
|------|------|
| `content/baikal-rail/source/photo-sync-config.json` | 已含相同 `folder_id`（`1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`） |
| `content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md` | 子資料夾命名慣例（`Day NN - 景點中文名` 等） |
| `content/baikal-rail/source/PHOTO_SYNC.md` | 同步操作流程（目前以 baikal-rail script 為例；**政策適用全站**） |

### 結構示意

```text
Google Drive Shared Folder（永久根，folder_id 固定）
├── <旅程 A 子資料夾>/          ← 例：Siberian Railway / baikal-rail
│   ├── Day 01 - …/
│   └── Day 02 - …/
├── <旅程 B 子資料夾>/
│   └── …
└── …
```

---

## Agent 行為摘要

| 情境 | 行為 |
|------|------|
| Resume / 開工 | 直接使用上方 Shared Folder，不詢問路徑 |
| Daily Update / 照片同步 | 遵循 `.ai-kos/DAILY_TRAVEL_UPDATE.md`（每日 08:00 主動執行） |
| 新旅程 | 在 Shared Folder 內新增子資料夾，**不**建立新 Shared Folder |

**決策背景**：`.ai-kos/DECISIONS.md` — Google Drive Shared Folder 永久 SSOT · Daily Travel Photo Sync（2026-07-16）

**Canonical 營運規則**：`.ai-kos/DAILY_TRAVEL_UPDATE.md`
