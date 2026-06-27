#!/bin/zsh
set -e
cd "/Users/johnsonwang/Desktop/旅遊/travel-site"

echo "▶ 重建網站..."
python3 scripts/build.py

echo "▶ 部署到 Surge..."
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
cd dist
SURGE_TOKEN="0cebc8930cbbc08556bad82b2110398b" surge . cluttered-breath.surge.sh

echo "✓ 完成：https://cluttered-breath.surge.sh"
