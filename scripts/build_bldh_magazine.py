#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 本排版器依照根目錄的 `city-magazine-template.md` 所定義的
# 「城市雜誌風排版器模板」運作。
# 所有排版邏輯（大標題＋斜體副標、行距 1.75、字重 300–400、
# 全寬圖片、上下留白、--- 分隔、✦ 側註、Day kicker、meta 卡片、
# 歷史／古蹟／預告分節標）皆以該模板為準。
"""
Generate a standalone "city-walk magazine" style page for the BLDH Trio trip.

- Scope: ONLY content/bldh-trio/ (does not touch build.py, base.css, or other trips).
- Faithful: text is taken verbatim from the day*.md files (layout only, no wording changes).
- Output: content/bldh-trio/bldh-trio-magazine.html (a single, clean, self-contained
  HTML file with a small embedded stylesheet). It is ignored by build.py, so the live
  site and its deployment are unaffected.

Typography per brief: line-height 1.75, thin weights (300-400), big title + one-line
italic subtitle per spot, generous whitespace around full-width (uncropped) images,
hairline dividers between entries.
"""
import os
import re
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIP_DIR = os.path.join(ROOT, 'content', 'bldh-trio')
OUT = os.path.join(TRIP_DIR, 'bldh-trio-magazine.html')

META_LABELS = {
    'meals': None,       # handled specially (split into cards)
    'lodging': '住宿',
    'flight': '航班',
    'leader': '領隊',
    'guide': '導遊',
}


def esc(s):
    return html.escape(s, quote=True)


def parse_front_matter(path):
    data = {}
    if not os.path.exists(path):
        return data
    lines = open(path, encoding='utf-8').read().splitlines()
    if not lines or lines[0].strip() != '---':
        return data
    for l in lines[1:]:
        if l.strip() == '---':
            break
        m = re.match(r'^([a-zA-Z_]+):\s*(.*)$', l)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def parse_meta(meta_line):
    body = meta_line[len(':::meta'):].strip()
    out = []
    for m in re.finditer(r'(\w+)=(.*?)(?=\s+\w+=|$)', body):
        out.append((m.group(1), m.group(2).strip()))
    return out


def split_lead(paragraph):
    """First sentence (through first 。/！/？) becomes the italic subtitle."""
    m = re.search(r'[。！？]', paragraph)
    if not m:
        return paragraph.strip(), ''
    k = m.end()
    return paragraph[:k].strip(), paragraph[k:].strip()


def parse_day(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    title = lines[0].lstrip('#').strip() if lines else ''
    meta = []
    entries = []
    cur = None
    section = None
    for l in lines[1:]:
        if l.startswith(':::meta'):
            meta = parse_meta(l)
            continue
        if l.startswith(':::'):
            continue
        if l.startswith('## '):
            section = l[3:].strip()
            continue
        m = re.match(r'^###\s+!\[(.*?)\]\((.*?)\)\s+(.*)$', l)
        if m:
            cur = {'name': m.group(3).strip(), 'img': m.group(2).strip(),
                   'alt': m.group(1).strip(), 'section': section, 'raw': []}
            entries.append(cur)
            continue
        m = re.match(r'^###\s+(.*)$', l)
        if m:
            cur = {'name': m.group(1).strip(), 'img': None, 'alt': '',
                   'section': section, 'raw': []}
            entries.append(cur)
            continue
        if cur is not None:
            cur['raw'].append(l)
    for e in entries:
        # split raw buffer into paragraphs by blank lines
        paras, buf = [], []
        for r in e['raw']:
            if r.strip():
                buf.append(r.strip())
            elif buf:
                paras.append(' '.join(buf)); buf = []
        if buf:
            paras.append(' '.join(buf))
        e['paras'] = paras
    return {'title': title, 'meta': meta, 'entries': entries}


CSS = """
:root{
  --ink:#2b2b2b; --soft:#38352f; --muted:#8a8172; --faint:#b9b0a0;
  --line:#e6dfd2; --gold:#bd9438; --bg:#faf7f1; --card:#ffffff;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Noto Sans TC","PingFang TC",-apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;
  font-weight:300; line-height:1.75;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
.mag{max-width:720px; margin:0 auto; padding:0 24px 120px;}

/* Cover */
.cover{padding:104px 0 40px; text-align:center;}
.cover .kicker{font-size:.72rem; letter-spacing:.42em; color:var(--gold); font-weight:400; margin-bottom:22px;}
.cover h1{font-size:2.4rem; font-weight:300; letter-spacing:.06em; line-height:1.4; margin:0 0 18px;}
.cover .sub{font-size:1rem; font-weight:300; color:var(--muted); letter-spacing:.08em; margin:0 0 10px;}
.cover .dates{font-size:.82rem; letter-spacing:.2em; color:var(--faint); margin:0 0 30px;}
.cover .quote{font-style:italic; font-weight:300; color:var(--soft); font-size:1.02rem;
  line-height:1.9; max-width:560px; margin:0 auto;}
.cover-rule{border:0; border-top:1px solid var(--line); margin:44px 0 0;}

/* Day chapter */
.day{padding-top:76px;}
.day-head{margin:0 0 30px;}
.day-no{font-size:.72rem; letter-spacing:.4em; color:var(--gold); font-weight:400;}
.day-title{font-size:1.6rem; font-weight:300; letter-spacing:.03em; line-height:1.5; margin:8px 0 0;}
.day-rule{border:0; border-top:2px solid var(--line); margin:18px 0 0;}

/* meta cards */
.meta{display:flex; flex-wrap:wrap; gap:12px; margin:26px 0 6px;}
.card{flex:1 1 190px; border:1px solid var(--line); border-radius:12px; padding:13px 17px; background:var(--card);}
.card .k{font-size:.66rem; letter-spacing:.3em; color:var(--gold); font-weight:400; margin-bottom:5px;}
.card .v{font-size:.92rem; font-weight:300; color:var(--soft);}

/* section kicker */
.kicker{font-size:.68rem; letter-spacing:.36em; color:var(--faint); font-weight:400;
  text-transform:uppercase; margin:52px 0 -8px;}

/* spot entry */
.spot{margin-top:44px;}
.spot h2{font-size:1.42rem; font-weight:300; letter-spacing:.03em; line-height:1.5; margin:0 0 12px; color:var(--ink);}
.spot .lead{font-style:italic; color:var(--muted); font-weight:300; font-size:1.05rem;
  line-height:1.7; margin:0 0 30px;}
.spot figure{margin:0 0 30px;}
.spot img{display:block; width:100%; height:auto; border-radius:10px;}
.spot p.body{font-size:1rem; font-weight:300; line-height:1.8; color:var(--soft); margin:0 0 14px;}
.spot p.note{font-size:.9rem; font-weight:300; line-height:1.8; color:var(--muted);
  border-left:2px solid var(--gold); padding-left:14px; margin:6px 0 0;}
hr.sep{border:0; border-top:1px solid var(--line); margin:58px 0 0;}

@media(max-width:600px){
  .mag{padding:0 18px 88px;}
  .cover{padding:72px 0 32px;} .cover h1{font-size:1.8rem;}
  .day{padding-top:56px;} .day-title{font-size:1.35rem;} .spot h2{font-size:1.25rem;}
}
"""


def render():
    trip = parse_front_matter(os.path.join(TRIP_DIR, 'trip.md'))
    day_files = sorted(f for f in os.listdir(TRIP_DIR)
                       if re.match(r'^day\d+\.md$', f, re.IGNORECASE))
    out = []
    out.append('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">')
    out.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    out.append('<title>%s ｜ 城市散步</title>' % esc(trip.get('title', 'BLDH Trio')))
    out.append('<style>%s</style></head><body><div class="mag">' % CSS)

    # Cover
    out.append('<header class="cover">')
    if trip.get('number'):
        out.append('<div class="kicker">%s</div>' % esc(trip['number']))
    out.append('<h1>%s</h1>' % esc(trip.get('title', '')))
    if trip.get('subtitle'):
        out.append('<p class="sub">%s</p>' % esc(trip['subtitle']))
    if trip.get('hero_quote'):
        out.append('<p class="quote">%s</p>' % esc(trip['hero_quote']))
    out.append('<hr class="cover-rule"></header>')

    for df in day_files:
        day = parse_day(os.path.join(TRIP_DIR, df))
        title = day['title']
        no = ''
        m = re.match(r'^(Day\s*\d+)', title)
        if m:
            no = m.group(1)
        rest = title[len(no):].lstrip('｜|').strip() if no else title
        out.append('<section class="day">')
        out.append('<div class="day-head">')
        if no:
            out.append('<div class="day-no">%s</div>' % esc(no.upper()))
        out.append('<h2 class="day-title">%s</h2>' % esc(rest))
        out.append('<hr class="day-rule"></div>')

        # meta cards
        cards = []
        for k, v in day['meta']:
            if not v:
                continue
            if k == 'meals':
                for part in [p for p in re.split(r'／|/', v) if p.strip()]:
                    if '：' in part:
                        lab, desc = part.split('：', 1)
                    elif ':' in part:
                        lab, desc = part.split(':', 1)
                    else:
                        lab, desc = part, ''
                    lab = {'午': '午餐', '晚': '晚餐'}.get(lab.strip(), lab.strip())
                    cards.append((lab, desc.strip()))
            else:
                cards.append((META_LABELS.get(k, k), v))
        if cards:
            out.append('<div class="meta">')
            for lab, val in cards:
                out.append('<div class="card"><div class="k">%s</div><div class="v">%s</div></div>'
                           % (esc(lab), esc(val)))
            out.append('</div>')

        last_section = None
        for e in day['entries']:
            if e['section'] and e['section'] != last_section:
                out.append('<div class="kicker">%s</div>' % esc(e['section']))
                last_section = e['section']
            paras = e['paras']
            lead, first_rest = ('', '')
            if paras:
                lead, first_rest = split_lead(paras[0])
            out.append('<article class="spot">')
            out.append('<h2>%s</h2>' % esc(e['name']))
            if lead:
                out.append('<p class="lead">%s</p>' % esc(lead))
            if e['img']:
                out.append('<figure><img src="../../photos/bldh-trio/%s" alt="%s"></figure>'
                           % (esc(e['img']), esc(e['alt'])))
            if first_rest:
                out.append('<p class="body">%s</p>' % esc(first_rest))
            for extra in paras[1:]:
                cls = 'note' if extra.lstrip().startswith('✦') else 'body'
                out.append('<p class="%s">%s</p>' % (cls, esc(extra)))
            out.append('</article>')
            out.append('<hr class="sep">')
        out.append('</section>')

    out.append('</div></body></html>')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    return day_files


if __name__ == '__main__':
    dfs = render()
    print('days:', len(dfs), '->', os.path.relpath(OUT, ROOT))
