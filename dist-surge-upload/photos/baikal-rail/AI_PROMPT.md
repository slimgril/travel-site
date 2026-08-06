# Google Drive 照片自动下载和映射 - AI 提示词

## 项目背景

贝加尔铁路旅行项目，需要从 Google Drive 共享文件夹同步照片到本地项目目录，并按日期映射到特定文件夹结构。

## Google Drive 信息

- **文件夹名称**: 西伯利亚大铁路 20 日
- **分享链接**: https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty
- **Folder ID**: `1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty`
- **内部结构**: 包含子文件夹 `0803`, `0804`, `0805`... 对应 8月3日、8月4日等
- **更新频率**: 斌哥每日更新新照片到对应日期文件夹

## 本地目录结构

```
目标路径: /Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail/

预期结构:
├── day01/    ← 对应 Google Drive 的 0803 文件夹（8月3日）
├── day02/    ← 对应 0804（8月4日）
├── day03/    ← 对应 0805（8月5日）
├── ...
└── day20/    ← 对应 0822（8月22日）
```

## 映射规则

| Google Drive 文件夹 | 本地文件夹 | 说明 |
|-------------------|----------|------|
| `0803` | `day01` | 旅程第1天（8月3日） |
| `0804` | `day02` | 旅程第2天（8月4日） |
| `0805` | `day03` | 旅程第3天（8月5日） |
| ... | ... | 依此类推 |
| `0822` | `day20` | 旅程第20天（8月22日） |

**映射公式**: 
- Google Drive 日期: `08{DD}` 格式
- 本地文件夹: `day{NN}` 格式，其中 NN = DD - 3 + 1（因为8月3日是第1天）
- 例如：`0805` → DD=05 → NN = 05-3+1 = 03 → `day03`

## 需求说明

### 核心功能要求

1. **批量下载**: 能够从 Google Drive 下载照片到本地
2. **分批处理**: 支持选择下载特定日期，避免一次性下载太大导致超时
3. **自动映射**: 下载后自动将 `08XX` 格式文件夹映射到 `dayXX` 格式
4. **可重复下载**: 允许重复下载已下载过的日期（用于更新或重新同步）
5. **备份机制**: 覆盖前自动备份现有内容
6. **容错处理**: 网络超时或失败时有清晰的错误提示

### 用户偏好

- 不要过于复杂的配置（如 rclone 需要授权配置）
- 支持命令行操作，有清晰的交互提示
- 可以自动确认（`-y` 参数）或交互式选择
- 操作简单，不易出错

### 已知问题

- **网络不稳定**: 下载大文件或整个文件夹容易超时
- **gdown 限制**: 使用 `gdown --folder` 下载整个主文件夹时不稳定
- **手动下载慢**: 从网页一个个文件下载太耗时

## 期望的解决方案

### 方案1：分批下载脚本（推荐）

创建 Python 脚本 `sync_photos_batch.py`，支持：

**使用示例**:
```bash
# 交互式选择
python3 sync_photos_batch.py

# 下载特定日期
python3 sync_photos_batch.py 03 04 05

# 自动确认模式
python3 sync_photos_batch.py 03 -y

# 下载所有
python3 sync_photos_batch.py all -y
```

**脚本要求**:
- 使用 `gdown` 库下载
- 支持日期格式识别：`0803`, `08{DD}` → `day{NN}`
- 每次下载一个日期文件夹，避免超时
- 覆盖前询问确认，并自动备份
- 清晰的进度提示和错误处理

### 方案2：从浏览器下载的 ZIP 文件自动解压映射

用户从 Google Drive 网页下载 zip 压缩包后，脚本自动：
1. 解压 zip 文件
2. 识别日期文件夹
3. 映射到对应的 day 文件夹
4. 清理临时文件

### 方案3：手动映射工具

从已下载到临时目录（`_temp_download/`）的内容直接映射：
```bash
_temp_download/0803/ → day01/
_temp_download/0804/ → day02/
```

## 技术栈

- **Python 3.14+**: 主要脚本语言
- **gdown**: Google Drive 下载工具（已安装）
- **标准库**: shutil, pathlib, subprocess, re

## 使用场景

### 场景 1: 首次同步所有照片
```bash
python3 sync_photos_batch.py all -y
```

### 场景 2: 同步最新几天的照片
```bash
python3 sync_photos_batch.py 03 04 05 -y
```

### 场景 3: 重新下载某天照片（因为不完整或有更新）
```bash
python3 sync_photos_batch.py 04
# 脚本会提示是否覆盖，选择 y 确认
```

### 场景 4: 从已有临时文件映射
```bash
# 手动命令
cp -r _temp_download/0803/* day01/
```

## 文件清单

在 `/Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail/` 目录下应创建：

1. **sync_photos_batch.py** - 主下载脚本
2. **使用指南.md** - 详细的中文使用说明
3. **sync.sh** - 简化的执行脚本（可选）

## AI 助手指令

当用户提供此提示词时，AI 助手应该：

1. 确认理解项目背景和映射规则
2. 检查已安装的工具（gdown, Python 版本）
3. 创建或更新下载脚本
4. 提供清晰的使用说明
5. 处理错误情况并提供替代方案
6. 必要时创建辅助工具（zip 解压映射、手动映射等）

## 常见问题处理

### 问题：网络超时
- 解决：改用分批下载，每次只下载一个日期
- 或：使用浏览器下载 zip 文件

### 问题：文件夹映射错误
- 检查：Google Drive 文件夹命名格式
- 确认：映射公式计算正确

### 问题：覆盖已有内容
- 要求：脚本必须先询问确认
- 必须：自动备份为 `.backup` 文件夹

---

## 快速开始模板

将以下内容发送给 AI 助手：

```
我需要从 Google Drive 下载照片并映射到本地文件夹。

Google Drive: https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty
本地目录: /Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail/

映射规则: 0803→day01, 0804→day02, 0805→day03...（8月3日是第1天）

需求:
1. 创建分批下载脚本，支持选择特定日期
2. 支持可重复下载和自动确认
3. 覆盖前备份
4. 处理网络超时问题

已安装: Python 3.14, gdown
```
