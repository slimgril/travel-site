# DECISIONS — travel-site

架構與流程決策紀錄。新增決策時在最上方追加條目。

---

## 2026-08-08 — Landmark Layer Rule（Owner 定稿 · HARD）

**性質**：Owner 明確指示 · 內容架構規則。  
**背景**：baikal-rail Day 2 rebuild 時，4 張 Landmark 參考圖被斌哥照片取代而消失；斌哥指出此為錯誤，提出正確分層概念。

**決策：**

| # | 規則 | 含義 |
|---|------|------|
| **1** | **Landmark 參考圖為永久資產** | `*-downloaded.*` 等骨架期參考圖代表「景點本身」，不因旅程進行而消失 |
| **2** | **Landmark 圖不得被旅行照片取代** | 斌哥照片＝「現場體驗」；Landmark 圖＝「景點身份」；兩者性質不同，各自獨立存在 |
| **3** | **斌哥照片僅能附加於 Landmark 之下** | 新照片在對應 Landmark 卡後方另開新卡，用不同卡名（體驗視角）區分 |
| **4** | **Daily Travel Update 不得刪除既有 Landmark** | 日常同步只能新增，不能移除 `day##.md` 中的 Landmark 卡 |
| **5** | **新照片一律採增量加入模式** | 禁止以「合併」為由刪減既有卡數；不論是否已有同地點描述，新照片都另開新卡附加 |

**修復**：`content/baikal-rail/day02.md` 已還原 4 張 Landmark 參考圖（`ulaanbaatar-city-downloaded.jpg`、`turtle-rock-downloaded.jpg`、`genghis-khan-statue-downloaded.jpg`、`mongolia-horseback-riding-downloaded.png`），斌哥 11 張照片改為附加於下方。`day03.md` Landmark 卡同步還原。

**參考**：`.ai-kos/CONTENT_STYLE.md` § Landmark Layer Rule · `.ai-kos/DAILY_TRAVEL_UPDATE.md` Step 3

---

## 2026-07-30 — Production Cutover → Cloudflare Pages（Owner 核准）

**性質**：Owner 明確指示「換 Production」· Cutover。

**問題：** Surge 上傳長連線反覆 `ECONNRESET`；Pages 試跑已 PASS。

**決策：**
- **本季 Production** = Cloudflare Pages `travel-site-quarter`  
  → https://travel-site-quarter.pages.dev/
- 預設 Deploy：`scripts/deploy_cloudflare_pages.sh`（預設 project＝`travel-site-quarter`，`--branch=main`）
- 上傳包不變：`dist-surge-upload`（壓縮靜態包；禁止未壓縮 `dist`／`photos/` 原圖）
- **Surge fallback**：`cluttered-breath.surge.sh` 可保留過渡；日常不再當預設；Rollback 指令見 `DEPLOY_MIGRATION.md`
- **下季新旅程**：新 **Pages project**＋該季獨立壓縮包（延續每季分站精神；不再預設新 Surge 網域）
- 自訂網域（CNAME）本階段不強制

**參考**：`.ai-kos/DEPLOY_MIGRATION.md` Phase 2 · `.ai-kos/INFRASTRUCTURE.md`

---

## 2026-07-30 — 影片畫面／配樂淡入淡出加長（先行＋延遲收）

**性質**：Owner／斌哥聽覺體驗（覆寫 2026-07-26 的 800ms 音量淡變）。

**決策：**
- **配樂先行**：點擊後先播原片音軌並淡入，**約 2.5s** 後才淡入影片畫面（仍蓋海報圖）
- **畫面入場**：由 **0.5×** 慢慢放大至滿版，約 **3.5s**（足夠看清）
- **畫面先收／慢慢消失**：片尾約 **5.2s** 前開始淡出（CSS transition 約 **4.5s**）
- **音量淡出加長至約 4.5s**（ease-out），並在影片結束前收到接近靜音，避免驟停；保底約 **2.8s**
- 立陶宛黑膠 15s：片尾／手動停止亦淡出約 **2.8s**
- 短片（<12s，如栗子攤）自動縮短先行／延遲，避免吃掉全片
- `prefers-reduced-motion: reduce`：取消先行／縮放／長淡變，瞬切
- 仍為原片音軌，**不是**獨立景點配樂（`MUSIC_CLICK_PLAN`）

**參考**：`templates/shell.html`（`VISUAL_LEAD_MS`／`VISUAL_TRAIL_MS`／`AUDIO_FADE_MS`）· `templates/base.css`（`.is-picture-on`／`.is-picture-out`）

---

## 2026-07-30 — 斌哥自維護照片播放器（主題＝資料夾）

**性質**：Owner 要求 · UI 設計定稿。

**決策：**
- 路徑：`player/bingge/`（本機伺服器 `server.py`／`開始播放.bat`／`開始播放.command`）
- **主題名稱＝Library 資料夾名**；匯入 UI（`maintain.html`）建立主題並上傳照片
- 播放器首頁列出全部主題供選擇播放
- 斌哥自行維護；Agent／旅行書札記不自動改 Library
- 雲端靜態站無法收上傳 → 維護在本機；站上僅掛 `how-to.html` 說明
- 本機開發可預置主題「山西漫遊」；**PC 發行包不含照片**（`player/releases/斌哥照片播放器-PC.zip`）

**參考**：`player/bingge/README.md`

---

## 2026-07-30 — 山西雲端照片播放器（全部照片）

**性質**：Owner 要求 · 新能力（雲端；掛在山西旅程）。

**決策：**
- 路徑：`player/shanxi/`（靜態；`scripts/build_shanxi_player.py`）
- 內容＝**全部照片**：札記入站＋磁碟未入冊＋`photos/shanxi/player-extras/`（斌哥補傳未入選）
- **不**把未入選圖塞進札記卡；播放器獨立於旅行書敘事
- 混合打包：入站／未入冊圖走 `photos/shanxi/`；extras 內嵌 `player/shanxi/media/extras/`（控 Surge 體積）
- 山西頁入口：「照片播放器 · 全部照片 →」
- 重建：`python3 scripts/build_shanxi_player.py`（sips 須 sandbox 外）

**參考**：`CLAUDE.md` Photos SSOT；Live 待 deploy

---

## 2026-07-30 — Deploy 遷移就緒（Cloudflare Pages 備援；未切換）

> **狀態：已被上方「Production Cutover → Cloudflare Pages」覆寫（2026-07-30）。** 以下保留為遷移前決策軌跡。

**性質**：Owner 指示「先準備」· Knowledge＋腳本就緒 · **當時** Production 不變。

**問題：** Surge 體積／上傳不穩；評估過 Render（付費）與其他靜態主機。

**決策：**
- **Production 維持** `cluttered-breath.surge.sh`（Surge）直到 Owner 明確核准 Cutover
- **首選備援**：Cloudflare Pages（非 Render）
- 就緒產物：`.ai-kos/DEPLOY_MIGRATION.md`、`deploy/cloudflare/wrangler.toml`、`scripts/deploy_cloudflare_pages.sh`（需 `MIGRATE_CONFIRM=1`）
- 上傳包不變：仍用 `dist-surge-upload`（壓縮靜態包；目錄名歷史遺留）
- 試跑可與 Surge 並存；**不得**在未核准時改 Daily Update 預設 Deploy

**不採（本階段）：** 付費 Render 作為主路徑；媒體全面 CDN（仍為 Phase 3 後備）

**參考**：`.ai-kos/DEPLOY_MIGRATION.md` · `.ai-kos/INFRASTRUCTURE.md`

---

## 2026-07-30 — 每季旅程分網域部署（Owner 定稿）

> **修正（Cutover）：** 本季 Production 宿主已改為 Cloudflare Pages `travel-site-quarter`；「每季分站」精神保留，但**下季改為新 Pages project**（不再預設新 Surge 網域）。見上方 Cutover 決策。

**性質**：Owner 定稿 · HARD RULE（原 Surge 體積上限對策；宿主已遷移）。

**問題：** 原圖／未壓縮 `dist` 過大；壓縮包 `dist-surge-upload` 亦隨旅程累積（已 ~146MB），單一 Surge Student 站會再撞上限或連線中斷。

**決策：**
- **本季（波羅的海 `bldh-trio` ＋ 西伯利亞 `baikal-rail`）**：繼續共用 Production `cluttered-breath.surge.sh`；只部署壓縮包（`dist-surge-upload`／`package_preview_deploy`），禁止部署未壓縮 `dist` 或 `photos/` 原圖
- **西伯利亞結束後的下一季新旅程**：必須使用**新 Surge 網域**＋**該季獨立壓縮包**（只含該季 HTML／縮圖）；不得把舊季媒體再打進新站
- 可選輕量入口站用連結指向各季網域；不強制本 repo 立刻拆站
- 新季開站時由 Owner 指定網域名稱，再更新本決策與 `RESUME_CONTEXT`／`DAILY_TRAVEL_UPDATE` Deploy 指令
- **備援：** 若改走 Cloudflare Pages，每季可對應新 Pages project（見 `DEPLOY_MIGRATION.md`）；不自動切換

**不採（本階段）：** 照片全面改 CDN（保留為體積仍失控時的後備）

**參考**：`.ai-kos/RESUME_CONTEXT.md` Infrastructure · `.ai-kos/DAILY_TRAVEL_UPDATE.md` Step 6 · `.ai-kos/DEPLOY_MIGRATION.md`

---

## 2026-07-30 — 描述區 v1.2「資深旅遊作家」規則

**性質**：Owner 定稿（以後所有描述區；西伯利亞同）。

**決策：** 描述區依 6 條硬規則改寫——身在現場感官切入、資訊嵌入敘事、禁導覽詞、禁流水帳、結尾個人感受（非總結）、4–6 句精簡有畫面。定稿範例：聖靈教堂古鐘。

**承接：** v1.1 壓縮四拍仍為內部節奏；寫法以 v1.2 為準。

**參考**：`.ai-kos/CONTENT_STYLE.md` v1.2 · `CLAUDE.md`

---

## 2026-07-30 — 景點壓縮四拍（覆寫知性見聞）

**性質**：Owner 文風定稿（BLDH Day 7–10 批次適用，全站新增／改寫沿用）。

**問題：** 07-29「知性見聞優先」讓景觀卡偏向設計理念／建造邏輯長文，讀起來像導遊詞或 Wikipedia，不像旅行書。

**決策：**
- 景點卡採**壓縮四拍**（當下 → 故事 1–2 句 → 旅遊雜記 → 一句收尾），寫成一小段散文
- 景點知識約 **30%**，雜記與感受約 **70%**
- **廢止** 07-29「景觀描述 — 知性見聞優先」
- 主站不顯示 emoji／區塊標題；愛沙尼亞互動札記與 day07 EE–day10 同步

**適用：**
- 立即：`bldh-trio` Day 7–10
- 下一旅程：`baikal-rail`（西伯利亞）— **每天每張照片**依同一原則寫旅行書，不做冷冰冰導覽介紹

**參考**：`.ai-kos/CONTENT_STYLE.md` v1.1 · `CLAUDE.md` · `content/bldh-trio/day07.md`–`day10.md`

---

## 2026-07-29 — 隨身碟／離線：音檔必須相對路徑

**性質**：離線相容修正（Day 2 立陶宛黑膠播放器）。

**問題：** `lithuania_15s.mp3` 曾用絕對路徑 `/photos/...`，線上 surge 可播；**隨身碟／file://** 開 `trips/*.html` 時路徑指到磁碟根目錄 → 播放器無聲／載入失敗。

**決策：**
- 音檔與照片／影片一律用 `../photos/...`（相對 `trips/`）
- 打包隨身碟前用本機 `file://` 或相對目錄開啟驗證黑膠＋影片

**參考：** `scripts/build.py`（`audio_src`）· `templates/shell.html`（`.lt-vinyl`）

---

## 2026-07-26 — 影片配樂淡入淡出（800ms）

**性質**：主站聽覺體驗（接續有聲修正）。

**決策：**
- 點擊播放：音量 **0 → 1** 淡入約 **800ms**
- 手動停止／接近片尾：音量 **→ 0** 淡出約 **800ms**（片尾依剩餘秒數縮短）
- `prefers-reduced-motion: reduce` 時改為瞬切（無漸變）
- 僅影響有音軌之 `.video-card`；無音軌檔行為不變

**參考**：`templates/shell.html`（`FADE_MS`／`fadeVolume`）

---

## 2026-07-26 — 點擊播放影片＝有聲（取消 muted）

**性質**：主站互動修正（Day 7 圖雷達塔樓影片無聲回報）。

**決策：**
- `<video>` 仍保留初始 `muted playsinline`（行動端相容）
- **點擊播放時** `video.muted = false`（使用者手勢允許出聲）
- 無音軌影片（如 Day1 栗子攤）不受影響；有音軌影片（如 Day7 `turaida-tower-gauja.mp4`）放出原片環境音／現場聲
- 此為原片音軌，**不是** `MUSIC_CLICK_PLAN.md` 的景點配樂功能

**參考**：`templates/shell.html` `startPlayback`

---

## 2026-07-25 — Day1 栗子攤點擊播放影片（主站 sites 卡）

**性質**：主站互動（網站版）；雜誌 HTML 維持靜態照片。

**決策：**
- Markdown 可選標記：`![alt](poster.jpg){video=path.mp4}`（由 `split_heading_image` 解析）
- 首例：伊斯坦堡街頭烤栗子 → `photos/bldh-trio/day01/istanbul-chestnut-stall.mp4`（~10s，初始 muted／playsinline；點擊後 unmute，該檔無音軌）
- UI：本日照片網格拉出 → 底端 `.sites-featured` 獨立放大（左圖右文）；poster → hover 微放大＋栗子裂口播放鈕 bounce → 點擊淡出照片淡入影片；結束自動回 poster
- 不開 lightbox（`.video-card` 排除）；不加 Plyr 等第三方套件
- 原圖 JPG 不改（僅疊互動層）

**參考**：`templates/base.css`（`.video-card`）· `templates/shell.html` · `scripts/build.py` `render_video_site_img`

---

## 2026-07-20 — 景點點擊播放音樂＝計畫書先入庫、暫不實作／不為此改部署

**性質**：產品互動規格（延後執行）。

**決策：**
- 計畫 SSOT：`content/bldh-trio/source/MUSIC_CLICK_PLAN.md`（旅客／Agent 依此執行）
- `CLAUDE.md` 僅掛索引；**現階段不改站上 UI、不為此單獨 deploy**
- 開工資格：對應景點已入站＋合法 15–30s 音檔＋使用者明示「開始做配樂」
- 規格要點：點擊角落微圖標（非標準 ▶️）、淡入淡出、同頁單曲

---

## 2026-07-18 — 排版風格＝Knowledge（Template Library 原則）

**性質**：架構原則（使用者明確陳述，記錄／同步，非我主動 scaffold）。

**原則：** AI-KOS 將**排版風格（Layout）視為 Knowledge，而非 Prompt**。所有模板皆為**可重複使用的 Knowledge Asset**。Project **不直接描述排版**，而是**指定使用哪一個 Template**。

**知識流：**

```
Knowledge → Template → Renderer → Output
```

**首個具體實例（已驗證）：**

| 層 | 實體 |
|----|------|
| Knowledge | 旅程內容 `content/bldh-trio/day*.md`（旅行札記 v1.0） |
| Template | `city-magazine-template.md`（城市雜誌風，根目錄 SSOT） |
| Renderer | `scripts/build_bldh_magazine.py` |
| Output | `content/bldh-trio/bldh-trio-magazine.html` |

**含義：**
- Project 端只需「指定 Template」，不再在 prompt 內描述排版細節
- 同一 Template 可被多個 Project／旅程重用
- 模板規格變更 = 修改 Template（Knowledge），Renderer 依模板產出

**待批准（Suggestion，未執行）：** 是否新開 `.ai-kos/TEMPLATES.md` 作為正式 Template Library 登錄（依 `INDEX.md` 治理原則，新增治理文件需明確批准）。

---

## 2026-07-18 — BLDH Trio 指定「城市雜誌風排版器模板」為正式排版規格

**性質**：專案排版規格決策（僅限 `bldh-trio`，不影響其他旅程或 `build.py` 主流程）。

**決策：** 波羅的海三小國 11 天（`bldh-trio`）專案，所有**排版、生成、合併、渲染**流程一律套用「城市雜誌風排版器模板」。

| 角色 | 檔案 |
|------|------|
| **模板（SSOT）** | 根目錄 `city-magazine-template.md` |
| **排版器** | `scripts/build_bldh_magazine.py`（header 已標註以模板為準） |
| **輸出** | `content/bldh-trio/bldh-trio-magazine.html`（standalone，`build.py` 不處理） |

**模板規格摘要：** 大標題＋斜體副標（原文首句）· 行距 1.75 · 字重 300–400 · 全寬圖片不裁切／不變形 · 上下留白 · `---` 細線分隔 · `✦` 金線側註 · Day kicker（Day 01）· meta 卡片（航班／住宿／領隊／午晚餐）· 歷史／古蹟／預告分節標。

**約束：**
- 排版器必須可重複執行，且產出恆依 `city-magazine-template.md`
- 只調整排版，不改動 `day*.md` 原始文字（layout only）
- 未來新增的「城市散步類」旅程沿用同一模板

**參考**：`city-magazine-template.md` · `scripts/build_bldh_magazine.py`

---

## 2026-07-17 — Knowledge First 營運驗證（Baltic Day 3）

**性質**：營運驗證紀錄（非新規則、非流程重設計）。記於此處而非 AI-KOS 憲法——憲法不放營運範例。

**背景**：Baltic Day 3（07/13 維爾紐斯）以一個真實案例驗證了 AI-KOS **Rule 0：Knowledge First**。

**觀察到的工作流：**

1. 先驗證來源完整性（Drive SSOT 掃描）
2. 偵測到同步落差（Drive `0713/` 約 27 張，本機僅 2 張）
3. 先修復知識完整性（增量同步補齊 Day 3 照片）
4. 才生成旅行內容（札記 + build + deploy）

**關鍵教訓：**

> **正確的知識，先於正確的內容（Correct knowledge precedes correct content）。**

若當時直接就本機既有 2 張照片撰稿，會漏掉整天的維爾紐斯行程；先補知識再產出，才得到完整交付。

**參考**：`.ai-kos/STATUS.md`（2026-07-17 Day 3 entry）· `AI-KOS.md` Rule 0 / Rule -1（真實專案驗證）

---

## 2026-07-17 — Observability 原則 + Operational Confidence 選填欄位

**決策**：對齊已被真實營運驗證的知識，於文件層面同步（不改行為、不重設計流程）。

1. **Observability** 確立為 AI-KOS **營運設計原則**，記於 `AI-KOS.md`（哲學層級，無實作細節）：讓人類理解 AI 正在做什麼、進度、營運健康、是否需介入。其具體展現即既有的**固定營運摘要**與 **Optional Safety Layer** 批准前摘要——屬同一原則的展現，故僅交叉引用、不另立新機制。
2. **Operational Confidence** 加入 `DAILY_TRAVEL_UPDATE.md`，為**選填**欄位（High/Medium/Low + Reason）。整合進既有「可選附註」區，不新增必填欄位、不取代 `Status`。

**一致性處理（發現的潛在衝突）：**

- `AI-KOS/CLAUDE.md`：「Prefer evidence-backed conclusions over self-reported confidence.」
- 為避免牴觸，Operational Confidence 明確定義為**由摘要既有證據彙整**（Source / Build / Deploy / Live / review_required），非主觀自評。

**理由**：兩項知識已由多次真實營運 session 驗證（符合 Rule -1）；以最小幅度落於最合適文件，維持一致、避免重複。

---

## 2026-07-16 — Wake command：Ingest（跨文件相關內容同步）

**決策**：新增喚醒／替代指令 **Ingest**（`ingest` 同等）。

**定義：**

> **Ingest** = 修改跨文件中的相關內容。

**行為：**

1. 以本次（或使用者指定）變更為中心，搜尋仍引用舊名稱、舊 URL、舊 Phase／Mode、舊模板的相關文件  
2. **一併修改**使 AI-KOS、操作手冊、父層 `CLAUDE.md`、現行 deploy／sync 指引一致  
3. 歷史 archive（如 STALE `SESSION.md`、已標 legacy 的舊敘事）可保留，但**可執行指令**必須改為現行正確值  
4. 不做無關功能開發、不做 bulk rewrite  
5. 完成後簡報：改了哪些檔、刻意未改哪些

**與其他指令關係：**

| 指令 | 用途 |
|------|------|
| **開工** | 恢復記憶 → 預設 Daily Travel Update |
| **收工** | 寫斷點 → 道別 |
| **Ingest** | 跨文件相關內容同步（知識一致性） |

**理由**：Operational Phase 下仍需偶爾對齊文件；用短指令代替長說明，避免漏改相關檔。

---

## 2026-07-16 — Operational Phase 正式生效

**決策**：自本日起 travel-site 正式進入 **Operational Phase**。`6779dac`（Workspace Integrity）已上遠端；治理基建凍結為夠用狀態。

**原則：**

> AI-KOS 服務旅行書，而不是旅行書繼續服務 AI-KOS。

**自 2026-07-17 起預設工作：** Daily Travel Update（照片 → 札記 → build → deploy → 固定營運摘要）。  
**非預設：** 擴充 AI-KOS、路徑再遷移、架構重構、舊內容 bulk rewrite（需使用者明確授權）。

**理由**：Integrity 與 Daily Update 模板已就緒；繼續打磨 KOS 會反客為主。

---

## 2026-07-16 — Daily Update 固定營運摘要（Handoff）

**決策**：Daily Travel Update 每次回報**結尾**必須輸出固定短摘要（欄位名不可改），格式見 `.ai-kos/DAILY_TRAVEL_UPDATE.md` § 輸出模板。

**必填欄位**：Date / Trip / New Photos / Updated Day / Travel Notes / Build / Deploy / Live Verification / Commit / Production / Status

**理由**：營運已穩定；固定摘要方便每日掃讀與跨 session 對帳，避免表格與敘事混雜。

**參考**：使用者核定範例（2026-07-13 Baltic，Commit `ce389e9`）

---

## 2026-07-16 — Canonical workspace path（Documents ONLY）

**決策**：travel-site 與所有旅遊子專案**唯一**工作區為 Documents。Desktop 路徑**永久禁止**。

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
FORBIDDEN: /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
New projects: create under /Users/mac/Documents/Projects/旅遊/<project-name>/
```

**政策**：

1. Agent / 腳本 / 文件 / Cursor workspace **一律**使用 Documents 路徑
2. **禁止**「Desktop 或 Documents 擇一」「try both paths」等模糊指引
3. **禁止**在 Desktop 路徑讀寫、commit、push、deploy
4. 若 Cursor workspace 指向 Desktop → Agent **立即停止**並要求使用者重新開啟 Documents 資料夾
5. `~/Desktop/旅遊/` 僅允許導向文件（`DEPRECATED.md` / redirect `CLAUDE.md`）；**禁止**存在可被 Cursor 開啟的 `travel-site/` 子目錄
6. Workspace Integrity SSOT：`.ai-kos/WORKSPACE.md`（路徑衝突時以此為準）
7. 若本機 git 物件損壞，優先自 `origin/main` 還原；無法安全修復則 **rebuild clone**，不得沿用半壞 repo

**理由**：2026-07-15 桌面整理後專案已遷移；Cursor 若開錯 workspace 會導致 agent 在空殼或錯誤路徑工作，造成資料遺失。2026-07-16 Integrity 稽核確認：路徑已在 Documents，但 Desktop 假專案目錄與損壞 blob 仍會造成「看似還在舊路徑」的錯覺。

---

## 2026-07-16 — Daily Travel Photo Sync（Operational Phase · 08:00）

**決策**：自 2026-07-16 起，travel-site 進入 **Daily Travel Photo Sync** 營運規則 — 每日 **08:00（Asia/Taipei）** Agent **主動**執行 Daily Travel Update，無需使用者提醒。  
（舊稱 Operational Mode；正式名稱以 **Operational Phase** 為準，見上方條目。）

**流程**（canonical：`.ai-kos/DAILY_TRAVEL_UPDATE.md`）：

1. Drive SSOT 掃描（`.ai-kos/INFRASTRUCTURE.md`，不 re-ask Folder ID）
2. 增量同步（比對 `photo-sync.json` manifest）
3. 更新旅行札記（所有新照片，`.ai-kos/CONTENT_STYLE.md` 第一人稱視角）
4. Build → Verify → Deploy → Commit/Push（有變更時）→ **固定營運摘要** Handoff

**Error Policy**：auth / permission / infrastructure 錯誤 — **立即停止、不重試、回報根因**。

**理由**：

- Operational Phase 需固定節奏，避免照片與札記滞後
- 單一 canonical 規則供開工與排程 session 遵循
- 與既有 Drive SSOT、增量 sync 決策一致，不重複基礎設施定義

**Active path**：`/Users/mac/Documents/Projects/旅遊/travel-site/`

**參考**：`.ai-kos/DAILY_TRAVEL_UPDATE.md` · `.ai-kos/RESUME_CONTEXT.md` · `content/baikal-rail/source/PHOTO_SYNC.md`

---

## 2026-07-13 — Google Drive Shared Folder 永久 SSOT

**決策**：斌哥所有旅行照片以單一 Google Drive Shared Folder 為**永久唯一來源**（Single Source of Truth）。Folder ID 固定為 `1qLKyqo2HAjA_Z_-ucwCUYoTKGgEVqkrD`，不因新旅程而更換。

**政策**：

1. **固定根資料夾** — Shared Folder URL / ID 不變；各次旅行以子資料夾區分
2. **Resume 不 re-ask** — 恢復 session 或旅行更新時，直接使用此 Folder，不再要求使用者提供路徑
3. **Daily Update 增量同步** — 每次日常更新由此 Folder 增量同步（見 Incremental Sync 決策）
4. **Photo Sync 統一入口** — 所有 trip 的照片同步一律從此 Shared Folder 開始

**理由**：

- 避免每次 session 重複確認 Drive 路徑，降低交接摩擦
- 單一 SSOT 便於跨 trip 管理與備份
- 子資料夾模型已於 baikal-rail 驗證（`DRIVE_FOLDER_CONVENTION.md`）

**參考**：`.ai-kos/INFRASTRUCTURE.md` · `content/baikal-rail/source/photo-sync-config.json`

---

## 2026-07-13 — Google Drive 採 Incremental Sync

**決策**：Baikal Rail 照片自 Google Drive 匯入時，採**增量同步**（manifest 驅動），而非每次全量重新下載。

**理由**：

1. **避免重複下載** — 以 `drive_file_id` 與 SHA-256 hash 去重，節省頻寬與時間
2. **保留手動策展** — 不覆寫 `dayXX.md` 中已有 `![...]` 的標題；不覆寫既有 `photos/` 檔案
3. **支援每日同步** — 使用者上傳新照片後，單一指令即可只處理增量
4. **不猜 Day** — 路徑無法解析時不強制歸類，改進 review 流程（見下一則決策）

**實作**：`scripts/sync_baikal_photos.py` + `content/baikal-rail/source/photo-sync.json`

**不修改**：`scripts/build.py`、`scripts/build_prototype.py`、網站 UI/CSS、其他 trip

---

## 2026-07-13 — AI 無法判定 Day 時 → Review Required

**決策**：當 Drive 路徑缺少 `Day XX - 景點名` 結構，或資料夾名無法對應 `dayXX.md` landmark 標題時，**不進行自動分類**，改寫入 `photo-sync.json` → `review_required`。

**理由**：

1. 日期資料夾（如 `0711/`、`0712/`）或 `IMG_xxxx` 檔名無法可靠對應行程天數
2. 錯誤自動歸類會污染 `photos/baikal-rail/` 與 `dayXX.md`，比待審更難修復
3. 人工將照片移至正確 Drive 資料夾後，下次 sync 即可自動匯入

**拒絕的替代方案**：依 EXIF 日期或檔名推測 Day — 準確率不足，且與「Knowledge First」衝突

**參考**：`content/baikal-rail/source/DRIVE_FOLDER_CONVENTION.md`
