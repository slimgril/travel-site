#!/usr/bin/env python3
"""
从浏览器下载的 ZIP 文件自动解压并映射到 dayXX 文件夹

使用方法：
1. 从 Google Drive 网页下载文件夹（会得到一个 zip 文件）
2. 将 zip 文件放到 Downloads 目录
3. 运行此脚本：python3 process_download.py [zip文件名]
   或直接运行让脚本自动查找最新的 zip
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import re
from datetime import datetime

# 配置
TARGET_DIR = Path("/Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail")
DOWNLOADS_DIR = Path.home() / "Downloads"
TEMP_EXTRACT_DIR = TARGET_DIR / "_temp_extract"

# 旅程起始日期
START_DATE = 3  # 8月3日

def find_latest_zip():
    """在 Downloads 目录找最新的 zip 文件"""
    zip_files = list(DOWNLOADS_DIR.glob("*.zip"))
    if not zip_files:
        return None
    # 按修改时间排序，返回最新的
    return max(zip_files, key=lambda p: p.stat().st_mtime)

def extract_zip(zip_path):
    """解压 zip 文件"""
    print(f"📦 解压文件: {zip_path.name}")

    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR)
    TEMP_EXTRACT_DIR.mkdir(parents=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_EXTRACT_DIR)
        print(f"✅ 解压完成")
        return True
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False

def find_date_folders(base_dir):
    """递归查找所有日期格式的文件夹（0803, 0804等）"""
    date_folders = []

    for item in base_dir.rglob("*"):
        if item.is_dir():
            # 匹配 0803, 0804 等格式
            if re.match(r'^0[3-9]\d{2}$|^08\d{2}$', item.name):
                date_folders.append(item)

    return sorted(date_folders, key=lambda x: x.name)

def map_date_to_day(date_str):
    """将日期字符串映射到 day 编号"""
    # 0803 -> day01, 0804 -> day02, etc.
    try:
        day_num = int(date_str[-2:])  # 取最后两位
        day_index = day_num - START_DATE + 1
        if 1 <= day_index <= 20:
            return f"day{day_index:02d}"
    except:
        pass
    return None

def process_folders(date_folders):
    """处理日期文件夹，映射到目标位置"""
    print(f"\n📂 找到 {len(date_folders)} 个日期文件夹")

    mapping = []
    for folder in date_folders:
        day_name = map_date_to_day(folder.name)
        if day_name:
            mapping.append((folder, day_name))
            print(f"   {folder.name} → {day_name}")
        else:
            print(f"   ⚠️  {folder.name} 无法映射，跳过")

    if not mapping:
        print(f"❌ 没有可映射的文件夹")
        return False

    print(f"\n准备复制 {len(mapping)} 个文件夹")
    confirm = input("确认开始? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return False

    success_count = 0
    for src_folder, day_name in mapping:
        target_folder = TARGET_DIR / day_name

        # 检查目标是否存在
        if target_folder.exists():
            print(f"\n⚠️  {day_name} 已存在")
            choice = input(f"   覆盖? (y/n/skip): ").strip().lower()
            if choice == 'skip':
                print(f"   ⏭️  跳过")
                continue
            elif choice != 'y':
                print(f"   ❌ 取消")
                continue

            # 备份
            backup = TARGET_DIR / f"{day_name}.backup"
            if backup.exists():
                shutil.rmtree(backup)
            shutil.move(str(target_folder), str(backup))
            print(f"   📦 已备份至 {backup.name}")

        # 复制文件
        try:
            shutil.copytree(src_folder, target_folder)
            file_count = len([f for f in target_folder.rglob("*") if f.is_file()])
            print(f"   ✅ {day_name}: {file_count} 个文件")
            success_count += 1
        except Exception as e:
            print(f"   ❌ {day_name} 失败: {e}")

    return success_count > 0

def cleanup():
    """清理临时文件"""
    if TEMP_EXTRACT_DIR.exists():
        print(f"\n🗑️  清理临时文件...")
        shutil.rmtree(TEMP_EXTRACT_DIR)

def main():
    print("=" * 60)
    print("Google Drive ZIP 自动处理工具")
    print("=" * 60)

    # 获取 zip 文件路径
    if len(sys.argv) > 1:
        zip_path = Path(sys.argv[1])
        if not zip_path.is_absolute():
            zip_path = DOWNLOADS_DIR / zip_path
    else:
        print(f"\n🔍 在 Downloads 目录查找最新的 zip 文件...")
        zip_path = find_latest_zip()
        if not zip_path:
            print(f"❌ 未找到 zip 文件")
            print(f"\n提示：请先从 Google Drive 网页下载文件夹")
            print(f"      然后运行: python3 process_download.py [zip文件名]")
            return 1
        print(f"   找到: {zip_path.name}")
        print(f"   时间: {datetime.fromtimestamp(zip_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

        confirm = input(f"\n使用此文件? (y/n): ").strip().lower()
        if confirm != 'y':
            print(f"已取消")
            return 0

    if not zip_path.exists():
        print(f"❌ 文件不存在: {zip_path}")
        return 1

    # 解压
    if not extract_zip(zip_path):
        return 1

    # 查找日期文件夹
    date_folders = find_date_folders(TEMP_EXTRACT_DIR)

    if not date_folders:
        print(f"\n⚠️  未找到日期格式的文件夹（08XX）")
        print(f"   解压内容位于: {TEMP_EXTRACT_DIR}")
        print(f"   请检查文件夹结构")
        return 1

    # 处理和映射
    success = process_folders(date_folders)

    # 清理
    cleanup()

    if success:
        print(f"\n" + "=" * 60)
        print(f"✅ 处理完成！")
        print(f"=" * 60)
        return 0
    else:
        print(f"\n❌ 处理失败")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n已中断")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        sys.exit(1)
