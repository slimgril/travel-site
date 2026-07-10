#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
#  Prototype Build — 用 photos/<slug>/cooked/matched/ 的候選圖片疊出一份
#  獨立於生產環境的預覽站（dist-prototype/）。
#
#  只做一件事：正常跑一次 build.py 的 main()，輸出目錄換成 dist-prototype/，
#  複製完 photos/ 之後，把每個 slug 的 cooked/matched/* 蓋到
#  dist-prototype/photos/<slug>/reference/ 上——只動這份輸出複本。
#
#  不動的東西（保證）：
#   - dist/（生產環境輸出）完全不被讀取、不被寫入。
#   - photos/<slug>/reference/（磁碟上的正式核准圖）完全不被寫入。
#   - content/*.md、landmarks.yaml 完全不變動。
#
#  用法：python3 scripts/build_prototype.py
# ============================================================================

import os
import re
import shutil

import build

D_DIST_PROTOTYPE = os.path.join(build.ROOT, 'dist-prototype')

# 景點資料的原型覆寫（只在記憶體套用，不寫回 content/<slug>/landmarks.yaml）。
# 目前不需要覆寫；照片與驗證狀態都應回到 landmarks.yaml 管理。
LANDMARKS_PATCH = {}


def overlay_cooked_matches(dist_dir, photos_root):
    """把每個 slug 的 cooked/matched/* 覆蓋到 dist_dir/photos/<slug>/reference/。
    只在 dist_dir 這份複本上動刀，photos_root 底下的真正 reference/ 不受影響。"""
    if not os.path.isdir(photos_root):
        return
    for slug in sorted(os.listdir(photos_root)):
        matched_dir = os.path.join(photos_root, slug, 'cooked', 'matched')
        if not os.path.isdir(matched_dir):
            continue
        dst_reference = os.path.join(dist_dir, 'photos', slug, 'reference')
        os.makedirs(dst_reference, exist_ok=True)
        overridden = 0
        for name in sorted(os.listdir(matched_dir)):
            if name.startswith('.') or re.search(r' \d+\.[^.]+$', name):
                continue
            src = os.path.join(matched_dir, name)
            if not os.path.isfile(src):
                continue
            if os.path.getsize(src) == 0:
                continue
            shutil.copy2(src, os.path.join(dst_reference, name))
            overridden += 1
        if overridden:
            print('  ↻ prototype overlay：%s 換上 %d 張候選圖（來自 cooked/matched/）'
                  % (slug, overridden))


def main():
    print('─' * 50)
    print('▶ PROTOTYPE BUILD — 不影響生產環境 dist/ 與 photos/*/reference/')
    print('─' * 50)
    build.main(dist_dir=D_DIST_PROTOTYPE, overlay=overlay_cooked_matches,
               label='dist-prototype/（僅供審核，非生產環境）',
               landmarks_patch=LANDMARKS_PATCH)


if __name__ == '__main__':
    main()
