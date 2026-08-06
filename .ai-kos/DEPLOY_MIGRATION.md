# Deploy Migration — travel-site

**狀態：** **Cutover 完成**（2026-07-30）— Production = Cloudflare Pages  
**Production：** https://travel-site-quarter.pages.dev/  
**Fallback：** Surge `cluttered-breath.surge.sh`（過渡期可留）

---

## 為什麼遷移

| 痛點 | 結果 |
|------|------|
| Surge 上傳 `ECONNRESET`／體積壓力 | 改 Pages Direct Upload |
| Render 付費評估 | **不採**為主路徑 |

---

## 不變硬規則

- Canonical root：`/Users/mac/Documents/Projects/旅遊/travel-site`（禁 Desktop）
- **禁止** deploy 未壓縮 `dist` 或 `photos/` 原圖
- Bundle：`dist-surge-upload`（目錄名歷史遺留）
- sips／`package_preview_deploy` **須在 sandbox 外**
- 下季：新 Pages project＋該季獨立壓縮包

---

## 產物對照

| 產物 | 用途 |
|------|------|
| `dist-surge-upload/` | **正式上傳包** |
| `deploy/cloudflare/wrangler.toml` | Pages 設定 |
| `scripts/deploy_cloudflare_pages.sh` | **預設 Deploy** |
| Surge CLI | Fallback only |

---

## Phase 紀錄

| Phase | 狀態 |
|-------|------|
| 0 就緒 | Done |
| 1 試跑 | Done（2026-07-30 · 473 files） |
| 2 Cutover | **Done**（Owner：「換 Production」） |
| 3 媒體 CDN | 未採（後備） |

---

## 日常 Deploy（Production）

```bash
# 須已 wrangler login；sips／打包在 sandbox 外
bash scripts/deploy_cloudflare_pages.sh
# 等價：
# wrangler pages deploy dist-surge-upload \
#   --project-name=travel-site-quarter --branch=main --commit-dirty=true
```

npm：`npm run deploy:pages`

驗收：

- https://travel-site-quarter.pages.dev/ → 200
- `/trips/bldh-trio.html`、`/trips/baikal-rail.html` → 200

---

## Rollback（Surge）

```bash
npx surge@0.23.1 dist-surge-upload cluttered-breath.surge.sh
# 或 npm run deploy:surge:fallback
```

Rollback 後須同步改回 Knowledge Production URL（DECISIONS／INFRASTRUCTURE／DAILY／RESUME）。

---

## Video Deployment Policy（2026-08-05 實證）

**限制：** Cloudflare Pages 單檔上限 25 MiB。

**政策：**

| 項目 | 做法 |
|------|------|
| **原始影片** | 永久保留在 `photos/<trip>/dayNN/` 原始檔案；**不覆蓋** |
| **檢查** | 部署前檢查 `dist-surge-upload/photos/` 中所有 `.mp4` / `.MP4` 檔案大小 |
| **壓縮** | 若超過 25 MiB，產生 Web 版（目標 18–22 MiB，保持品質） |
| **Web 版** | 覆蓋 `dist-surge-upload/` 中的對應檔案，原始檔案保持不動 |

**參考實證：**

- **BLDH**（波羅的海）：原始影片已在 10 MiB 以下，直接部署
- **Baikal Day 03**（2026-08-05）：74 MiB 原始 → 19 MiB Web 版（44s/1080p/3.6Mbps）

**壓縮指令範例：**

```bash
# 檢查影片時長和解析度
ffprobe -v error -show_entries format=duration -show_entries stream=width,height \
  -of default=noprint_wrappers=1 video.mp4

# 壓縮至約 20 MiB（根據時長調整 bitrate）
ffmpeg -i original.mp4 \
  -c:v libx264 -b:v 3600k -maxrate 3800k -bufsize 7200k \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output.mp4 -y
```

**Why 18–22 MiB：**

- Cloudflare 限制 < 25 MiB
- 留 3–7 MiB 餘裕（metadata／封裝開銷）
- 優先保持品質，不追求極致壓縮

---

## Phase 3 — 媒體 CDN（僅體積仍失控）

R2／Bunny／S3 外置大圖與 mp4；另開 ADR 後再改 build。
