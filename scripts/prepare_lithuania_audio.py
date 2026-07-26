#!/usr/bin/env python3
"""
Download royalty-free Lithuanian music (Wikimedia Commons) and export a
15-second MP3 clip with fade-in start and fade-out ending.

Output (SSOT for the vinyl component):
  photos/bldh-trio/audio/lithuania_15s.mp3

Requires: ffmpeg on PATH (Homebrew: brew install ffmpeg)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / 'photos' / 'bldh-trio' / 'audio'
OUT_MP3 = OUT_DIR / 'lithuania_15s.mp3'
CACHE_DIR = ROOT / 'content' / 'bldh-trio' / 'audio' / '_source'
META_PATH = OUT_DIR / 'SOURCE.json'

# US Navy Band — instrumental Lithuanian national anthem (public domain / US gov)
# https://commons.wikimedia.org/wiki/File:Tautiška_giesme_instrumental.oga
COMMONS_TITLE = 'File:Tautiška giesme instrumental.oga'
COMMONS_PAGE = 'https://commons.wikimedia.org/wiki/File:Tauti%C5%A1ka_giesme_instrumental.oga'
FALLBACK_URL = (
    'https://upload.wikimedia.org/wikipedia/commons/a/ab/'
    'Tauti%C5%A1ka_giesme_instrumental.oga'
)

CLIP_START_SEC = 22.0   # skip fanfare; land on melodic body
CLIP_DURATION = 15.0
FADE_IN_SEC = 0.9       # short open — long fades feel like “no sound”
FADE_OUT_SEC = 2.5


def require_ffmpeg() -> str:
    path = shutil.which('ffmpeg')
    if not path:
        print(
            '✗ 找不到 ffmpeg。\n'
            '  macOS：brew install ffmpeg\n'
            '  安裝後重新執行：python3 scripts/prepare_lithuania_audio.py',
            file=sys.stderr,
        )
        sys.exit(1)
    return path


def resolve_commons_url(title: str) -> str:
    api = (
        'https://commons.wikimedia.org/w/api.php'
        f'?action=query&titles={urllib.request.quote(title)}'
        '&prop=imageinfo&iiprop=url&format=json'
    )
    req = urllib.request.Request(
        api,
        headers={'User-Agent': 'travel-site-lithuania-audio/1.0 (local prep)'},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        infos = page.get('imageinfo') or []
        if infos and infos[0].get('url'):
            return infos[0]['url']
    return FALLBACK_URL


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 100_000:
        print(f'  · reuse cache: {dest.name}')
        return
    print(f'  ↓ downloading…')
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'travel-site-lithuania-audio/1.0 (local prep)'},
    )
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, 'wb') as f:
        shutil.copyfileobj(resp, f)
    print(f'  ✓ saved {dest.name} ({dest.stat().st_size:,} bytes)')


def cut_with_fade(ffmpeg: str, src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    fade_out_at = max(0.0, CLIP_DURATION - FADE_OUT_SEC)
    # Fade in at start, fade out at end — clear begin / end feel
    af = (
        f'afade=t=in:st=0:d={FADE_IN_SEC:.2f},'
        f'afade=t=out:st={fade_out_at:.2f}:d={FADE_OUT_SEC:.2f}'
    )
    cmd = [
        ffmpeg, '-y',
        '-ss', f'{CLIP_START_SEC:.2f}',
        '-t', f'{CLIP_DURATION:.2f}',
        '-i', str(src),
        '-af', af,
        '-codec:a', 'libmp3lame',
        '-q:a', '4',
        str(dst),
    ]
    print('  ✂ cutting 15s + fade-in / fade-out…')
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        sys.exit(proc.returncode)
    print(f'  ✓ wrote {dst.relative_to(ROOT)} ({dst.stat().st_size:,} bytes)')


def write_meta(url: str) -> None:
    META_PATH.write_text(
        json.dumps(
            {
                'title': 'Tautiška giesmė (instrumental)',
                'commons': COMMONS_PAGE,
                'source_url': url,
                'performer': 'United States Navy Band',
                'note': (
                    '15s excerpt with 0.9s fade-in + 2.5s fade-out for Day 2 vinyl; '
                    'not the full anthem.'
                ),
                'clip': {
                    'start_sec': CLIP_START_SEC,
                    'duration_sec': CLIP_DURATION,
                    'fade_in_sec': FADE_IN_SEC,
                    'fade_out_sec': FADE_OUT_SEC,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + '\n',
        encoding='utf-8',
    )


def main() -> None:
    ffmpeg = require_ffmpeg()
    print('▶ prepare_lithuania_audio')
    url = resolve_commons_url(COMMONS_TITLE)
    print(f'  source: {url}')
    src = CACHE_DIR / 'tautoska-giesme-instrumental.oga'
    download(url, src)
    cut_with_fade(ffmpeg, src, OUT_MP3)
    # Convenience copy beside the demo page
    demo_copy = ROOT / 'content' / 'bldh-trio' / 'audio' / 'lithuania_15s.mp3'
    demo_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_MP3, demo_copy)
    write_meta(url)
    print(f'  ✓ demo copy → {demo_copy.relative_to(ROOT)}')
    print('✓ done')


if __name__ == '__main__':
    main()
