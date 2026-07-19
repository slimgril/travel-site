#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
#  丫斌哥 World Journey — 静态网站生成器（零依赖，纯 Python 3 标准库）
#  用法：python3 scripts/build.py
#
#  设计原则：
#   - content/*.md 是永久原稿，永不被本脚本改动。
#   - dist/ 每次重新生成（先清空再重建）。
#   - 只用 Python 3 标准库（macOS 自带），确保十年后仍能 python3 scripts/build.py。
# ============================================================================

import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D_CONTENT = os.path.join(ROOT, 'content')
D_PHOTOS = os.path.join(ROOT, 'photos')
D_TEMPLATES = os.path.join(ROOT, 'templates')
D_DIST = os.path.join(ROOT, 'dist')

GRADIENTS = ['g-temple', 'g-cave', 'g-tower', 'g-city', 'g-river', 'g-mountain',
             'g-gorge', 'g-museum', 'g-grass', 'g-gate', 'g-arch', 'g-shrine', 'g-ice']


# ─────────────────────────────────────────────────────────────────────────
#  Minimal YAML loader for landmarks.yaml (stdlib only; handles flat keys
#  inside a list-of-maps structure, no nested objects needed).
# ─────────────────────────────────────────────────────────────────────────
def _yaml_scalar(v):
    v = v.strip()
    if not v or v in ('null', 'Null', 'NULL', '~'):
        return None
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def load_landmarks_yaml(path):
    """Return dict keyed by chinese_name → landmark dict."""
    if not os.path.exists(path):
        return {}
    landmarks = {}
    current = None
    in_landmarks = False
    with open(path, encoding='utf-8') as fh:
        for raw_line in fh:
            line = raw_line.rstrip('\n')
            stripped = line.lstrip()
            if stripped.startswith('#'):
                continue
            if stripped == 'landmarks:':
                in_landmarks = True
                continue
            if not in_landmarks:
                continue
            # new list item
            if re.match(r'^  - ', line):
                current = {}
                m = re.match(r'^  - ([A-Za-z_]+):\s*(.*)', line)
                if m:
                    current[m.group(1)] = _yaml_scalar(m.group(2))
                    if m.group(1) == 'chinese_name' and current.get('chinese_name'):
                        landmarks[current['chinese_name']] = current
            elif current is not None and re.match(r'^    [A-Za-z_]', line):
                m = re.match(r'^    ([A-Za-z_]+):\s*(.*)', line)
                if m:
                    current[m.group(1)] = _yaml_scalar(m.group(2))
    return landmarks


# ─────────────────────────────────────────────────────────────────────────
#  小工具
# ─────────────────────────────────────────────────────────────────────────
def esc(s=''):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def inline(s=''):
    """行内 Markdown：**粗体** *斜体* `code` [text](url)。极简、可预测。"""
    t = esc(s)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(^|[^*])\*([^*]+)\*', r'\1<em>\2</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def route_html(s=''):
    t = esc(s)
    t = re.sub(r'\s*(→|->)\s*', ' <span class="route-arrow">→</span> ', t)
    t = re.sub(r'\s*✈\s*', ' <span class="route-arrow">✈</span> ', t)
    return t


# ─────────────────────────────────────────────────────────────────────────
#  Front-matter 解析（极简 YAML 子集）
# ─────────────────────────────────────────────────────────────────────────
def parse_scalar(v):
    v = v.strip()
    if not v:
        return ''
    if (v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'"):
        return v[1:-1]
    if v.startswith('[') and v.endswith(']'):
        items = [x.strip() for x in v[1:-1].split(',') if x.strip()]
        return [x[1:-1] if (x and x[0] in '"\'') else x for x in items]
    if v.startswith('{') and v.endswith('}'):
        obj = {}
        for pair in v[1:-1].split(','):
            i = pair.find(':')
            if i > -1:
                obj[pair[:i].strip()] = parse_scalar(pair[i + 1:])
        return obj
    return v


def parse_front_matter(raw):
    if not raw.startswith('---'):
        return {}, raw
    end = raw.find('\n---', 3)
    if end == -1:
        return {}, raw
    fm_text = raw[3:end].strip()
    body = raw[end + 4:]
    if body.startswith('\n'):
        body = body[1:]
    data = {}
    cur_key = None
    for line in fm_text.split('\n'):
        if re.match(r'^\s*-\s+', line) and cur_key:
            data[cur_key].append(parse_scalar(re.sub(r'^\s*-\s+', '', line)))
            continue
        m = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if val.strip() == '':
            data[key] = []
            cur_key = key
        else:
            data[key] = parse_scalar(val)
            cur_key = None
    return data, body


# ─────────────────────────────────────────────────────────────────────────
#  正文解析：# 天 / ## 区块 / ### 卡片
# ─────────────────────────────────────────────────────────────────────────
def split_days(body):
    days = []
    cur = None
    for line in body.split('\n'):
        if re.match(r'^#\s+', line):
            cur = {'heading': re.sub(r'^#\s+', '', line).strip(), 'lines': []}
            days.append(cur)
        elif cur is not None:
            cur['lines'].append(line)
    return days


def parse_day_heading(h):
    parts = [s.strip() for s in re.split(r'｜|\|', h)]
    day_num, dt, rest = '', '', ''
    if len(parts) >= 3:
        mnum = re.search(r'\d+', parts[0])
        day_num = mnum.group(0) if mnum else ''
        dt = parts[1]
        rest = ' ｜ '.join(parts[2:])
    else:
        rest = h
    route, title = rest, ''
    dash = re.search(r'\s[—–-]\s', rest)
    if dash:
        i = rest.find(dash.group(0))
        route = rest[:i].strip()
        title = rest[i + len(dash.group(0)):].strip()
    return {'day_num': day_num, 'date': dt, 'route': route, 'title': title}


def classify_block(label):
    l = label.lower()
    if re.search(r'古蹟|古迹|sites?', l):
        return 'sites'
    if re.search(r'歷史|历史|history|後記|后记|epilogue', l):
        return 'history'
    if re.search(r'現場|现场|直擊|直击|live', l):
        return 'live'
    if re.search(r'預告|预告|plan|行程', l):
        return 'plan'
    return 'prose'


def split_blocks(lines):
    blocks = []
    cur = {'kind': 'meta', 'label': '', 'lines': []}
    blocks.append(cur)
    for line in lines:
        if re.match(r'^##\s+', line):
            label = re.sub(r'^##\s+', '', line).strip()
            cur = {'kind': classify_block(label), 'label': label, 'lines': []}
            blocks.append(cur)
        else:
            cur['lines'].append(line)
    return blocks


def split_cards(lines):
    cards = []
    cur = None
    pre = []
    for line in lines:
        if re.match(r'^###\s+', line):
            cur = {'heading': re.sub(r'^###\s+', '', line).strip(), 'lines': []}
            cards.append(cur)
        elif cur is not None:
            cur['lines'].append(line)
        else:
            pre.append(line)
    return pre, cards


def extract_image(text):
    m = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', text)
    if not m:
        return None, '', text
    return m.group(2), m.group(1), text.replace(m.group(0), '').strip()


def split_heading_image(heading):
    img, alt, rest = extract_image(heading)
    name = re.sub(r'\s+', ' ', rest).strip()
    return name, img, alt


def classify_paras(lines):
    out = []
    buf = []
    in_raw = False
    raw_buf = []

    def flush():
        if buf:
            out.append({'type': 'p', 'text': ' '.join(buf)})
            buf.clear()

    for raw in lines:
        line = raw.strip()
        if in_raw:
            if line == ':::':
                out.append({'type': 'raw', 'html': '\n'.join(raw_buf)})
                raw_buf.clear()
                in_raw = False
            else:
                raw_buf.append(raw)
            continue
        if not line:
            flush()
            continue
        if line.startswith(':::raw'):
            flush()
            in_raw = True
            continue
        if line.startswith('>'):
            flush()
            out.append({'type': 'quote', 'text': re.sub(r'^>\s?', '', line)})
        elif line.startswith('✦'):
            flush()
            out.append({'type': 'tip', 'text': re.sub(r'^✦\s?', '', line)})
        else:
            buf.append(line)
    flush()
    return out


def parse_day_meta(meta_lines):
    meta = {}
    for line in meta_lines:
        m = re.match(r'^:::meta\s+(.*)$', line)
        if not m:
            continue
        for mm in re.finditer(r'([A-Za-z]+)=(.+?)(?=\s{2,}[A-Za-z]+=|$)', m.group(1)):
            meta[mm.group(1)] = mm.group(2).strip()
    return meta


# ─────────────────────────────────────────────────────────────────────────
#  区块渲染器
# ─────────────────────────────────────────────────────────────────────────
def render_sites(block, slug, gi):
    _, cards = split_cards(block['lines'])
    if not cards:
        return ''
    out = []
    for c in cards:
        name, img, _ = split_heading_image(c['heading'])
        desc = ' '.join(p['text'] for p in classify_paras(c['lines']) if p['type'] == 'p')
        if img:
            img_style = ("class=\"site-img photo\" style=\"background-image:url('../photos/%s/%s')\""
                         % (slug, img))
        else:
            img_style = 'class="site-img %s"' % GRADIENTS[gi[0] % len(GRADIENTS)]
            gi[0] += 1
        out.append(
            '      <div class="site-card">\n'
            '        <div %s><div class="img-label">%s</div></div>\n'
            '        <div class="site-body">\n'
            '          <div class="site-name">%s</div>\n'
            '          <div class="site-desc">%s</div>\n'
            '        </div>\n'
            '      </div>' % (img_style, esc(name), esc(name), inline(desc))
        )
    return '    <div class="sites-grid">\n%s\n    </div>' % '\n'.join(out)


def render_history_panel(title, body_lines):
    inner = []
    for p in classify_paras(body_lines):
        if p['type'] == 'quote':
            inner.append('      <p style="padding:12px 20px;border-left:3px solid var(--gold);'
                         'background:rgba(212,168,67,0.08);border-radius:0 8px 8px 0;font-style:italic;'
                         'color:#4a3800;">%s</p>' % inline(p['text']))
        elif p['type'] == 'tip':
            inner.append('      <div class="extra-tip">%s</div>' % inline(p['text']))
        elif p['type'] == 'raw':
            inner.append(p['html'])
        else:
            inner.append('      <p>%s</p>' % inline(p['text']))
    return ('    <div class="history-panel">\n      <h3>%s</h3>\n%s\n    </div>'
            % (esc(title), '\n'.join(inner)))


def render_history(block):
    pre, cards = split_cards(block['lines'])
    if cards:
        return '\n'.join(render_history_panel(c['heading'], c['lines']) for c in cards)
    return render_history_panel(block['label'], pre)


def render_live(block, slug, day_meta):
    _, cards = split_cards(block['lines'])
    if not cards:
        return ''
    route_clean = re.sub(r'<[^>]+>', '', day_meta['route'])
    date_line = ('%s　%s' % (day_meta['date'], route_clean)) if day_meta['date'] else '實況記錄'
    grid = []
    for c in cards:
        heading = c['heading']
        feature = bool(re.search(r'⭐|\{feature\}', heading))
        clean_heading = re.sub(r'⭐|\{feature\}', '', heading).strip()
        name, img, _ = split_heading_image(clean_heading)
        is_note = bool(re.search(r'隨筆|随笔', name))
        time_label = re.sub(r'隨筆|随笔', '', name).strip()
        desc_html = []
        for p in classify_paras(c['lines']):
            if p['type'] == 'quote':
                desc_html.append('          <blockquote>%s</blockquote>' % inline(p['text']))
            else:
                desc_html.append('          <div class="live-desc">%s</div>' % inline(p['text']))
        img_tag = ('        <img class="live-img" src="../photos/%s/%s" alt="%s">'
                   % (slug, img, esc(name))) if img else ''
        tag = ' <span class="live-tag">丫斌哥隨筆</span>' if is_note else ''
        grid.append(
            '      <div class="live-card%s">\n'
            '%s\n'
            '        <div class="live-body">\n'
            '          <div class="live-time">%s%s</div>\n'
            '%s\n'
            '        </div>\n'
            '      </div>' % (' live-feature' if feature else '', img_tag,
                             esc(time_label), tag, '\n'.join(desc_html))
        )
    return (
        '    <div class="live-dispatch">\n'
        '      <div class="live-header">\n'
        '        <span class="live-badge">🔴 丫斌哥現場直擊</span>\n'
        '        <span class="live-date">%s</span>\n'
        '      </div>\n'
        '      <div class="live-grid">\n%s\n      </div>\n'
        '    </div>' % (esc(date_line), '\n'.join(grid))
    )


def render_plan(block, landmarks=None, diagonal=False):
    _, cards = split_cards(block['lines'])
    out = []
    landmarks = landmarks or {}
    for i, c in enumerate(cards):
        name, _, _ = split_heading_image(c['heading'])
        desc = ' '.join(p['text'] for p in classify_paras(c['lines']) if p['type'] == 'p')
        lm = landmarks.get(name)
        if lm is None:
            # fuzzy: find landmark whose chinese_name starts with card name, or vice versa
            for k, v in landmarks.items():
                if k.startswith(name) or name.startswith(k):
                    lm = v
                    break
        hero = lm.get('hero_image') if lm else None
        if hero and lm.get('image_verification_status') == 'verified':
            img_div = ('        <div class="site-img photo" style="background-image:url(\'../%s\')">'
                       '<div class="img-label">%s</div></div>' % (hero, esc(name)))
            attribution = lm.get('attribution', '')
            license_txt = lm.get('license', '')
            official_url = lm.get('official_url') or ''
            meta_parts = []
            if attribution:
                meta_parts.append('<span class="site-attribution">%s · %s</span>'
                                  % (esc(attribution), esc(license_txt)))
            if official_url and official_url not in ('null', 'unverified', ''):
                meta_parts.append('<span class="site-attribution"><a href="%s" target="_blank" rel="noopener">官方資訊</a>'
                                  ' <span class="site-ref-img-badge">參考圖片</span></span>' % esc(official_url))
            meta_html = ('          <div class="site-meta">\n            %s\n          </div>'
                         % '\n            '.join(meta_parts)) if meta_parts else ''
        else:
            img_div = ('        <div class="site-img %s"><div class="img-label">%s</div></div>'
                       % (GRADIENTS[i % len(GRADIENTS)], esc(name)))
            meta_html = ''
        role = ''
        kicker = ''
        if diagonal and len(cards) == 2:
            if i == 0:
                role = ' site-card--diag-primary'
                kicker = '        <div class="diag-kicker">上午 · 歷史人文</div>\n'
            else:
                role = ' site-card--diag-secondary'
                kicker = '        <div class="diag-kicker">午後 · 現代生活</div>\n'
        out.append(
            '      <div class="site-card%s">\n'
            '%s'
            '%s\n'
            '        <div class="site-body">\n'
            '          <div class="site-name">%s</div>\n'
            '          <div class="site-desc">%s</div>\n'
            '%s\n'
            '        </div>\n'
            '      </div>' % (role, kicker, img_div, esc(name), inline(desc), meta_html)
        )
    if diagonal and len(out) == 2:
        spine = (
            '      <div class="diag-spine" aria-hidden="true">'
            '<span class="diag-spine-dot"></span>'
            '<span class="diag-spine-line"></span>'
            '<span class="diag-spine-label">行程動線</span>'
            '<span class="diag-spine-arrow">→</span>'
            '</div>\n'
        )
        souvenirs = (
            '      <aside class="diag-souvenirs" aria-label="立陶宛紀念小物">'
            '<span class="diag-souv diag-souv--a">琥珀吊墜</span>'
            '<span class="diag-souv diag-souv--b">黑麥麵包</span>'
            '<span class="diag-souv diag-souv--c">木雕鸛鳥</span>'
            '<span class="diag-souv diag-souv--d">櫻桃酒磁鐵</span>'
            '<span class="diag-souv diag-souv--e">亞麻手巾</span>'
            '<span class="diag-souv diag-souv--f">Cepelinai 胸針</span>'
            '</aside>\n'
        )
        return (
            '    <div class="sites-grid sites-grid--diagonal">\n'
            '%s%s%s\n'
            '    </div>' % (spine, souvenirs, '\n'.join(out))
        )
    return '    <div class="sites-grid">\n%s\n    </div>' % '\n'.join(out)


# ─────────────────────────────────────────────────────────────────────────
#  组装一天
# ─────────────────────────────────────────────────────────────────────────
def render_day(day, slug, status, gi, landmarks=None):
    head = parse_day_heading(day['heading'])
    blocks = split_blocks(day['lines'])
    meta_block = next((b for b in blocks if b['kind'] == 'meta'), None)
    day_meta = parse_day_meta(meta_block['lines'] if meta_block else [])
    day_meta_live = {'date': head['date'], 'route': head['route']}

    acc = ''
    if day_meta.get('lodging'):
        acc = ('    <div class="accommodation"><div class="acc-label">住宿</div>'
               '<div class="acc-name">%s</div></div>' % esc(day_meta['lodging']))
    extra = []
    if day_meta.get('flight'):
        extra.append('航班：%s' % esc(day_meta['flight']))
    if day_meta.get('meals'):
        extra.append('餐食：%s' % esc(day_meta['meals']))
    if day_meta.get('leader'):
        extra.append('領隊：%s' % esc(day_meta['leader']))
    meta_tip = ('    <div class="extra-tip">%s</div>' % '　|　'.join(extra)) if extra else ''

    sections = []
    day_num = head.get('day_num') or ''
    use_diagonal = (day_num == '2')  # 2026-07-19 斜對角動線首試（BLDH Day 2）
    for b in blocks:
        if b['kind'] == 'sites':
            sections.append(render_sites(b, slug, gi))
        elif b['kind'] == 'history':
            sections.append(render_history(b))
        elif b['kind'] == 'live' and status == 'done':
            sections.append(render_live(b, slug, day_meta_live))
        elif b['kind'] == 'plan':
            sections.append(render_plan(b, landmarks, diagonal=use_diagonal))

    did = ('d%s' % head['day_num']) if head['day_num'] else ''
    day_extra_class = ' day-section--diagonal' if use_diagonal else ''
    route_div = ('<div class="route">%s</div>' % route_html(head['route'])) if head['route'] else ''
    return (
        '<div class="day-divider"></div>\n'
        '<section class="day-section%s" id="%s">\n'
        '  <div class="day-header">\n'
        '    <div class="day-badge"><div class="num">%s</div><div class="label">DAY</div></div>\n'
        '    <div class="day-info">\n'
        '      <div class="date">%s</div>\n'
        '      <h2>%s</h2>\n'
        '      %s\n'
        '    </div>\n'
        '%s\n'
        '  </div>\n'
        '%s\n'
        '%s\n'
        '</section>' % (
            day_extra_class, did, esc(head['day_num']), esc(head['date']),
            esc(head['title'] or head['route']), route_div, acc, meta_tip,
            '\n'.join(s for s in sections if s)
        )
    )


# ─────────────────────────────────────────────────────────────────────────
#  组装一趟旅程页
# ─────────────────────────────────────────────────────────────────────────
def render_trip_page(trip, shell, prev_trip, next_trip, landmarks=None):
    data, days, slug = trip['data'], trip['days'], trip['slug']
    gi = [0]
    title_html = re.sub(r'\{([^}]+)\}', r'<span>\1</span>', (data.get('title') or slug))

    stats = data.get('stats') if isinstance(data.get('stats'), list) else []
    stats_html = '\n'.join(
        '      <div class="stat"><div class="stat-num">%s</div>'
        '<div class="stat-label">%s</div></div>' % (esc(s.get('num', '')), esc(s.get('label', '')))
        for s in stats if isinstance(s, dict)
    )
    badge = data.get('hero_badge') or ('即將啟程' if data.get('status') == 'upcoming' else '')
    hero = (
        '<section class="hero">\n'
        '  %s\n'
        '  <h1>%s</h1>\n'
        '  %s\n'
        '  %s\n'
        '  %s\n'
        '  <div class="scroll-hint">▼ 向下展開旅程</div>\n'
        '</section>' % (
            ('<div class="hero-badge">%s</div>' % esc(badge)) if badge else '',
            title_html,
            ('<p class="hero-sub">%s</p>' % esc(data['subtitle'])) if data.get('subtitle') else '',
            ('<p style="color:var(--gold-light);font-size:1.05rem;margin-top:14px;'
             'letter-spacing:1px;max-width:600px;position:relative;">%s</p>' % inline(data['hero_quote']))
            if data.get('hero_quote') else '',
            ('<div class="hero-stats">\n%s\n  </div>' % stats_html) if stats_html else ''
        )
    )

    nav_items = []
    for d in days:
        h = parse_day_heading(d['heading'])
        if h['day_num']:
            label = (h['title'] or h['route'])[:4]
            nav_items.append('  <a href="#d%s">D%s %s</a>' % (h['day_num'], h['day_num'], esc(label)))
    nav = ('<nav class="days-nav">\n%s\n</nav>' % ''.join(nav_items)) if nav_items else ''

    map_html = ''
    if data.get('map_svg'):
        p = os.path.join(D_CONTENT, data['map_svg'])
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                svg = f.read()
            map_html = (
                '<section class="map-section">\n'
                '  <div class="section-title">ROUTE MAP</div>\n'
                '  <h2 class="section-heading">%s・足跡總覽</h2>\n'
                '  <div class="map-container">%s</div>\n'
                '</section>' % (esc(data.get('title') or slug), svg)
            )

    day_html = '\n'.join(render_day(d, slug, data.get('status'), gi, landmarks) for d in days)

    def clean_title(t):
        return re.sub(r'[{}]', '', t or '')

    links = []
    links.append('<a href="%s.html">← %s</a>' % (prev_trip['slug'], esc(clean_title(prev_trip['data'].get('title') or prev_trip['slug'])))
                 if prev_trip else '<span></span>')
    links.append('<a href="../index.html">回首頁</a>')
    links.append('<a href="%s.html">%s →</a>' % (next_trip['slug'], esc(clean_title(next_trip['data'].get('title') or next_trip['slug'])))
                 if next_trip else '<span></span>')
    footer = (
        '<footer>\n'
        '  <div style="display:flex;justify-content:space-between;max-width:900px;'
        'margin:0 auto 20px;gap:16px;flex-wrap:wrap;">\n    %s\n  </div>\n'
        '  <p><strong>丫斌哥 World Journey</strong>　%s %s</p>\n'
        '  <p style="margin-top:8px;font-size:0.78rem;">© 2026　持續更新中…</p>\n'
        '</footer>' % ('\n    '.join(links), esc(data.get('number', '')), esc(clean_title(data.get('title') or slug)))
    )

    body = '\n\n'.join(x for x in [hero, map_html, nav, day_html, footer] if x)
    safe_title = re.sub(r'[{}]', '', data.get('title') or slug)
    return (shell.replace('{{TITLE}}', esc(safe_title))
                 .replace('{{DESC}}', esc(data.get('summary', '')))
                 .replace('{{BODY}}', body))


# ─────────────────────────────────────────────────────────────────────────
#  首页
# ─────────────────────────────────────────────────────────────────────────
# About Ben / 旅人介紹——恢復自山西原首頁；肖像使用 photos/site/（網站層級素材，
# 非任何 Trip 的行程照片）。此段含字面 %（width:100% 等），為模組層級常數，
# render_index() 只引用、不重新組裝。
TRAVELER_SECTION = (
    '<section style="background:linear-gradient(135deg,#0D2B1F 0%,#1B4332 60%,#2D4A22 100%);'
    ' padding:80px 20px; text-align:center; position:relative; overflow:hidden;">\n'
    '  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,'
    ' rgba(212,168,67,0.08) 0%, transparent 70%);"></div>\n'
    '  <div style="max-width:720px;margin:0 auto;position:relative;">\n'
    '    <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:20px;'
    'margin-bottom:44px;align-items:flex-end;">\n'
    '      <div style="position:relative;flex-shrink:0;">\n'
    '        <div style="width:200px;height:260px;border-radius:20px;overflow:hidden;'
    'border:3px solid rgba(212,168,67,0.5);box-shadow:0 16px 48px rgba(0,0,0,0.5);">\n'
    '          <img src="photos/site/yabin-wuxi.jpg" alt="丫斌哥 無錫"'
    ' style="width:100%;height:100%;object-fit:cover;object-position:center top;">\n'
    '        </div>\n'
    '        <div style="position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);'
    'background:rgba(0,0,0,0.75);color:rgba(255,255,255,0.7);font-size:0.7rem;padding:4px 12px;'
    'border-radius:20px;white-space:nowrap;border:1px solid rgba(255,255,255,0.15);">\n'
    '          📍 無錫・2026.03\n'
    '        </div>\n'
    '      </div>\n'
    '      <div style="flex:1;min-width:220px;max-width:320px;text-align:center;padding:0 8px;">\n'
    '        <div style="font-size:4rem;color:rgba(212,168,67,0.2);line-height:0.8;'
    'margin-bottom:12px;font-family:Georgia,serif;">&ldquo;</div>\n'
    '        <div style="display:inline-flex;align-items:center;gap:12px;'
    'background:rgba(255,255,255,0.07);border:1px solid rgba(212,168,67,0.35);border-radius:40px;'
    'padding:8px 22px;margin-bottom:20px;">\n'
    '          <span style="color:var(--gold-light);letter-spacing:3px;font-size:0.82rem;'
    'font-weight:600;">旅　人</span>\n'
    '          <span style="color:#fff;font-size:1.05rem;font-weight:700;'
    'letter-spacing:2px;">丫斌哥</span>\n'
    '        </div>\n'
    '        <p style="color:#fff;font-size:clamp(1.1rem,3vw,1.5rem);font-weight:300;'
    'line-height:1.9;letter-spacing:0.05em;">\n'
    '          退休，不是句點——<br>是另一段旅程的<br>'
    '<strong style="color:var(--gold);font-weight:700;">起點</strong>。\n'
    '        </p>\n'
    '      </div>\n'
    '      <div style="position:relative;flex-shrink:0;">\n'
    '        <div style="width:200px;height:260px;border-radius:20px;overflow:hidden;'
    'border:3px solid rgba(212,168,67,0.5);box-shadow:0 16px 48px rgba(0,0,0,0.5);">\n'
    '          <img src="photos/site/yabin-dalat.jpg" alt="丫斌哥 大叻"'
    ' style="width:100%;height:100%;object-fit:cover;object-position:center top;">\n'
    '        </div>\n'
    '        <div style="position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);'
    'background:rgba(0,0,0,0.75);color:rgba(255,255,255,0.7);font-size:0.7rem;padding:4px 12px;'
    'border-radius:20px;white-space:nowrap;border:1px solid rgba(255,255,255,0.15);">\n'
    '          📍 越南大叻・2026.05\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '    <div style="width:60px;height:2px;background:linear-gradient(90deg,transparent,'
    'var(--gold),transparent);margin:0 auto 32px;"></div>\n'
    '    <p style="color:rgba(255,255,255,0.78);font-size:1.05rem;line-height:2;'
    'letter-spacing:0.03em;margin-bottom:28px;">\n'
    '      帥氣、有個性，骨子裡藏著一股不安分的靈魂。<br>\n'
    '      在人生最自由的時刻，他立下誓言：<br>\n'
    '      <strong style="color:var(--gold-light);">用餘生走遍天下，用雙腳丈量世界，'
    '用心去感受每一片土地的呼吸。</strong>\n'
    '    </p>\n'
    '    <p style="color:rgba(255,255,255,0.6);font-size:0.98rem;line-height:2;'
    'letter-spacing:0.03em;margin-bottom:36px;">\n'
    '      不是走馬看花，不是打卡留念。<br>\n'
    '      他要的是真正的相遇——與古城相遇，與歷史相遇，<br>\n'
    '      與陌生的人情風土，面對面地相遇。\n'
    '    </p>\n'
    '    <p style="color:rgba(255,255,255,0.78);font-size:1.05rem;line-height:2;'
    'letter-spacing:0.03em;margin-bottom:0;">\n'
    '      這本旅誌，是他送給自己的禮物，<br>\n'
    '      也是他向每一位讀者發出的邀請：<br>\n'
    '      <strong style="color:#fff;">翻開每一頁，你不只是讀者，你是他的旅伴。</strong>\n'
    '    </p>\n'
    '  </div>\n'
    '</section>\n\n'
)


def render_index(trips, shell):
    done = [t for t in trips if t['data'].get('status') == 'done']
    countries, cities = set(), set()
    total_days = 0
    for t in done:
        for x in (t['data'].get('tags') if isinstance(t['data'].get('tags'), list) else []):
            countries.add(x)
        for d in t['days']:
            h = parse_day_heading(d['heading'])
            for c in re.split(r'→|->|✈|\s', h['route']):
                c = c.strip()
                if len(c) > 1:
                    cities.add(c)
        if t['data'].get('date_start') and t['data'].get('date_end'):
            try:
                ds = date.fromisoformat(str(t['data']['date_start']))
                de = date.fromisoformat(str(t['data']['date_end']))
                total_days += (de - ds).days + 1
            except ValueError:
                pass

    stat_defs = [
        (countries and len(countries) or len(done), '個國家／地區'),
        (len(cities), '座城市'),
        (total_days, '天旅程'),
    ]
    stat_cards = '\n'.join(
        '      <div class="stat"><div class="stat-num">%s</div>'
        '<div class="stat-label">%s</div></div>' % (n, lbl) for n, lbl in stat_defs
    )

    series = []
    for t in trips:
        d = t['data']
        is_done = d.get('status') == 'done'
        is_up = d.get('status') == 'upcoming'
        mark = '✓ 已完成' if is_done else ('⏳ 即將出發' if is_up else '□ 規劃中')
        cls = 'series-done' if is_done else 'series-future'
        series.append(
            '    <a class="series-card %s" href="trips/%s.html">\n'
            '      <div class="series-num">%s</div>\n'
            '      <div class="series-title">%s</div>\n'
            '      <div class="series-sub">%s</div>\n'
            '      <div class="series-summary">%s</div>\n'
            '      <div class="series-mark">%s</div>\n'
            '    </a>' % (
                cls, t['slug'], esc(d.get('number', '')),
                esc(re.sub(r'[{}]', '', d.get('title') or t['slug'])),
                esc(d.get('subtitle', '')), esc(d.get('summary', '')), mark
            )
        )

    # Hero（%s = stat_cards）——單獨格式化，避免下方 About Ben 的字面 % 被誤解析
    hero = (
        '<section class="hero">\n'
        '  <div class="hero-badge">World Journey</div>\n'
        '  <h1>旅人：<span>丫斌哥</span></h1>\n'
        '  <p class="hero-sub">退休，不是終點——而是另一段探索世界的開始。</p>\n'
        '  <div class="hero-stats">\n%s\n  </div>\n'
        '  <div class="scroll-hint">▼ 所有旅程</div>\n'
        '</section>\n\n'
    ) % stat_cards

    # About Ben / 旅人介紹——恢復自山西原首頁；模組層級 TRAVELER_SECTION 常數。
    traveler = TRAVELER_SECTION

    # THE JOURNEYS（%s = series 卡片）
    journeys = (
        '<section style="max-width:1100px;margin:0 auto;padding:60px 20px;">\n'
        '  <div class="section-title" style="color:var(--gold);text-align:center;">THE JOURNEYS</div>\n'
        '  <h2 class="section-heading" style="color:var(--green-dark);text-align:center;">世界旅行計畫</h2>\n'
        '  <div class="series-grid">\n%s\n  </div>\n'
        '</section>\n\n'
    ) % '\n'.join(series)

    footer = (
        '<footer>\n'
        '  <p><strong>丫斌哥 World Journey</strong></p>\n'
        '  <p style="margin-top:8px;font-size:0.78rem;">用餘生走遍天下，用雙腳丈量世界。© 2026</p>\n'
        '</footer>'
    )

    body = hero + traveler + journeys + footer

    return (shell.replace('{{TITLE}}', '丫斌哥 World Journey — 退休後的世界旅行計畫')
                 .replace('{{DESC}}', '退休不是終點，而是另一段探索世界的開始。丫斌哥的世界旅行計畫。')
                 .replace('{{BODY}}', body))


# ─────────────────────────────────────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────────────────────────────────────
def copy_tree(src, dst, skip=None):
    """复制目录树。skip 内的目录名（任意层级）会被跳过——
    用于把 photos/<slug>/originals/ 原始照片仓库排除在发布品之外。"""
    skip = skip or set()
    os.makedirs(dst, exist_ok=True)
    for name in os.listdir(src):
        if name in skip:
            continue
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isdir(s):
            copy_tree(s, d, skip)
        else:
            if name.startswith('.') or re.search(r' \d+\.[^.]+$', name):
                continue
            if os.path.getsize(s) == 0:
                continue
            shutil.copy2(s, d)


def load_trip_single(md_path):
    """单文件模式：content/<slug>.md"""
    with open(md_path, encoding='utf-8') as fh:
        raw = fh.read()
    data, body = parse_front_matter(raw)
    slug = data.get('slug') or os.path.basename(md_path)[:-3]
    return {'slug': slug, 'data': data, 'days': split_days(body)}


def load_trip_folder(folder):
    """文件夹模式：content/<slug>/trip.md（元数据）+ dayNN.md（每天一档，按文件名排序）。
    每个 dayNN.md 可含或不含 front-matter；正文直接拼接后统一 split_days。"""
    trip_md = os.path.join(folder, 'trip.md')
    with open(trip_md, encoding='utf-8') as fh:
        data, _ = parse_front_matter(fh.read())
    slug = data.get('slug') or os.path.basename(folder)
    day_files = sorted(f for f in os.listdir(folder)
                       if re.match(r'^day\d+\.md$', f, re.IGNORECASE))
    bodies = []
    for df in day_files:
        with open(os.path.join(folder, df), encoding='utf-8') as fh:
            _, body = parse_front_matter(fh.read())
        bodies.append(body.strip())
    return {'slug': slug, 'data': data, 'days': split_days('\n\n'.join(bodies))}


def main(dist_dir=None, overlay=None, label='dist/', landmarks_patch=None):
    """dist_dir: 輸出目錄，預設 D_DIST（生產環境，行為與原版完全相同）。
    overlay: 選用 callback，簽名 overlay(dist_dir, photos_root)，在 photos/ 複製到
             dist 之後執行——目前只有 Prototype Build 用它把 cooked/matched/ 疊到
             dist-prototype 的複本上，不會動到磁碟上的 photos/<slug>/reference/。
    label: 純粹用於最後一行輸出訊息，方便分辨生產／原型 build。
    landmarks_patch: 選用 dict，{slug: {chinese_name: {欄位: 值, ...}}}——只在記憶體裡
             覆寫 load_landmarks_yaml() 讀出的欄位（例如給還沒有 reference/ 檔案、
             未完整核實地點的景點一張示意用途的照片），不會寫回 landmarks.yaml。
             預設 None，生產環境完全不受影響。"""
    dist_dir = dist_dir or D_DIST

    trips = []
    for name in sorted(os.listdir(D_CONTENT)):
        p = os.path.join(D_CONTENT, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'trip.md')):
            trips.append(load_trip_folder(p))
        elif name.endswith('.md'):
            trips.append(load_trip_single(p))

    trips.sort(key=lambda t: str(t['data'].get('date_start') or ''))

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(os.path.join(dist_dir, 'trips'), exist_ok=True)

    with open(os.path.join(D_TEMPLATES, 'shell.html'), encoding='utf-8') as f:
        shell = f.read()
    with open(os.path.join(D_TEMPLATES, 'index-shell.html'), encoding='utf-8') as f:
        index_shell = f.read()

    for i, t in enumerate(trips):
        prev_t = trips[i - 1] if i > 0 else None
        next_t = trips[i + 1] if i < len(trips) - 1 else None
        lm_path = os.path.join(D_CONTENT, t['slug'], 'landmarks.yaml')
        trip_landmarks = load_landmarks_yaml(lm_path)
        patch = (landmarks_patch or {}).get(t['slug'])
        if patch:
            for cname, fields in patch.items():
                if cname in trip_landmarks:
                    trip_landmarks[cname].update(fields)
        html = render_trip_page(t, shell, prev_t, next_t, trip_landmarks)
        with open(os.path.join(dist_dir, 'trips', '%s.html' % t['slug']), 'w', encoding='utf-8') as f:
            f.write(html)

    with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_index(trips, index_shell))

    shutil.copy2(os.path.join(D_TEMPLATES, 'base.css'), os.path.join(dist_dir, 'base.css'))
    if os.path.exists(D_PHOTOS):
        copy_tree(D_PHOTOS, os.path.join(dist_dir, 'photos'), skip={'originals', 'unassigned', 'source', 'cooked'})

    if overlay is not None:
        overlay(dist_dir, D_PHOTOS)

    missing = 0
    for t in trips:
        with open(os.path.join(dist_dir, 'trips', '%s.html' % t['slug']), encoding='utf-8') as f:
            html = f.read()
        # <img src="../photos/...">（day 卡片、live 卡片）
        # 與 background-image:url('../photos/...')（plan hero、sites 卡片）都要檢查，
        # 否則 CSS 背景圖的缺圖會被漏掉（hero image 走的正是這條路徑）。
        refs = re.findall(r'src="\.\./photos/([^"]+)"', html)
        refs += re.findall(r"background-image:url\('\.\./photos/([^']+)'\)", html)
        for path in refs:
            if not os.path.exists(os.path.join(dist_dir, 'photos', path)):
                print('  ⚠ 缺图：%s（%s）' % (path, t['slug']))
                missing += 1

    print('─' * 50)
    print('✓ 生成 %d 趟旅程：%s' % (len(trips), ', '.join((t['data'].get('number', '') + t['slug']) for t in trips)))
    for t in trips:
        print('    %s: %d 天, status=%s' % (t['slug'], len(t['days']), t['data'].get('status')))
    print('✓ 缺图 %d 张' % missing)
    print('✓ 输出 → %s' % label)
    print('─' * 50)


if __name__ == '__main__':
    main()
