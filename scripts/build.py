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
    if re.search(r'歷史|历史|history', l):
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


def render_plan(block):
    _, cards = split_cards(block['lines'])
    out = []
    for i, c in enumerate(cards):
        name, _, _ = split_heading_image(c['heading'])
        desc = ' '.join(p['text'] for p in classify_paras(c['lines']) if p['type'] == 'p')
        out.append(
            '      <div class="site-card">\n'
            '        <div class="site-img %s"><div class="img-label">%s</div></div>\n'
            '        <div class="site-body">\n'
            '          <div class="site-name">%s</div>\n'
            '          <div class="site-desc">%s</div>\n'
            '        </div>\n'
            '      </div>' % (GRADIENTS[i % len(GRADIENTS)], esc(name), esc(name), inline(desc))
        )
    return '    <div class="sites-grid">\n%s\n    </div>' % '\n'.join(out)


# ─────────────────────────────────────────────────────────────────────────
#  组装一天
# ─────────────────────────────────────────────────────────────────────────
def render_day(day, slug, status, gi):
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
    for b in blocks:
        if b['kind'] == 'sites':
            sections.append(render_sites(b, slug, gi))
        elif b['kind'] == 'history':
            sections.append(render_history(b))
        elif b['kind'] == 'live' and status == 'done':
            sections.append(render_live(b, slug, day_meta_live))
        elif b['kind'] == 'plan':
            sections.append(render_plan(b))

    did = ('d%s' % head['day_num']) if head['day_num'] else ''
    route_div = ('<div class="route">%s</div>' % route_html(head['route'])) if head['route'] else ''
    return (
        '<div class="day-divider"></div>\n'
        '<section class="day-section" id="%s">\n'
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
            did, esc(head['day_num']), esc(head['date']),
            esc(head['title'] or head['route']), route_div, acc, meta_tip,
            '\n'.join(s for s in sections if s)
        )
    )


# ─────────────────────────────────────────────────────────────────────────
#  组装一趟旅程页
# ─────────────────────────────────────────────────────────────────────────
def render_trip_page(trip, shell, prev_trip, next_trip):
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

    day_html = '\n'.join(render_day(d, slug, data.get('status'), gi) for d in days)

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

    body = (
        '<section class="hero">\n'
        '  <div class="hero-badge">World Journey</div>\n'
        '  <h1>旅人：<span>丫斌哥</span></h1>\n'
        '  <p class="hero-sub">退休，不是終點——而是另一段探索世界的開始。</p>\n'
        '  <div class="hero-stats">\n%s\n  </div>\n'
        '  <div class="scroll-hint">▼ 所有旅程</div>\n'
        '</section>\n\n'
        '<section style="max-width:1100px;margin:0 auto;padding:60px 20px;">\n'
        '  <div class="section-title" style="color:var(--gold);text-align:center;">THE JOURNEYS</div>\n'
        '  <h2 class="section-heading" style="color:var(--green-dark);text-align:center;">世界旅行計畫</h2>\n'
        '  <div class="series-grid">\n%s\n  </div>\n'
        '</section>\n\n'
        '<footer>\n'
        '  <p><strong>丫斌哥 World Journey</strong></p>\n'
        '  <p style="margin-top:8px;font-size:0.78rem;">用餘生走遍天下，用雙腳丈量世界。© 2026</p>\n'
        '</footer>' % (stat_cards, '\n'.join(series))
    )

    return (shell.replace('{{TITLE}}', '丫斌哥 World Journey — 退休後的世界旅行計畫')
                 .replace('{{DESC}}', '退休不是終點，而是另一段探索世界的開始。丫斌哥的世界旅行計畫。')
                 .replace('{{BODY}}', body))


# ─────────────────────────────────────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────────────────────────────────────
def copy_tree(src, dst):
    os.makedirs(dst, exist_ok=True)
    for name in os.listdir(src):
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isdir(s):
            copy_tree(s, d)
        else:
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


def main():
    trips = []
    for name in sorted(os.listdir(D_CONTENT)):
        p = os.path.join(D_CONTENT, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'trip.md')):
            trips.append(load_trip_folder(p))
        elif name.endswith('.md'):
            trips.append(load_trip_single(p))

    trips.sort(key=lambda t: str(t['data'].get('date_start') or ''))

    if os.path.exists(D_DIST):
        shutil.rmtree(D_DIST)
    os.makedirs(os.path.join(D_DIST, 'trips'), exist_ok=True)

    with open(os.path.join(D_TEMPLATES, 'shell.html'), encoding='utf-8') as f:
        shell = f.read()
    with open(os.path.join(D_TEMPLATES, 'index-shell.html'), encoding='utf-8') as f:
        index_shell = f.read()

    for i, t in enumerate(trips):
        prev_t = trips[i - 1] if i > 0 else None
        next_t = trips[i + 1] if i < len(trips) - 1 else None
        html = render_trip_page(t, shell, prev_t, next_t)
        with open(os.path.join(D_DIST, 'trips', '%s.html' % t['slug']), 'w', encoding='utf-8') as f:
            f.write(html)

    with open(os.path.join(D_DIST, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_index(trips, index_shell))

    shutil.copy2(os.path.join(D_TEMPLATES, 'base.css'), os.path.join(D_DIST, 'base.css'))
    if os.path.exists(D_PHOTOS):
        copy_tree(D_PHOTOS, os.path.join(D_DIST, 'photos'))

    missing = 0
    for t in trips:
        with open(os.path.join(D_DIST, 'trips', '%s.html' % t['slug']), encoding='utf-8') as f:
            html = f.read()
        for m in re.finditer(r'src="\.\./photos/([^"]+)"', html):
            if not os.path.exists(os.path.join(D_DIST, 'photos', m.group(1))):
                print('  ⚠ 缺图：%s（%s）' % (m.group(1), t['slug']))
                missing += 1

    print('─' * 50)
    print('✓ 生成 %d 趟旅程：%s' % (len(trips), ', '.join((t['data'].get('number', '') + t['slug']) for t in trips)))
    for t in trips:
        print('    %s: %d 天, status=%s' % (t['slug'], len(t['days']), t['data'].get('status')))
    print('✓ 缺图 %d 张' % missing)
    print('✓ 输出 → dist/')
    print('─' * 50)


if __name__ == '__main__':
    main()
