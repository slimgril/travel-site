#!/usr/bin/env python3
"""
贝加尔铁路照片分批下载脚本
支持选择特定日期下载，可重复下载

使用方法：
  python3 sync_photos_batch.py          # 交互式选择
  python3 sync_photos_batch.py 03       # 下载8月3日（会询问确认）
  python3 sync_photos_batch.py 03 -y    # 下载8月3日（自动确认）
  python3 sync_photos_batch.py 03 04 05 # 下载多个日期
  python3 sync_photos_batch.py all -y   # 下载所有（自动确认）
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re

# 配置
TARGET_DIR = Path("/Users/mac/Documents/Projects/斌哥旅遊書/photos/baikal-rail")
TEMP_BASE_DIR = TARGET_DIR / "_temp_batch"

# 旅程日期配置（8月3日-8月22日，共20天）
START_DATE = 3
END_DATE = 22

def get_folder_id_for_date(date_str):
    """
    获取特定日期的 Google Drive 子文件夹 ID
    注意：这需要你先手动获取每个子文件夹的ID
    """
    # TODO: 这里需要填入每个日期文件夹的实际 folder ID
    # 目前我们使用主文件夹ID，gdown会下载整个文件夹然后我们筛选
    return "1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty"

def download_date(date_num):
    """下载指定日期的照片"""
    date_str = f"{date_num:02d}"
    folder_name = f"08{date_str}"  # Google Drive 中的文件夹名：0803, 0804...
    day_folder = f"day{date_num - START_DATE + 1:02d}"  # 本地文件夹名：day01, day02...

    print(f"\n{'='*60}")
    print(f"📥 下载 8月{date_num}日 → {day_folder}")
    print(f"{'='*60}")

    # 创建临时下载目录
    temp_dir = TEMP_BASE_DIR / date_str
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # 下载整个主文件夹（因为无法直接获取子文件夹ID）
    print(f"⏳ 正在下载... (这可能需要几分钟)")
    full_temp = TEMP_BASE_DIR / "full_download"
    if full_temp.exists():
        shutil.rmtree(full_temp)

    cmd = [
        "gdown",
        "--folder",
        "https://drive.google.com/drive/folders/1VnHEb__UrT7-MMOrTKfh8OB6lBFzE6Ty",
        "-O", str(full_temp)
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # 找到目标日期文件夹
        source_folder = full_temp / folder_name
        if not source_folder.exists():
            print(f"❌ 未找到文件夹 {folder_name}")
            # 列出实际下载的文件夹
            if full_temp.exists():
                print(f"   已下载的文件夹：")
                for item in full_temp.iterdir():
                    if item.is_dir():
                        print(f"     - {item.name}")
            return False

        # 复制到目标位置
        target_folder = TARGET_DIR / day_folder

        # 询问是否覆盖
        if target_folder.exists():
            print(f"\n⚠️  {day_folder} 已存在")
            choice = input(f"   覆盖? (y/n): ").strip().lower()
            if choice != 'y':
                print(f"   ⏭️  跳过")
                return False
            # 备份
            backup = TARGET_DIR / f"{day_folder}.backup"
            if backup.exists():
                shutil.rmtree(backup)
            shutil.move(str(target_folder), str(backup))
            print(f"   📦 已备份至 {backup.name}")

        # 复制文件
        shutil.copytree(source_folder, target_folder)

        # 统计文件
        file_count = len([f for f in target_folder.iterdir() if f.is_file()])
        print(f"✅ 完成！复制了 {file_count} 个文件到 {day_folder}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败")
        print(f"   错误: {e.stderr[:200] if e.stderr else '未知错误'}")
        return False
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False
    finally:
        # 清理临时文件
        if full_temp.exists():
            shutil.rmtree(full_temp)

def cleanup():
    """清理临时文件"""
    if TEMP_BASE_DIR.exists():
        shutil.rmtree(TEMP_BASE_DIR)

def interactive_mode():
    """交互式选择模式"""
    print("贝加尔铁路照片分批下载")
    print(f"可用日期：8月{START_DATE}日 - 8月{END_DATE}日")
    print("\n选项：")
    print("  1. 输入日期编号（如：03, 04, 05）")
    print("  2. 输入 'all' 下载所有")
    print("  3. 输入 'q' 退出")

    choice = input("\n请选择: ").strip().lower()

    if choice == 'q':
        return []
    elif choice == 'all':
        return list(range(START_DATE, END_DATE + 1))
    else:
        # 解析输入的日期
        dates = []
        for part in choice.split():
            try:
                date_num = int(part)
                if START_DATE <= date_num <= END_DATE:
                    dates.append(date_num)
                else:
                    print(f"⚠️  日期 {date_num} 超出范围，已跳过")
            except ValueError:
                print(f"⚠️  无效输入 '{part}'，已跳过")
        return dates

def main():
    print("=" * 60)
    print("贝加尔铁路照片分批下载工具")
    print("=" * 60)

    # 检查是否有自动确认标志
    auto_confirm = '-y' in sys.argv or '--yes' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ['-y', '--yes']]

    # 解析命令行参数
    if len(args) > 0:
        # 命令行模式
        dates = []
        if args[0].lower() == 'all':
            dates = list(range(START_DATE, END_DATE + 1))
        else:
            for arg in args:
                try:
                    date_num = int(arg)
                    if START_DATE <= date_num <= END_DATE:
                        dates.append(date_num)
                    else:
                        print(f"⚠️  日期 {date_num} 超出范围 ({START_DATE}-{END_DATE})")
                except ValueError:
                    print(f"⚠️  无效参数 '{arg}'")
    else:
        # 交互式模式
        dates = interactive_mode()

    if not dates:
        print("未选择任何日期，退出")
        return 0

    print(f"\n准备下载：{len(dates)} 个日期")
    for date_num in dates:
        print(f"  - 8月{date_num}日")

    if not auto_confirm:
        confirm = input("\n确认开始下载? (y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return 0
    else:
        print("\n自动确认模式，开始下载...")

    # 执行下载
    success_count = 0
    failed_dates = []

    for date_num in dates:
        try:
            if download_date(date_num):
                success_count += 1
            else:
                failed_dates.append(date_num)
        except KeyboardInterrupt:
            print(f"\n\n⚠️  用户中断")
            break

    # 清理
    cleanup()

    # 总结
    print(f"\n{'='*60}")
    print(f"下载完成")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count}/{len(dates)}")
    if failed_dates:
        print(f"❌ 失败: {', '.join([f'8月{d}日' for d in failed_dates])}")

    return 0 if not failed_dates else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n已中断")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        cleanup()
        sys.exit(1)
