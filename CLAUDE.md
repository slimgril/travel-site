# travel-site — Agent guidance

## Workspace（canonical — HARD RULE）

```
CANONICAL PROJECT ROOT: /Users/mac/Documents/Projects/旅遊/travel-site
WORKSPACE PARENT:       /Users/mac/Documents/Projects/旅遊/
FORBIDDEN:              /Users/mac/Desktop/旅遊/ — do not read, write, commit, or deploy from Desktop
```

**SSOT：** `.ai-kos/WORKSPACE.md` → `.ai-kos/RESUME_CONTEXT.md` → `.ai-kos/DAILY_TRAVEL_UPDATE.md`

## Phase

**Operational Phase** — AI-KOS 服務旅行書；旅行書不再服務 AI-KOS。  
預設工作：Daily Travel Update（照片 → 札記 → build → deploy → 固定營運摘要）。

## Wake commands

| 指令 | 行為 |
|------|------|
| **開工** | 讀 `.ai-kos/RESUME_CONTEXT.md`；預設 Daily Travel Update |
| **收工** | 寫輕量斷點至父層 `旅遊/CLAUDE.md` 後道別 |
| **Ingest** | **跨文件相關內容同步**：找出本次修改牽涉的相關文件並一併改一致 |

### Ingest（知識維護，非功能開發）

> **Ingest** = 修改跨文件中的相關內容。

- 對齊舊名稱、舊 URL、舊 Phase／Mode、舊模板
- 歷史 archive 可保留；**可執行指令**必須改為現行正確值
- 不做無關功能、不做 bulk rewrite
- 詳見 `.ai-kos/DECISIONS.md` · `.ai-kos/RESUME_CONTEXT.md`
