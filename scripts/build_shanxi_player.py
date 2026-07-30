#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Shanxi cloud photo player — ALL photos (journal + disk + extras).

Usage:
  python3 scripts/build_shanxi_player.py
  python3 scripts/build_shanxi_player.py --width 1600 --no-sips

Output: player/shanxi/ (index.html + data.js + media/)
Also syncs into dist-preview-deploy/player/shanxi and dist-surge-upload/player/shanxi
when those dirs exist.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "shanxi"
PHOTOS = ROOT / "photos" / "shanxi"
EXTRAS = PHOTOS / "player-extras"
OUT = ROOT / "player" / "shanxi"
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# Skip build/source clutter if ever nested under photos/shanxi
SKIP_DIRS = {"originals", "unassigned", "source", "cooked", "player-extras", "audio"}


def safe_name(name: str) -> str:
    keep = []
    for c in name:
        if c.isalnum() or c in "._-":
            keep.append(c)
        else:
            keep.append("_")
    out = "".join(keep).strip("._") or "photo"
    if not Path(out).suffix:
        out += ".jpg"
    return out[:140]


def parse_day_heading(line: str) -> dict:
    """# Day 2 ｜ 6月11日（四） ｜ route — title"""
    m = re.match(
        r"^#\s*Day\s*(\d+)\s*｜\s*([^｜]+)\s*｜\s*(.+)$",
        line.strip(),
    )
    if not m:
        return {"num": "", "date": "", "title": line.lstrip("# ").strip()}
    num, date, rest = m.group(1), m.group(2).strip(), m.group(3).strip()
    title = rest
    if "—" in rest:
        title = rest.split("—", 1)[-1].strip()
    elif "–" in rest:
        title = rest.split("–", 1)[-1].strip()
    return {"num": num, "date": date, "title": title or rest}


def collect_day_albums() -> tuple[list[dict], set[str]]:
    albums = []
    used: set[str] = set()
    for md in sorted(CONTENT.glob("day*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        head = next((l for l in lines if l.startswith("#")), md.stem)
        meta = parse_day_heading(head)
        refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
        photos = []
        for ref in refs:
            name = Path(ref.strip()).name
            src = PHOTOS / name
            if not src.is_file():
                continue
            if name in used:
                continue
            used.add(name)
            photos.append({"name": name, "src": src, "caption": Path(name).stem})
        day_id = f"day{int(meta['num']):02d}" if meta["num"].isdigit() else md.stem
        label = f"Day {meta['num']}" if meta["num"] else md.stem
        albums.append(
            {
                "id": day_id,
                "label": label,
                "title": meta["title"],
                "date": meta["date"],
                "photos": photos,
            }
        )
    return albums, used


def collect_loose(used: set[str]) -> list[dict]:
    loose = []
    for p in sorted(PHOTOS.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMG_EXT:
            continue
        if p.name.startswith("."):
            continue
        if p.name in used:
            continue
        loose.append({"name": p.name, "src": p, "caption": p.stem})
        used.add(p.name)
    return loose


def collect_extras(used: set[str]) -> list[dict]:
    extras = []
    if not EXTRAS.is_dir():
        return extras
    for p in sorted(EXTRAS.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_file() or p.suffix.lower() not in IMG_EXT:
            continue
        if p.name.startswith("."):
            continue
        key = p.name
        if key in used:
            continue
        used.add(key)
        extras.append({"name": p.name, "src": p, "caption": p.stem})
    return extras


def sips_copy(src: Path, dest: Path, width: int, quality: int, use_sips: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not use_sips:
        shutil.copyfile(src, dest)
        return
    # Copy first then resample in place (avoids black images from bad pipes)
    shutil.copyfile(src, dest)
    subprocess.run(
        [
            "sips",
            "--resampleHeightWidthMax",
            str(width),
            "--setProperty",
            "formatOptions",
            str(quality),
            str(dest),
        ],
        capture_output=True,
        check=False,
    )


def write_html(out: Path, total: int) -> None:
    html = PLAYER_HTML.replace("{{TOTAL}}", str(total))
    (out / "index.html").write_text(html, encoding="utf-8")


def sync_to_dist(out: Path) -> None:
    for name in ("dist-preview-deploy", "dist-surge-upload", "dist-prototype", "dist"):
        dist = ROOT / name
        if not dist.is_dir():
            continue
        target = dist / "player" / "shanxi"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(out, target)
        print(f"  synced → {target.relative_to(ROOT)}/")


def build(width: int, quality: int, use_sips: bool) -> None:
    """Hybrid cloud pack: journal/loose → site photos/; extras → player/media/."""
    albums, used = collect_day_albums()
    loose = collect_loose(used)
    extras = collect_extras(used)

    if loose:
        albums.append(
            {
                "id": "loose",
                "label": "未入冊",
                "title": "磁碟有、札記未引用",
                "date": "",
                "photos": loose,
            }
        )
    if extras:
        albums.append(
            {
                "id": "extras",
                "label": "未入選",
                "title": "斌哥補傳・未入站札記",
                "date": "",
                "photos": extras,
            }
        )

    if OUT.exists():
        shutil.rmtree(OUT)
    media = OUT / "media"
    media.mkdir(parents=True)

    days_bundle = {}
    day_meta = []
    all_photos = []
    total = 0
    site_refs: list[str] = []

    for album in albums:
        photos_out = []
        print(f"[{album['id']}] {len(album['photos'])} …", flush=True)
        embed = album["id"] == "extras"
        dest_dir = None
        if embed:
            dest_dir = media / album["id"]
            dest_dir.mkdir(parents=True, exist_ok=True)
        for i, ph in enumerate(album["photos"], 1):
            if embed:
                dest_name = safe_name(ph["name"])
                dest = dest_dir / dest_name
                if dest.exists():
                    dest = dest_dir / f"{Path(dest_name).stem}_{i}{Path(dest_name).suffix}"
                sips_copy(ph["src"], dest, width, quality, use_sips)
                url = f"media/{album['id']}/{dest.name}"
            else:
                url = f"../../photos/shanxi/{ph['name']}"
                site_refs.append(f"shanxi/{ph['name']}")
            item = {
                "name": ph["name"],
                "url": url,
                "caption": ph.get("caption") or Path(ph["name"]).stem,
                "day": album["id"],
                "day_label": album["label"],
            }
            photos_out.append(item)
            all_photos.append(item)
            total += 1
        days_bundle[album["id"]] = {
            "id": album["id"],
            "label": album["label"],
            "title": album["title"],
            "date": album["date"],
            "count": len(photos_out),
            "photos": photos_out,
        }
        if photos_out:
            day_meta.append(
                {
                    "id": album["id"],
                    "label": album["label"],
                    "title": album["title"],
                    "count": len(photos_out),
                }
            )

    payload = {
        "meta": {
            "title": "丫斌哥 · 山西漫遊",
            "subtitle": "照片播放器 · 全部照片",
            "trip": "shanxi",
            "slide_ms": 5000,
            "total": total,
            "back_href": "../../trips/shanxi.html",
            "site_photo_refs": sorted(set(site_refs)),
        },
        "days": day_meta,
        "albums": days_bundle,
        "all": all_photos,
    }
    (OUT / "data.js").write_text(
        "window.SHANXI_PLAYER = "
        + json.dumps(payload, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    write_html(OUT, total)
    (OUT / "photo-refs.txt").write_text(
        "\n".join(sorted(set(site_refs))) + "\n", encoding="utf-8"
    )
    print(
        f"DONE total={total} (extras={len(extras)}, site_refs={len(set(site_refs))}) → {OUT.relative_to(ROOT)}/",
        flush=True,
    )
    sync_to_dist(OUT)


PLAYER_HTML = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>丫斌哥 · 山西漫遊 — 照片播放器</title>
<meta name="description" content="山西旅程全部照片播放器（入站＋未入選）">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@300;400;500&display=swap" rel="stylesheet">
<script src="data.js"></script>
<style>
  :root {
    --ink: #0d2b1f;
    --moss: #1b4332;
    --gold: #d4a843;
    --gold-soft: #e8c97a;
    --fog: rgba(248, 244, 234, 0.92);
    --paper: #f3efe4;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    font-family: "Noto Sans TC", "PingFang TC", sans-serif;
    background:
      radial-gradient(ellipse at 20% 10%, rgba(212,168,67,.18), transparent 45%),
      radial-gradient(ellipse at 80% 90%, rgba(45,106,79,.35), transparent 40%),
      linear-gradient(160deg, #0a1f16 0%, var(--ink) 40%, #163528 100%);
    color: var(--paper);
    overflow: hidden;
  }
  #home, #stage { height: 100vh; position: relative; }
  #home.hidden, #stage.hidden { display: none; }

  #home {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 6vh 5vw 8vh; text-align: center; gap: 18px;
  }
  .eyebrow {
    letter-spacing: .28em; font-size: 12px; color: var(--gold-soft); opacity: .85;
    text-transform: uppercase;
  }
  h1 {
    font-family: "Noto Serif TC", serif; font-weight: 700;
    font-size: clamp(28px, 5vw, 48px); line-height: 1.25;
  }
  .sub { opacity: .7; font-size: 15px; letter-spacing: .04em; }
  .count { color: var(--gold); font-size: 14px; letter-spacing: .08em; }

  .actions { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 10px; }
  button, .link-btn {
    appearance: none; border: 1px solid rgba(212,168,67,.45);
    background: rgba(212,168,67,.12); color: var(--paper);
    font: inherit; cursor: pointer; border-radius: 999px;
    padding: 12px 22px; letter-spacing: .06em; transition: .2s ease;
    text-decoration: none; display: inline-flex; align-items: center;
  }
  button.primary { background: var(--gold); color: var(--ink); border-color: var(--gold); font-weight: 600; }
  button:hover, .link-btn:hover { transform: translateY(-1px); border-color: var(--gold); }
  button.primary:hover { filter: brightness(1.05); }

  .days {
    max-width: 820px; width: 100%; margin-top: 22px;
    display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
  }
  .day-chip {
    border: 1px solid rgba(255,255,255,.18); background: rgba(0,0,0,.18);
    padding: 8px 12px; border-radius: 10px; font-size: 13px; cursor: pointer;
    min-width: 92px; text-align: left;
  }
  .day-chip strong { display: block; color: var(--gold-soft); font-size: 12px; }
  .day-chip span { opacity: .75; font-size: 11px; }
  .day-chip:hover { border-color: var(--gold); }

  #stage { background: #050b08; }
  #stage .frame {
    position: absolute; inset: 0;
    display: grid; place-items: center;
  }
  #stage img {
    max-width: 100%; max-height: 100%;
    object-fit: contain;
    opacity: 0; transition: opacity .45s ease;
    box-shadow: 0 20px 60px rgba(0,0,0,.45);
  }
  #stage img.show { opacity: 1; }

  .hud {
    position: absolute; left: 0; right: 0; bottom: 0;
    padding: 18px 22px 22px;
    background: linear-gradient(transparent, rgba(0,0,0,.72));
    display: flex; flex-direction: column; gap: 10px;
  }
  .caption {
    font-family: "Noto Serif TC", serif; font-size: clamp(16px, 2.4vw, 22px);
  }
  .meta-row { display: flex; justify-content: space-between; gap: 12px; font-size: 13px; opacity: .8; }
  .bar { height: 3px; background: rgba(255,255,255,.15); border-radius: 2px; overflow: hidden; }
  .bar > i { display: block; height: 100%; width: 0; background: var(--gold); transition: width .25s linear; }

  .topbar {
    position: absolute; top: 0; left: 0; right: 0;
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 16px; gap: 10px;
    background: linear-gradient(rgba(0,0,0,.55), transparent);
  }
  .topbar .group { display: flex; gap: 8px; flex-wrap: wrap; }
  .ghost {
    border: 1px solid rgba(255,255,255,.25); background: rgba(0,0,0,.25);
    color: #fff; border-radius: 999px; padding: 8px 14px; font-size: 13px; cursor: pointer;
  }
  .nav-hit {
    position: absolute; top: 18%; bottom: 22%; width: 22%;
    background: transparent; border: 0; cursor: pointer;
  }
  .nav-hit.prev { left: 0; }
  .nav-hit.next { right: 0; }

  @media (max-width: 640px) {
    .day-chip { min-width: calc(50% - 8px); }
    .nav-hit { width: 18%; }
  }
</style>
</head>
<body>
  <section id="home">
    <div class="eyebrow">World Journey #001</div>
    <h1 id="title">丫斌哥 · 山西漫遊</h1>
    <p class="sub" id="subtitle">照片播放器 · 全部照片</p>
    <p class="count" id="totalLabel">共 {{TOTAL}} 張</p>
    <div class="actions">
      <button class="primary" id="btnAll" type="button">播放全部</button>
      <a class="link-btn" id="backLink" href="../../trips/shanxi.html">← 回山西旅程</a>
    </div>
    <div class="days" id="dayList" aria-label="依天播放"></div>
  </section>

  <section id="stage" class="hidden" aria-live="polite">
    <div class="topbar">
      <div class="group">
        <button class="ghost" id="btnHome" type="button">結束</button>
        <button class="ghost" id="btnToggle" type="button">暫停</button>
      </div>
      <div class="group">
        <button class="ghost" id="btnPrev" type="button">上一張</button>
        <button class="ghost" id="btnNext" type="button">下一張</button>
      </div>
    </div>
    <div class="frame"><img id="slide" alt=""></div>
    <button class="nav-hit prev" id="hitPrev" type="button" aria-label="上一張"></button>
    <button class="nav-hit next" id="hitNext" type="button" aria-label="下一張"></button>
    <div class="hud">
      <div class="bar"><i id="progress"></i></div>
      <div class="caption" id="caption"></div>
      <div class="meta-row">
        <span id="dayLabel"></span>
        <span id="counter"></span>
      </div>
    </div>
  </section>

<script>
(function () {
  var data = window.SHANXI_PLAYER;
  if (!data) {
    document.getElementById('subtitle').textContent = '缺少 data.js，請先執行 build_shanxi_player.py';
    return;
  }
  var meta = data.meta || {};
  var albums = data.albums || {};
  var all = data.all || [];
  document.getElementById('title').textContent = meta.title || '山西漫遊';
  document.getElementById('subtitle').textContent = meta.subtitle || '';
  document.getElementById('totalLabel').textContent = '共 ' + (meta.total || all.length) + ' 張';
  if (meta.back_href) document.getElementById('backLink').setAttribute('href', meta.back_href);

  var list = document.getElementById('dayList');
  (data.days || []).forEach(function (d) {
    if (!d.count) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'day-chip';
    b.innerHTML = '<strong>' + d.label + '</strong><span>' + (d.title || '') + ' · ' + d.count + ' 張</span>';
    b.addEventListener('click', function () { startAlbum(d.id); });
    list.appendChild(b);
  });

  var home = document.getElementById('home');
  var stage = document.getElementById('stage');
  var img = document.getElementById('slide');
  var caption = document.getElementById('caption');
  var dayLabel = document.getElementById('dayLabel');
  var counter = document.getElementById('counter');
  var progress = document.getElementById('progress');
  var btnToggle = document.getElementById('btnToggle');

  var queue = [];
  var index = 0;
  var playing = false;
  var timer = null;
  var slideMs = meta.slide_ms || 5000;
  var preload = [];

  function clearTimer() {
    if (timer) { clearTimeout(timer); timer = null; }
  }

  function showHome() {
    clearTimer();
    playing = false;
    home.classList.remove('hidden');
    stage.classList.add('hidden');
    img.removeAttribute('src');
    img.classList.remove('show');
  }

  function startAlbum(id) {
    var album = albums[id];
    if (!album || !album.photos || !album.photos.length) return;
    queue = album.photos.slice();
    index = 0;
    openStage();
  }

  function startAll() {
    if (!all.length) return;
    queue = all.slice();
    index = 0;
    openStage();
  }

  function openStage() {
    home.classList.add('hidden');
    stage.classList.remove('hidden');
    playing = true;
    btnToggle.textContent = '暫停';
    render();
  }

  function preloadAround() {
    preload.forEach(function (x) { try { x.src = ''; } catch (e) {} });
    preload = [];
    for (var i = 1; i <= 3; i++) {
      var n = index + i;
      if (n >= queue.length) break;
      var im = new Image();
      im.src = queue[n].url;
      preload.push(im);
    }
  }

  function render() {
    clearTimer();
    if (!queue.length) return;
    var item = queue[index];
    img.classList.remove('show');
    var nextSrc = item.url;
    var done = function () {
      img.classList.add('show');
      caption.textContent = item.caption || '';
      dayLabel.textContent = item.day_label || item.day || '';
      counter.textContent = (index + 1) + ' / ' + queue.length;
      progress.style.width = ((index + 1) / queue.length * 100).toFixed(1) + '%';
      preloadAround();
      if (playing) {
        timer = setTimeout(function () { next(true); }, slideMs);
      }
    };
    if (img.src && img.src.indexOf(nextSrc) !== -1 && img.complete) {
      done();
    } else {
      img.onload = done;
      img.onerror = done;
      img.src = nextSrc;
      img.alt = item.caption || '';
    }
  }

  function next(auto) {
    if (index >= queue.length - 1) {
      if (auto) { showHome(); return; }
      return;
    }
    index += 1;
    render();
  }

  function prev() {
    if (index <= 0) return;
    index -= 1;
    render();
  }

  function toggle() {
    playing = !playing;
    btnToggle.textContent = playing ? '暫停' : '繼續';
    if (playing) {
      timer = setTimeout(function () { next(true); }, slideMs);
    } else {
      clearTimer();
    }
  }

  document.getElementById('btnAll').addEventListener('click', startAll);
  document.getElementById('btnHome').addEventListener('click', showHome);
  document.getElementById('btnToggle').addEventListener('click', toggle);
  document.getElementById('btnPrev').addEventListener('click', prev);
  document.getElementById('btnNext').addEventListener('click', function () { next(false); });
  document.getElementById('hitPrev').addEventListener('click', prev);
  document.getElementById('hitNext').addEventListener('click', function () { next(false); });

  document.addEventListener('keydown', function (e) {
    if (stage.classList.contains('hidden')) return;
    if (e.key === 'Escape') showHome();
    else if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); next(false); }
    else if (e.key === 'ArrowLeft') prev();
    else if (e.key === 'p' || e.key === 'P') toggle();
  });
})();
</script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--no-sips", action="store_true")
    args = ap.parse_args()
    width = max(800, min(args.width, 2400))
    quality = max(60, min(args.quality, 95))
    build(width, quality, use_sips=not args.no_sips)


if __name__ == "__main__":
    main()
