#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baikal Rail incremental photo sync: Google Drive → travel-site.

Additive orchestrator — does NOT modify build.py or build_prototype.py.
Run daily: python3 scripts/sync_baikal_photos.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import build  # noqa: E402

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic'}
DAY_FOLDER_RE = re.compile(r'Day\s+(\d{1,2})\s*-\s*(.+)', re.IGNORECASE)
DRIVE_ID_RE = re.compile(r'[/?&]id=([a-zA-Z0-9_-]+)')

# Folder suffix (after "Day XX - ") → English slug for dest filename
FOLDER_SLUGS: dict[str, str] = {
    '蒙古國民族舞蹈與馬頭琴表演': 'mongolia-folk-dance-morin-khuur',
    '烏蘭烏德市中心': 'ulan-ude-city-center',
    '新西伯利亞地方誌博物館': 'novosibirsk-local-history-museum',
    '新西伯利亞火車博物館': 'novosibirsk-railway-museum',
    '成吉思汗巨大不鏽鋼塑像': 'genghis-khan-statue',
    '烏蘭巴托市景': 'ulaanbaatar-city',
    '特勒吉國家公園烏龜石': 'turtle-rock',
    '草原騎馬': 'mongolia-horseback-riding',
    '哈爾和林博物館': 'karakorum-museum',
    '哈爾和林古都遺跡': 'kharkhorin-ancient-city',
    '額爾登尼召寺': 'erdene-zuu-monastery',
    '柏格多汗冬宮': 'bogd-khan-winter-palace',
    '國立蒙古歷史博物館': 'national-museum-mongolia',
    '西伯利亞大鐵路蒙古段列車': 'trans-mongolian-railway-train',
    '伊爾庫次克市景明珠': 'irkutsk-city',
    '塔利茨木造建築博物館': 'taltsy-wooden-museum',
    '李斯特維揚卡湖畔小鎮': 'listvyanka-lakeside-town',
    '基洛夫廣場': 'kirov-square-irkutsk',
    '斯帕斯卡亞教堂': 'spasskaya-church',
    '貝加爾湖生態博物館': 'baikal-ecological-museum',
    '奧利洪島壯闊湖岸': 'olkhon-island-shore',
    '奧利洪島薩滿岩': 'lake-baikal-shaman-rock',
    '布里亞特傳統村落': 'buryat-traditional-village',
    '烏斯季奧爾登斯基博物館': 'ust-orda-museum',
    '伊爾庫次克火車站': 'irkutsk-railway-station',
    '湖島村落與沙灘怪松林': 'olkhon-village-beach-pines',
    '克拉斯諾亞爾斯克葉尼塞河鐵路橋': 'krasnoyarsk-railway-bridge',
    '濟馬 Zima 小鎮火車站': 'zima-railway-station',
    '馬林斯克 Mariinsk 木造歷史建築': 'mariinsk-wooden-architecture',
    '新西伯利亞國立歌劇院': 'novosibirsk-opera-theatre',
    '新西伯利亞極地動物園': 'novosibirsk-zoo',
    '聖亞歷山大涅夫斯基教堂': 'alexander-nevsky-cathedral',
    '巴拉賓斯克 Barabinsk 補給站': 'barabinsk-station',
    '烏拉爾重機械廠歷史照片': 'uralmash-heavy-machinery',
    '秋明 Tyumen 地理分界門戶': 'tyumen-riverfront',
    '葉卡捷琳堡歐亞分界紀念碑': 'europe-asia-border',
    '葉卡捷琳堡滴血教堂': 'church-on-blood-yekaterinburg',
    '鄂木斯克 Omsk 額爾齊斯河畔': 'omsk-irtysh-river',
    '聖彼得堡冬宮': 'winter-palace-hermitage',
    '聖彼得堡北方威尼斯運河': 'saint-petersburg-canals',
    '彼得夏宮大噴泉': 'peterhof-grand-cascade',
    '科特林島歷史風光': 'kotlin-island-kronstadt',
    '芬蘭灣海岸線風景': 'gulf-of-finland-coast',
    '彼得夏宮花園全景': 'peterhof-gardens',
    '聖彼得堡浴血復活大教堂': 'savior-on-spilled-blood',
    '聖彼得堡涅瓦大街街景': 'nevsky-prospect',
    '聖彼得堡聖以薩大教堂': 'saint-isaac-cathedral',
    '葉卡捷琳娜公園湖泊': 'catherine-park-lake',
    '葉卡捷琳娜宮': 'catherine-palace',
    '宮殿廣場': 'palace-square',
    '彼得保羅要塞': 'peter-and-paul-fortress',
    '莫斯科市天際線大景': 'moscow-skyline',
    '莫斯科克里姆林宮紅牆': 'kremlin-red-wall',
    '莫斯科地下宮殿地鐵站': 'moscow-metro-palace-station',
    '莫斯科紅場聖瓦西里大教堂': 'saint-basil-cathedral-front',
    '卡洛明斯科婭沙皇避暑莊園': 'kolomenskoye-estate',
    '伊茲麥洛夫跳蚤市集城堡': 'izmailovo-market-kremlin',
    '伊茲麥洛夫大型自然公園': 'izmailovo-park',
}


class SyncReport:
    def __init__(self):
        self.drive_access = 'unknown'
        self.drive_method = None
        self.drive_listed = 0
        self.drive_baikal_candidates = 0
        self.new_imported = 0
        self.skipped_existing = 0
        self.review_required: list[dict] = []
        self.updated_days: list[int] = []
        self.duplicates_skipped: list[str] = []
        self.errors: list[str] = []
        self.build_status = 'not_run'
        self.missing_images = 0
        self.broken_images = 0
        self.broken_links = 0
        self.deploy_status = 'not_run'
        self.deploy_url = None
        self.checks: dict[str, str] = {}


def load_config() -> dict:
    path = ROOT / 'content/baikal-rail/source/photo-sync-config.json'
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def load_sync_state(path: Path) -> dict:
    if path.exists():
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    return {
        'version': 1,
        'source': {'type': 'google_drive', 'drive_url': None, 'folder_id': None},
        'last_sync': None,
        'summary': {},
        'synced': [],
        'source_inventory': [],
        'review_required': [],
    }


def save_sync_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
        fh.write('\n')


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def extract_drive_id(url: str) -> str | None:
    m = DRIVE_ID_RE.search(url)
    return m.group(1) if m else None


def try_gdown_list(folder_url: str, retries: int = 3) -> tuple[list[dict] | None, str | None]:
    """Return list of {url, path, drive_file_id} or None on failure."""
    for attempt in range(1, retries + 1):
        try:
            proc = subprocess.run(
                ['gdown', '--folder', '--json', folder_url],
                capture_output=True, text=True, timeout=120,
            )
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or '').strip()
                if attempt < retries:
                    continue
                return None, err
            stdout = proc.stdout.strip()
            if not stdout:
                return None, proc.stderr.strip() or 'empty gdown response'
            items = json.loads(stdout)
            result = []
            for item in items:
                fid = extract_drive_id(item.get('url', ''))
                result.append({
                    'url': item['url'],
                    'path': item['path'],
                    'drive_file_id': fid,
                })
            return result, None
        except FileNotFoundError:
            return None, 'gdown not installed (pip3 install gdown)'
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            if attempt < retries:
                continue
            return None, str(exc)
    return None, 'gdown retries exhausted'


def try_drive_api(credentials_path: str | None) -> tuple[list[dict] | None, str | None]:
    if not credentials_path:
        return None, 'no credentials configured'
    cred = ROOT / credentials_path
    if not cred.exists():
        return None, 'credentials file not found: %s' % credentials_path
    return None, 'google-api-python-client not installed; use gdown or pip install google-api-python-client google-auth'


def try_rclone(remote: str | None, folder_id: str) -> tuple[list[dict] | None, str | None]:
    if not remote:
        return None, 'rclone_remote not configured'
    try:
        proc = subprocess.run(
            ['rclone', 'lsjson', '%s' % remote, '--drive-root-folder-id', folder_id],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            return None, proc.stderr.strip() or 'rclone failed'
        items = json.loads(proc.stdout)
        result = []
        for item in items:
            if item.get('IsDir'):
                continue
            result.append({
                'url': None,
                'path': item['Path'],
                'drive_file_id': item.get('ID'),
                'size': item.get('Size'),
            })
        return result, None
    except FileNotFoundError:
        return None, 'rclone not installed'
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        return None, str(exc)


def access_drive(config: dict, report: SyncReport) -> list[dict] | None:
    drive = config['drive']
    folder_url = drive['folder_url']
    folder_id = drive['folder_id']
    methods = config.get('access_methods', ['gdown', 'google_drive_api', 'rclone'])
    errors = []

    for method in methods:
        if method == 'gdown':
            items, err = try_gdown_list(folder_url)
            if items is not None:
                report.drive_access = 'ok'
                report.drive_method = 'gdown'
                return items
            errors.append('gdown: %s' % (err or 'unknown'))
        elif method == 'google_drive_api':
            items, err = try_drive_api(config.get('credentials'))
            if items is not None:
                report.drive_access = 'ok'
                report.drive_method = 'google_drive_api'
                return items
            errors.append('api: %s' % (err or 'unknown'))
        elif method == 'rclone':
            items, err = try_rclone(config.get('rclone_remote'), folder_id)
            if items is not None:
                report.drive_access = 'ok'
                report.drive_method = 'rclone'
                return items
            errors.append('rclone: %s' % (err or 'unknown'))

    report.drive_access = 'blocked'
    report.errors.extend(errors)
    return None


def known_hashes(state: dict) -> set[str]:
    hashes = set()
    for entry in state.get('synced', []):
        if entry.get('hash'):
            hashes.add(entry['hash'])
    for entry in state.get('source_inventory', []):
        if entry.get('hash'):
            hashes.add(entry['hash'])
    return hashes


def known_drive_ids(state: dict) -> set[str]:
    ids = set()
    for entry in state.get('synced', []):
        if entry.get('drive_file_id'):
            ids.add(entry['drive_file_id'])
    for entry in state.get('source_inventory', []):
        if entry.get('drive_file_id'):
            ids.add(entry['drive_file_id'])
    for entry in state.get('review_required', []):
        if entry.get('drive_file_id'):
            ids.add(entry['drive_file_id'])
    return ids


def path_has_day_folder(path: str) -> bool:
    for part in path.replace('\\', '/').split('/'):
        if DAY_FOLDER_RE.match(part.strip()):
            return True
    return False


def parse_day_folder_from_path(path: str) -> tuple[int | None, str | None]:
    for part in path.replace('\\', '/').split('/'):
        m = DAY_FOLDER_RE.match(part.strip())
        if m:
            return int(m.group(1)), m.group(2).strip()
    return None, None


def load_day_landmarks(day: int, content_root: Path) -> list[dict]:
    md_path = content_root / ('day%02d.md' % day)
    if not md_path.exists():
        return []
    landmarks = []
    with open(md_path, encoding='utf-8') as fh:
        for line in fh:
            m = re.match(r'^###\s+(?:!\[[^\]]*\]\([^)]+\)\s+)?(.+)$', line.strip())
            if m:
                name = m.group(1).strip()
                has_image = line.strip().startswith('### ![')
                landmarks.append({'name': name, 'has_image': has_image, 'line': line})
    return landmarks


def match_landmark(folder_landmark: str, day: int, content_root: Path) -> dict | None:
    landmarks = load_day_landmarks(day, content_root)
    norm_folder = re.sub(r'\s+', '', folder_landmark)
    for lm in landmarks:
        norm_name = re.sub(r'\s+', '', lm['name'])
        if norm_folder in norm_name or norm_name in norm_folder:
            return lm
        # partial keyword match (at least 4 chars overlap)
        for chunk in re.split(r'[與及、\s]+', folder_landmark):
            chunk = chunk.strip()
            if len(chunk) >= 3 and chunk in lm['name']:
                return lm
    return None


def dest_slug(folder_landmark: str, source_name: str) -> str:
    if folder_landmark in FOLDER_SLUGS:
        base = FOLDER_SLUGS[folder_landmark]
    else:
        base = re.sub(r'[^a-zA-Z0-9]+', '-', folder_landmark).strip('-').lower()
        if not base:
            base = Path(source_name).stem.lower()
    ext = Path(source_name).suffix.lower()
    if ext not in IMAGE_EXTS:
        ext = '.jpg'
    if ext == '.jpeg':
        ext = '.jpg'
    return '%s-downloaded%s' % (base, ext)


def download_gdown_file(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ['gdown', url, '-O', str(dest), '--fuzzy'],
        capture_output=True, text=True, timeout=180,
    )
    return proc.returncode == 0 and dest.exists() and dest.stat().st_size > 0


def update_day_md(day: int, landmark_name: str, rel_path: str, content_root: Path) -> bool:
    """Insert image ref only if landmark heading has no existing image."""
    md_path = content_root / ('day%02d.md' % day)
    if not md_path.exists():
        return False
    lines = md_path.read_text(encoding='utf-8').splitlines(keepends=True)
    changed = False
    day_prefix = 'day%02d/' % day
    filename = rel_path.split('/')[-1]
    for i, line in enumerate(lines):
        if line.strip().startswith('### !['):
            continue
        m = re.match(r'^###\s+(.+)$', line.strip())
        if not m:
            continue
        heading = m.group(1).strip()
        norm_h = re.sub(r'\s+', '', heading)
        norm_l = re.sub(r'\s+', '', landmark_name)
        if norm_l in norm_h or norm_h in norm_l:
            lines[i] = '### ![%s](%s%s) %s\n' % (heading, day_prefix, filename, heading)
            changed = True
            break
    if changed:
        md_path.write_text(''.join(lines), encoding='utf-8')
    return changed


def process_drive_files(
    drive_items: list[dict],
    config: dict,
    state: dict,
    report: SyncReport,
    dry_run: bool = False,
) -> None:
    paths = config['paths']
    content_root = ROOT / paths['content_root']
    photos_root = ROOT / paths['photos_root']
    originals_root = ROOT / paths['source_originals']
    hashes = known_hashes(state)
    drive_ids = known_drive_ids(state)

    report.drive_listed = len(drive_items)

    for item in drive_items:
        path = item['path']
        fid = item.get('drive_file_id')
        ext = Path(path).suffix.lower()
        if ext not in IMAGE_EXTS:
            continue

        if fid and fid in drive_ids:
            report.skipped_existing += 1
            continue

        if not path_has_day_folder(path):
            report.review_required.append({
                'drive_path': path,
                'drive_file_id': fid,
                'reason': 'no_day_folder_match',
                'note': 'Drive path lacks "Day XX - landmark" folder structure',
            })
            continue

        day, folder_landmark = parse_day_folder_from_path(path)
        if day is None or not folder_landmark:
            report.review_required.append({
                'drive_path': path,
                'drive_file_id': fid,
                'reason': 'unparseable_day_folder',
            })
            continue

        report.drive_baikal_candidates += 1
        lm = match_landmark(folder_landmark, day, content_root)
        if lm is None:
            report.review_required.append({
                'drive_path': path,
                'drive_file_id': fid,
                'day': day,
                'folder_landmark': folder_landmark,
                'reason': 'no_landmark_match_in_day_md',
            })
            continue

        filename = dest_slug(folder_landmark, path)
        day_dir = photos_root / ('day%02d' % day)
        dest_rel = 'photos/baikal-rail/day%02d/%s' % (day, filename)
        dest_abs = day_dir / filename

        if dest_abs.exists():
            report.duplicates_skipped.append(dest_rel)
            report.skipped_existing += 1
            continue

        if dry_run:
            print('  [dry-run] would import: %s → %s' % (path, dest_rel))
            report.new_imported += 1
            continue

        # Download to originals
        orig_rel = '%s/%s' % (path.replace('\\', '/'), Path(path).name)
        orig_abs = originals_root / path.replace('\\', '/')
        orig_abs.parent.mkdir(parents=True, exist_ok=True)

        url = item.get('url')
        if not url:
            report.review_required.append({
                'drive_path': path,
                'drive_file_id': fid,
                'reason': 'no_download_url',
            })
            continue

        if orig_abs.exists():
            tmp_path = orig_abs
        else:
            if not download_gdown_file(url, orig_abs):
                report.errors.append('download failed: %s' % path)
                continue
            tmp_path = orig_abs

        if not build.is_valid_image_file(str(tmp_path)):
            report.review_required.append({
                'drive_path': path,
                'drive_file_id': fid,
                'reason': 'invalid_image_file',
            })
            tmp_path.unlink(missing_ok=True)
            continue

        file_hash = sha256_file(tmp_path)
        if file_hash in hashes:
            report.duplicates_skipped.append('%s (hash match)' % path)
            report.skipped_existing += 1
            continue

        day_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp_path, dest_abs)

        if lm and not lm['has_image']:
            if update_day_md(day, lm['name'], filename, content_root):
                if day not in report.updated_days:
                    report.updated_days.append(day)

        now = datetime.now(timezone.utc).isoformat()
        state['synced'].append({
            'day': day,
            'dest': dest_rel,
            'filename': filename,
            'hash': file_hash,
            'size': dest_abs.stat().st_size,
            'source': 'drive:%s' % (fid or path),
            'source_folder': 'Day %02d - %s' % (day, folder_landmark),
            'drive_file_id': fid,
            'drive_path': path,
            'synced_at': now,
            'status': 'imported',
        })
        hashes.add(file_hash)
        if fid:
            drive_ids.add(fid)
        report.new_imported += 1


def run_build() -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'scripts/build_prototype.py')],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode == 0


def run_checks(report: SyncReport) -> bool:
    dist = ROOT / 'dist-prototype'
    all_pass = True

    # Missing images
    missing = 0
    broken = 0
    for html_path in (dist / 'trips').glob('*.html'):
        text = html_path.read_text(encoding='utf-8')
        refs = re.findall(r'src="\.\./photos/([^"]+)"', text)
        refs += re.findall(r"background-image:url\('\.\./photos/([^']+)'\)", text)
        for ref in refs:
            if re.match(r'https?://', ref):
                continue
            full = dist / 'photos' / ref
            if not full.exists():
                missing += 1
            elif not build.is_valid_image_file(str(full)):
                broken += 1

    report.missing_images = missing
    report.broken_images = broken
    report.checks['missing_image'] = 'PASS' if missing == 0 else 'FAIL (%d)' % missing
    report.checks['broken_image'] = 'PASS' if broken == 0 else 'FAIL (%d)' % broken
    if missing or broken:
        all_pass = False

    # Broken links (internal trip/page links; ignore cache-busted CSS)
    broken_links = 0
    for html_path in dist.rglob('*.html'):
        text = html_path.read_text(encoding='utf-8')
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(('http', '#', 'mailto:')):
                continue
            clean = href.split('?', 1)[0]
            if clean.endswith('.css'):
                continue
            if clean.startswith('/'):
                target = (dist / clean.lstrip('/')).resolve()
            else:
                target = (html_path.parent / clean).resolve()
            if not target.exists():
                broken_links += 1
    report.broken_links = broken_links
    report.checks['broken_link'] = 'PASS' if broken_links == 0 else 'FAIL (%d)' % broken_links
    if broken_links:
        all_pass = False

    # HTML build
    baikal_html = dist / 'trips' / 'baikal-rail.html'
    html_ok = baikal_html.exists() and baikal_html.stat().st_size > 1000
    report.checks['html_build'] = 'PASS' if html_ok else 'FAIL'
    if not html_ok:
        all_pass = False

    # Dist integrity
    required = [dist / 'index.html', dist / 'base.css', baikal_html]
    integrity_ok = all(p.exists() and p.stat().st_size > 0 for p in required)
    report.checks['dist_integrity'] = 'PASS' if integrity_ok else 'FAIL'
    if not integrity_ok:
        all_pass = False

    report.build_status = 'PASS' if all_pass else 'FAIL'
    return all_pass


def package_preview_deploy(config: dict) -> tuple[int, int]:
    deploy_cfg = config['deploy']
    src = ROOT / deploy_cfg['dist_prototype']
    dst = ROOT / deploy_cfg['dist_preview_deploy']
    if dst.exists():
        shutil.rmtree(dst)
    (dst / 'trips').mkdir(parents=True)

    for rel in ['index.html', 'base.css']:
        shutil.copy2(src / rel, dst / rel)
    for html in sorted((src / 'trips').glob('*.html')):
        shutil.copy2(html, dst / 'trips' / html.name)

    refs: set[str] = set()
    for html in list(dst.glob('*.html')) + list((dst / 'trips').glob('*.html')):
        text = html.read_text(encoding='utf-8')
        refs.update(re.findall(r'src="(?:\.\./)?photos/([^"]+)"', text))
        refs.update(re.findall(r"background-image:url\('(?:\.\./)?photos/([^']+)'\)", text))

    for rel in sorted(refs):
        s = src / 'photos' / rel
        if not s.exists():
            continue
        d = dst / 'photos' / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)

    # sips compression
    max_dim = deploy_cfg.get('sips_max_dimension', 1200)
    quality = deploy_cfg.get('sips_jpeg_quality', 82)
    img_count = 0
    for img in (dst / 'photos').rglob('*'):
        if img.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
            continue
        img_count += 1
        subprocess.run(
            ['sips', '--resampleHeightWidthMax', str(max_dim),
             '--setProperty', 'formatOptions', str(quality), str(img)],
            capture_output=True,
        )

    total_files = sum(1 for _ in dst.rglob('*') if _.is_file())
    return total_files, img_count


def deploy_surge(config: dict) -> tuple[bool, str | None]:
    deploy_dir = config['deploy']['dist_preview_deploy']
    domain = config['deploy']['surge_domain']
    proc = subprocess.run(
        ['surge', deploy_dir, domain],
        cwd=str(ROOT), capture_output=True, text=True, timeout=300,
    )
    url = 'https://%s/' % domain
    ok = proc.returncode == 0
    if not ok:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
    return ok, url if ok else None


def print_sync_report(report: SyncReport, state: dict, config: dict) -> None:
    print('\n' + '═' * 60)
    print('  BAIKAL RAIL PHOTO SYNC REPORT')
    print('═' * 60)

    print('\n## 1. Drive Access')
    if report.drive_access == 'ok':
        print('  Status: OK (method: %s)' % report.drive_method)
        print('  Files listed: %d' % report.drive_listed)
        print('  Baikal candidates (Day XX folders): %d' % report.drive_baikal_candidates)
    elif report.drive_access == 'blocked':
        print('  Status: BLOCKED')
        print('  Message: Google Drive 存取受限，需要登入或 API 授權')
        for err in report.errors:
            print('    - %s' % err)
        print('\n  Minimal auth setup: see content/baikal-rail/source/PHOTO_SYNC.md')
    else:
        print('  Status: %s' % report.drive_access)

    print('\n## 2. Sync Results')
    print('  New photos imported: %d' % report.new_imported)
    print('  Skipped (already synced): %d' % report.skipped_existing)
    print('  Duplicates skipped: %d' % len(report.duplicates_skipped))
    print('  Total synced in state: %d' % len(state.get('synced', [])))
    if report.updated_days:
        print('  Updated days: %s' % ', '.join('Day %d' % d for d in sorted(report.updated_days)))
    else:
        print('  Updated days: (none)')

    review_items = state.get('review_required', [])
    new_review_count = len(report.review_required)
    print('\n## 3. Review Required (%d in state%s)' % (
        len(review_items),
        ', +%d new this run' % new_review_count if new_review_count else '',
    ))
    if review_items:
        for item in review_items[:20]:
            print('  - %s [%s]' % (item.get('drive_path', '?'), item.get('reason', '?')))
        if len(review_items) > 20:
            print('  ... and %d more' % (len(review_items) - 20))
    else:
        print('  (none)')

    print('\n## 4. Remaining Gray Cards (no image in dayXX.md)')
    content_root = ROOT / config['paths']['content_root']
    gray = []
    for day in range(1, 21):
        for lm in load_day_landmarks(day, content_root):
            if not lm['has_image']:
                gray.append('Day %d: %s' % (day, lm['name']))
    for g in gray:
        print('  - %s' % g)

    print('\n## 5. Build & Checks')
    print('  Build: %s' % report.build_status)
    for check, result in report.checks.items():
        print('  %s: %s' % (check, result))

    print('\n## 6. Deploy')
    print('  Status: %s' % report.deploy_status)
    if report.deploy_url:
        print('  URL: %s' % report.deploy_url)

    if report.errors:
        print('\n## 7. Errors')
        for err in report.errors:
            print('  - %s' % err)

    print('\n' + '═' * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description='Baikal Rail Google Drive photo sync')
    parser.add_argument('--dry-run', action='store_true', help='List actions without writing')
    parser.add_argument('--skip-deploy', action='store_true', help='Skip Surge deployment')
    parser.add_argument('--skip-build', action='store_true', help='Skip build and checks')
    args = parser.parse_args()

    config = load_config()
    state_path = ROOT / config['paths']['sync_state']
    state = load_sync_state(state_path)
    report = SyncReport()

    # Update source metadata
    state['source'] = {
        'type': 'google_drive',
        'drive_url': config['drive']['folder_url'],
        'folder_id': config['drive']['folder_id'],
    }

    print('─' * 50)
    print('▶ BAIKAL RAIL PHOTO SYNC')
    print('─' * 50)

    drive_items = access_drive(config, report)

    if drive_items is None:
        # Drive blocked — still update state timestamp, no imports
        state['last_sync'] = datetime.now(timezone.utc).isoformat()
        state['summary'] = {
            'synced_count': len(state.get('synced', [])),
            'drive_access': 'blocked',
            'drive_new_imported': 0,
        }
        if not args.dry_run:
            save_sync_state(state_path, state)
        print_sync_report(report, state, config)
        return 1

    # Merge review_required from this run
    existing_review_ids = {r.get('drive_file_id') for r in state.get('review_required', [])}
    process_drive_files(drive_items, config, state, report, dry_run=args.dry_run)

    new_review = [r for r in report.review_required if r.get('drive_file_id') not in existing_review_ids]
    state['review_required'] = state.get('review_required', []) + new_review

    state['last_sync'] = datetime.now(timezone.utc).isoformat()
    state['summary'] = {
        'synced_count': len(state.get('synced', [])),
        'drive_listed': report.drive_listed,
        'drive_baikal_candidates': report.drive_baikal_candidates,
        'drive_new_imported': report.new_imported,
        'review_required_count': len(state.get('review_required', [])),
        'drive_access_method': report.drive_method,
    }

    if not args.dry_run:
        save_sync_state(state_path, state)

    if not args.skip_build and not args.dry_run:
        print('\n▶ Building prototype...')
        if run_build():
            print('▶ Running checks...')
            checks_ok = run_checks(report)
            if checks_ok and not args.skip_deploy:
                print('▶ Packaging dist-preview-deploy...')
                total_files, img_count = package_preview_deploy(config)
                print('  Packaged %d files (%d images compressed)' % (total_files, img_count))
                print('▶ Deploying to Surge...')
                ok, url = deploy_surge(config)
                report.deploy_status = 'PASS' if ok else 'FAIL'
                report.deploy_url = url
            elif checks_ok:
                report.deploy_status = 'skipped'
            else:
                report.deploy_status = 'skipped (checks failed)'
        else:
            report.build_status = 'FAIL'
            report.deploy_status = 'skipped (build failed)'

    print_sync_report(report, state, config)
    return 0 if report.drive_access == 'ok' else 1


if __name__ == '__main__':
    sys.exit(main())
