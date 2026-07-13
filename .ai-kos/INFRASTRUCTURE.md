# INFRASTRUCTURE — travel-site

專案基礎設施與永久資源。此文件為 **Knowledge Only** — 不涉及 build、deploy 或 session 狀態。

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
| Daily Update / 照片同步 | 從 Shared Folder 增量同步；依旅程子資料夾區分 |
| 新旅程 | 在 Shared Folder 內新增子資料夾，**不**建立新 Shared Folder |

**決策背景**：`.ai-kos/DECISIONS.md` — Google Drive Shared Folder 永久 SSOT
