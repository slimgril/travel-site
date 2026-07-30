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

## Phase 3 — 媒體 CDN（僅體積仍失控）

R2／Bunny／S3 外置大圖與 mp4；另開 ADR 後再改 build。
