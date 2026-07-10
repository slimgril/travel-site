# CONVENTIONS — 旅程資料規範（訂死，每趟照這一套）

本文件是 `travel-site` 每一趟旅程的**唯一資料規範**。新旅程一律照此建立，不再逐案發明結構。
規範以 `scripts/build.py` 的實際行為為準（Rule 1：Code Follows Knowledge 的反向約束——這裡的規則就是 build 能吃的格式）。

---

## 1. 每趟旅程的目錄結構

以 slug = `bldh-trio` 為例（實際 slug 換成該趟旅程的英文短名）：

```
content/
└── <slug>/
    ├── trip.md              # 旅程 front-matter（唯一必要檔，沒有它 build 會忽略整個資料夾）
    ├── day01.md
    ├── day02.md
    ├── ...
    ├── dayNN.md
    └── source/              # 原始行程（PDF / Excel / 貼上的文字）；build 一律忽略
        └── itinerary.pdf

photos/
└── <slug>/
    ├── day01/               # 該天最終選用、會出現在網站上的照片
    ├── day02/
    ├── ...
    ├── dayNN/
    └── originals/           # 手機原圖倉庫；永久保留，不進網站（見 §4）
```

單日單檔、分天資料夾。**不要**把所有照片直接丟進 `photos/<slug>/`。

---

## 2. 命名規則（build.py 硬性要求）

- **slug**：小寫英文 + 連字號，例：`shanxi`、`baltic`、`bldh-trio`。
  - `content/<slug>/` 資料夾名、`photos/<slug>/` 資料夾名、`trip.md` 內 `slug:` 三者必須一致。
  - 產出頁面為 `dist/trips/<slug>.html`。
- **每天檔名**：`dayNN.md`，兩位數補零（`day01.md`…`day15.md`）。
  - build 只認得 regex `^day\d+\.md$`，其它檔名（`itinerary.md`、`overview.md`、`notes.md`…）會被**忽略**，可安全用來放草稿。
  - 排序依檔名，所以務必補零，否則 `day10` 會排在 `day2` 前。
- **trip.md**：只放 front-matter，不放正文。欄位參考現有 `content/shanxi/trip.md`（slug / number / title / subtitle / traveler / status / date_start / date_end / hero_badge / hero_quote / summary / tags / stats）。
  - `status` 值：`upcoming`（即將出發）/ `done`（已完成）/ 其它（規劃中）。
  - **注意**：`## 現場直擊`（live）區塊只有在 `status: done` 時才會被渲染。

---

## 3. 照片引用規則 ★最關鍵，違反會 404

build.py 產生的路徑是：`../photos/<slug>/` + markdown 括號內的原字串。

因此在 `dayNN.md` 內引用照片時，**括號內必須帶上 `dayNN/` 前綴**：

```markdown
### ![青龍峽疊瀑](day03/114_疊瀑近景.jpg) 青龍峽
```

→ 解析為 `photos/bldh-trio/day03/114_疊瀑近景.jpg` ✅

**錯誤寫法**（山西舊格式，扁平引用）：

```markdown
### ![青龍峽疊瀑](114_疊瀑近景.jpg) 青龍峽    # ✗ 會找成 photos/bldh-trio/114_...jpg → 缺圖
```

- 照片檔名建議：`序號_短描述.jpg`（例 `114_青龍峽疊瀑.jpg`），序號在該天內遞增即可。
- build 完成後會印出「缺圖 N 張」，N 必須為 0 才算通過。

---

## 4. 原始照片 `originals/`

- 手機原圖（可能數百張）全部先進 `photos/<slug>/originals/`，**永久保留、永不刪**。
- AI 挑選後，把選用的照片**複製**（不是移動）到對應的 `photos/<slug>/dayNN/` 並重新命名。
- `originals/` 已在 build 的複製流程中被排除，**不會**進入 `dist/` 或部署包（見 `scripts/build.py` 的 `copy_tree(..., skip={'originals'})`）。
- 因此原圖不影響部署大小，可放心堆放。

---

## 5. 標準工作流程（五階段，先整理資料再做內容）

沿用 AI-KOS「先整理資料，再開始內容製作」，避免山西初期的資料混亂。

| 階段 | 動作 | 產出 | 禁止 |
|------|------|------|------|
| **Phase 1** | 建立資料夾：`content/<slug>/`(+`source/`)、`photos/<slug>/`、`photos/<slug>/originals/` | 空骨架 | 不寫任何內容 |
| **Phase 2** | 匯入原始行程到 `content/<slug>/source/` | 原始行程檔就位 | 不產生任何網站內容 |
| **Phase 3** | 依行程逐日拆成 `day01.md`…`dayNN.md`，並建立對應 `photos/<slug>/dayNN/` | 每天一檔 | 不要求一次拆完全部 |
| **Phase 4** | 照片整理：原圖進 `originals/`，選用圖複製到 `dayNN/` | 照片歸位 | — |
| **Phase 5** | 正式撰寫旅遊書內容 | 完成頁面 | — |

新旅程從 Phase 1 開始，不跳步。

---

## 6. Build / 驗證指令

```bash
python3 scripts/build.py     # 唯一生產環境產生器；零依賴，只用 Python 3 標準庫
```

> 註：`package.json` 目前寫的是 `node scripts/build.js`，但實際產生器是 `scripts/build.py`（`build.js` 不存在）。以 `build.py` 為準。此不一致已記錄，待後續統一。

驗證通過標準：
- build 無錯誤。
- 輸出「缺圖 **0** 張」。
- `content/*.md` 為永久原稿，build 永不改動；`dist/` 每次重建。

---

## 7. Landmark 候選圖片 Pipeline 與 Prototype Build

`reference/` 內的 hero image 是**生產環境唯一可信來源**，被 `landmarks.yaml` 的 `hero_image:` 欄位直接引用、由 `scripts/build.py` 發布進 `dist/`。要替換其中任何一張圖，**不得直接覆寫 `reference/`**——必須先經過候選管線與 Prototype Build 審核。

### 7.1 目錄結構（每個 slug 內新增）

```
photos/<slug>/
├── source/            # 候選替換圖片原始輸入；build.py 永遠忽略，不會進 dist/
├── cooked/
│   ├── matched/       # 判定與某張 reference 圖對應的候選圖（檔名＝要取代的 reference 檔名）
│   ├── review/         # 不確定的候選圖，需人工複核
│   └── review.csv      # 提案替換表：reference_file, candidate_file, status, confidence, notes
└── reference/          # 生產環境目前核准使用的圖；工具鏈永不寫入此資料夾，只能由人工晉升
```

- `source/`、`cooked/` 兩者皆不進生產 `dist/`（見 `copy_tree(..., skip=...)`），如同 `originals/`。
- `cooked/matched/<file>.jpg` 的檔名必須與它要取代的 `reference/<file>.jpg` 相同，Prototype Build 用檔名比對做覆蓋。

### 7.2 Prototype Build（獨立於生產環境）

```bash
python3 scripts/build_prototype.py   # 產出 dist-prototype/，不影響 dist/、不影響 reference/
```

- 內部重用 `scripts/build.py` 的 `main()`（新增 `dist_dir` / `overlay` 參數，預設值與原行為完全相同，`python3 scripts/build.py` 產出位元對位元不變）。
- 唯一差異：複製完 `photos/` 到 `dist-prototype/photos/` 之後，會把每個 slug 的 `cooked/matched/*.jpg` **覆蓋到 `dist-prototype/photos/<slug>/reference/`**——只動 `dist-prototype/` 這份輸出的複本，磁碟上真正的 `photos/<slug>/reference/` 完全不受影響。
- `dist-prototype/` 與 `dist/` 是兩棵獨立的樹；重新執行生產 `build.py` 不會讀到、也不會清除 `dist-prototype/`。

### 7.3 晉升流程（Promotion）

1. 候選圖片放入 `photos/<slug>/source/`。
2. （人工或 AI 輔助比對後）分類進 `cooked/matched/` 或 `cooked/review/`，並寫入 `cooked/review.csv`。
3. 執行 `scripts/build_prototype.py`，產出 `dist-prototype/`，供人工在瀏覽器實際比對後再決定。
4. **人工核准後**，才把 `cooked/matched/` 中核准的檔案複製（覆蓋同名檔）進 `photos/<slug>/reference/`，然後重跑正式 `scripts/build.py`。
5. 在核准前，`reference/`、`dist/`、生產部署三者都不得被此流程觸碰。

---

**Updated**: 2026-07-05
**Authority**: 本檔為旅程資料結構的 Single Source of Truth；與個別旅程作法衝突時以本檔為準。
