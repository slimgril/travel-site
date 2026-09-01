# travel-site 核心運作鐵律（大嬸與斌哥的最高指導原則）

## 1. 專案主神定位
* 正式營運專案路徑為 ~/Projects/travel-site，正式部署於 Cloudflare Pages。
* 隔壁棚的 lvhun/Render 是平行測試實驗室，嚴禁混淆。

## 2. 三大章節與檔案完美歸位
* **西伯利亞線**：日記放在 content/baikal-rail/，照片放在 photos/baikal-rail/。
* **波羅的海線**：日記放在 content/bldh-trio/，照片放在 photos/bldh-trio/。
* **山西線**：日記放在 content/shanxi/，照片放在 photos/shanxi/。

## 3. 拒絕盲目排查，寧可重寫生成
* 嚴禁在未確認照片是否存在的狀況下盲目跑排查。AI 每次更新必須執行 python3 scripts/build.py 確認【缺圖 0 張】才准推送。
* 若遇到路徑渲染錯誤，應直接參考 scripts/build.py 重新渲染對應的 HTML 檔案，不准修補有毒的舊路徑。
