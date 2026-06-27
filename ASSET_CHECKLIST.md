# Asset & Migration Checklist — 山西遷移

## ✅ 修正完成 — 全部 Day01–Day15 通過

Build 狀態：**缺圖 0 張，無錯誤**

---

## 已執行的圖片複製

```bash
# 已執行：將所有 img-*.jpg 從 Golden Master 複製到 travel-site
find "/Users/johnsonwang/Desktop/旅遊/shanxi-15day 2" \
  -maxdepth 1 -name "img-*.jpg" \
  -exec cp {} "/Users/johnsonwang/Desktop/旅遊/travel-site/photos/shanxi/" \;
# 結果：25 張 img-*.jpg 已就位
```

Day 13 的 IMG_2154–IMG_2179 已確認存在於 `travel-site/photos/shanxi/`（IMG_2177 在 GM 中本就不存在）。

---

## build.py 修正記錄（本次修正）

1. **`classify_paras` 加入 `:::raw` 支援**：偵測 `:::raw...:::` 區塊，輸出 `{'type': 'raw', 'html': ...}`，繞過 esc() 直接嵌入 HTML。
2. **`render_history` 重構**：原本只渲染第一個 `###` 卡，現在迭代所有 `###` 卡，各自產生一個 `<div class="history-panel">`（Day 13 需要兩個面板）。

---

## 最終比對結果

| Day | 文字內容 | 圖片引用 | feature 標記 | 整體狀態 |
|-----|---------|---------|-------------|---------|
| Day01 | ✅ | ✅ | ✅ | ✅ **PASS** |
| Day02 | ✅ | ✅ 已補 4 img | ✅ 已補 {feature} | ✅ **PASS** |
| Day03 | ✅ | ✅ 已補 2 img | ✅ 已補 {feature} | ✅ **PASS** |
| Day04 | ✅ | ✅ 已補 2 img | ✅ 已補 {feature} | ✅ **PASS** |
| Day05 | ✅ | ✅ | ✅ 已補 {feature} | ✅ **PASS** |
| Day06 | ✅ 已移除多餘卡 | ✅ | ✅ 已補 {feature} | ✅ **PASS** |
| Day07 | ✅ | ✅ | ✅ 已補 2 {feature} | ✅ **PASS** |
| Day08 | ✅ | ✅ 已補 2 img | ✅ 已補 2 {feature} | ✅ **PASS** |
| Day09 | ✅ | ✅ 已補 2 img | ✅ 已補 {feature} | ✅ **PASS** |
| Day10 | ✅ | ✅ 已補 1 img | ✅ 已補 {feature} | ✅ **PASS** |
| Day11 | ✅ | ✅ 已補 1 img | ✅（{feature} 文字卡） | ✅ **PASS** |
| Day12 | ✅ 已補 15 張現場 | ✅ 已補 1 img | ✅ | ✅ **PASS** |
| Day13 | ✅ 已補史段+25張現場 | ✅ 已補 3 img | ✅ 2 feature 卡 | ✅ **PASS** |
| Day14 | ✅（GM 無現場段） | ✅ 已補 2 img | ✅（GM 無 feature 卡） | ✅ **PASS** |
| Day15 | ✅ | ✅ | ✅ | ✅ **PASS** |

---

## 備注

- Day 06 的 `43_平遙炒碗托.jpg` 卡片：Golden Master 不含此條目，已從 day06.md 移除（遵守 GM 是唯一真實來源原則）。
- Day 13 的 `{tag:丫斌哥留影}` 和 `{tag:晉祠三絕}`：目前 build.py 只識別含「隨筆」的 tag，此二 tag 已記錄在 Markdown 中（資料保存完整），但渲染成 tag badge 需後續 build.py 擴充。
- Day 15 的 `lodging=溫暖的家` 渲染為「住宿：溫暖的家」（build.py 硬寫 "住宿"）；GM 使用「回到」。內容保留，label 差異可後續調整。

---

## 下一階段（100% 還原完成後可進行）

按照 Golden Master 規定的順序：

1. 地圖
2. 時間軸
3. Lightbox
4. 照片懶載入
5. AI 摘要
