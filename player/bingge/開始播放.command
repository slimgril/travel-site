#!/bin/bash
# 斌哥照片播放器 — 雙擊啟動
cd "$(dirname "$0")"
echo "啟動斌哥照片播放器…"
exec /usr/bin/env python3 server.py
