# 贝加尔铁路照片同步指南

## 快速开始

### 方法 1：使用 Python 脚本（推荐）

```bash
cd "/Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail"
python3 sync_photos.py
```

脚本会：
1. 从 Google Drive 下载整个文件夹到临时目录
2. 自动识别文件夹名称中的日期编号（如 "Day 1", "day01" 等）
3. 映射到本地的 day01, day02... 格式
4. 询问确认后执行同步
5. 自动清理临时文件

### 方法 2：使用命令行直接下载

如果只想快速下载到临时目录查看：

```bash
# 下载到当前目录的 temp 文件夹
gdown --folder https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty -O temp

# 查看下载的内容
ls temp/

# 手动移动到对应的 day 文件夹
# 例如：mv temp/Day1/* day01/
```

## Google Drive 信息

- **文件夹名称**: 西伯利亚大铁路 20 日
- **URL**: https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty
- **Folder ID**: `1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty`
- **更新频率**: 斌哥每日更新

## 文件夹映射规则

Python 脚本会自动识别以下格式：
- `Day 1` → `day01`
- `Day1` → `day01`
- `day 01` → `day01`
- `01` → `day01`

如果文件夹名称不符合规则，脚本会跳过并提示。

## 注意事项

1. **备份**: 如果目标文件夹已存在，脚本会询问是否覆盖，并自动创建 `.backup` 备份
2. **确认**: 脚本会在执行前显示映射计划，需要手动确认
3. **临时文件**: 所有下载先保存到 `_temp_download/`，同步完成后自动清理

## 故障排查

### 下载失败
```bash
# 检查 gdown 是否安装
gdown --version

# 重新安装
pip3 install -U gdown
```

### 权限问题
```bash
# 给脚本添加执行权限
chmod +x sync_photos.py
```

### 大文件下载
如果 Google Drive 提示病毒扫描警告，在命令中添加 `--fuzzy` 参数：
```bash
gdown --folder URL -O temp --fuzzy
```
