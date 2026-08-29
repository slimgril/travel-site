#!/usr/bin/env python3
"""
贝加尔铁路照片同步脚本
从 Google Drive 下载照片到本地 dayXX 文件夹

Google Drive Folder: https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty
Target: /Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail/
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re

# 配置
GOOGLE_DRIVE_URL = "https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty"
TARGET_DIR = Path("/Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail")
TEMP_DOWNLOAD_DIR = TARGET_DIR / "_temp_download"

def download_from_gdrive():
    """从 Google Drive 下载文件夹"""
    print(f"📥 开始从 Google Drive 下载...")
    print(f"   源: {GOOGLE_DRIVE_URL}")
    print(f"   临时目录: {TEMP_DOWNLOAD_DIR}")

    # 清理旧的临时目录
    if TEMP_DOWNLOAD_DIR.exists():
        print(f"🗑️  清理旧的临时目录...")
        shutil.rmtree(TEMP_DOWNLOAD_DIR)

    TEMP_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 使用 gdown 下载整个文件夹
    cmd = [
        "gdown",
        "--folder",
        GOOGLE_DRIVE_URL,
        "-O", str(TEMP_DOWNLOAD_DIR)
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 下载完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False

def map_folders():
    """映射下载的文件夹到 dayXX 格式"""
    print(f"\n📂 开始映射文件夹...")

    if not TEMP_DOWNLOAD_DIR.exists():
        print(f"❌ 临时目录不存在: {TEMP_DOWNLOAD_DIR}")
        return False

    # 获取所有下载的子文件夹
    downloaded_folders = sorted([
        f for f in TEMP_DOWNLOAD_DIR.iterdir()
        if f.is_dir() and not f.name.startswith('.')
    ])

    if not downloaded_folders:
        print(f"⚠️  临时目录中没有找到文件夹")
        return False

    print(f"   找到 {len(downloaded_folders)} 个文件夹:")
    for folder in downloaded_folders:
        print(f"     - {folder.name}")

    # 映射逻辑：支持多种格式
    # 1. 日期格式: "0803", "0804" -> day01, day02 (从8月3日开始)
    # 2. Day格式: "Day 1", "Day1", "day01" -> day01, day02
    # 3. 纯数字: "1", "01" -> day01, day02
    mapping = []

    # 旅程起始日期：2026年8月3日
    START_DATE = 3  # 8月3日

    for folder in downloaded_folders:
        folder_name = folder.name
        target_name = None

        # 尝试匹配日期格式 (MMDD 或 DD)
        if re.match(r'^0\d{3}$', folder_name):  # 0803, 0804 格式
            day = int(folder_name[-2:])  # 取最后两位作为日期
            day_num = day - START_DATE + 1
            if day_num > 0:
                target_name = f"day{day_num:02d}"
        # 尝试匹配 Day 格式
        elif match := re.search(r'(?:day\s*)?(\d+)', folder_name, re.IGNORECASE):
            day_num = int(match.group(1))
            target_name = f"day{day_num:02d}"

        if target_name:
            mapping.append((folder, target_name))
        else:
            print(f"⚠️  无法从 '{folder_name}' 提取日期编号，跳过")

    if not mapping:
        print(f"❌ 没有可映射的文件夹")
        return False

    print(f"\n📋 映射计划:")
    for src, dst in mapping:
        print(f"   {src.name} → {dst}")

    # 确认映射
    confirm = input(f"\n确认映射? (y/n): ").strip().lower()
    if confirm != 'y':
        print(f"❌ 用户取消")
        return False

    # 执行映射
    print(f"\n🔄 执行同步...")
    for src_folder, target_name in mapping:
        target_path = TARGET_DIR / target_name

        # 如果目标文件夹已存在，询问是否覆盖
        if target_path.exists():
            action = input(f"   {target_name} 已存在，是否覆盖? (y/n/skip): ").strip().lower()
            if action == 'skip':
                print(f"   ⏭️  跳过 {target_name}")
                continue
            elif action != 'y':
                print(f"   ❌ 取消覆盖 {target_name}")
                continue
            else:
                # 备份现有文件夹
                backup_path = TARGET_DIR / f"{target_name}.backup"
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                shutil.move(str(target_path), str(backup_path))
                print(f"   📦 备份至 {backup_path.name}")

        # 复制文件夹
        shutil.copytree(src_folder, target_path)
        print(f"   ✅ {src_folder.name} → {target_name}")

    return True

def cleanup():
    """清理临时文件"""
    if TEMP_DOWNLOAD_DIR.exists():
        print(f"\n🗑️  清理临时目录...")
        shutil.rmtree(TEMP_DOWNLOAD_DIR)
        print(f"   ✅ 清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print("贝加尔铁路照片同步工具")
    print("=" * 60)

    # 确认目标目录
    print(f"\n目标目录: {TARGET_DIR}")
    if not TARGET_DIR.exists():
        print(f"❌ 目标目录不存在")
        return 1

    # 下载
    if not download_from_gdrive():
        print(f"\n❌ 下载失败，退出")
        return 1

    # 映射
    if not map_folders():
        print(f"\n❌ 映射失败")
        cleanup()
        return 1

    # 清理
    cleanup()

    print(f"\n" + "=" * 60)
    print(f"✅ 同步完成!")
    print(f"=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
