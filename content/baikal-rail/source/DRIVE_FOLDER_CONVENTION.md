# Google Drive 資料夾命名慣例（Baikal Rail）

本文件定義 **Google Drive 共用資料夾** 的推薦結構，供使用者上傳、AI 同步、以及跨 session 交接時一致遵循。

**決策背景**：見 `.ai-kos/DECISIONS.md` — 路徑無法解析時不猜 Day，改進 `review_required`。

---

## 推薦結構

```text
<Siberian Railway 或旅程名稱>/          ← 根資料夾（photo-sync-config 指向此層）
├── Day 01 - 北京首都機場/
│   └── IMG_xxxx.JPG
├── Day 02 - 烏蘭巴托市景/
│   ├── IMG_2423.JPG
│   └── IMG_2424.JPG
├── Day 04 - 蒙古國民族舞蹈與馬頭琴表演/
│   └── ...
└── Day 20 - ...
```

### 資料夾命名格式

```
Day NN - 景點中文名
```

| 規則 | 範例 | 說明 |
|------|------|------|
| 天數 | `Day 02` 或 `Day 2` | 腳本接受 1–2 位數；建議兩位數 `Day 02` |
| 分隔 | ` - `（空格-空格） | 與本機 `Siberian_Railway_Landmarks` 一致 |
| 景點名 | 與 `dayXX.md` 標題一致或高度相似 | 腳本以關鍵字比對 landmark |

景點名應對應 `content/baikal-rail/dayXX.md` 中 `### 景點名` 標題，例如：

- `Day 02 - 烏蘭巴托市景`
- `Day 07 - 貝加爾湖生態博物館`
- `Day 11 - 新西伯利亞國立歌劇院`

檔名可為相機預設（`IMG_2432.JPG`）；同步後會重新命名為 `{english-slug}-downloaded.jpg`。

---

## 避免使用的結構

### ❌ 日期資料夾

```text
0711/
0712/
20260711/
```

**原因**：

- 腳本無法從 `0712/IMG_20260712_161953.jpg` 推斷對應 Day 4 還是 Day 11
- 同一日期可能跨越多個行程天或不同 trip（如 Baltic vs Baikal）
- 目前 15 張照片因此進入 `review_required`

### ❌ 僅檔名、無 Day 資料夾

```text
<根目錄>/
├── IMG_2432.JPG
└── IMG_2433.JPG
```

**原因**：缺少 Day 與 landmark 語意，無法自動配對 `dayXX.md`。

### ❌ 與行程無關的通用資料夾

```text
待整理/
新照片/
Baltic/
```

**原因**：不同 trip 的照片混在同一 Drive 根目錄時，腳本僅處理 Baikal 路徑；非 `Day XX -` 結構一律待審。

---

## 為什麼這很重要

| 面向 | 說明 |
|------|------|
| **AI 判斷** | 同步腳本以路徑 regex `Day\s+(\d{1,2})\s*-\s*(.+)` 解析；無此結構 → review_required |
| **增量同步** | 正確資料夾 → 自動寫入 manifest、更新 gray card；錯誤結構 → 每次 sync 跳過但不匯入 |
| **交接** | 新 agent / 新 session 讀 `photo-sync.json` 與本文件即可延續，無需猜測 |
| **維護** | 與本機 `content/baikal-rail/source/`、`photos/baikal-rail/dayXX/` 心智模型一致 |

---

## 多 trip 共用 Drive 時

若同一 Drive 根目錄存放多趟旅程：

1. **Baikal** 照片必須在 `Day XX - 景點名` 下（XX = 1–20）
2. **其他 trip** 照片應放在獨立子資料夾（如 `Baltic Day 01 - ...`），且**不要**與 Baikal sync 根目錄混用 — 或為其他 trip 建立獨立 sync 設定

目前 sync 根目錄 `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD` 內的 `0711/`、`0712/` 為 Baltic 上傳，非 Baikal Day 結構，故全部待審。

---

## 修正待審照片

1. 在 Drive 建立正確的 `Day XX - 景點名` 資料夾
2. 將照片移入
3. 自 `photo-sync.json` → `review_required` 刪除對應項目（解除 drive_file_id 封鎖）
4. 重新執行 `python3 scripts/sync_baikal_photos.py`

---

## 參考

- 操作手冊：[PHOTO_SYNC.md](./PHOTO_SYNC.md)
- 設定：[photo-sync-config.json](./photo-sync-config.json)
- Landmark 清單：`content/baikal-rail/day01.md` … `day20.md`
