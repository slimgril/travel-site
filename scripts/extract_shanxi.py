#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
#  一次性提取脚本：把 reference/shanxi-golden.html 的内容
#  确定性地抽取成 content/shanxi/ 下的 markdown 原稿。
#
#  目的：避免手工转写造成改字。机器提取 = 文字 100% 一致。
#  运行：python3 scripts/extract_shanxi.py
#  运行后产出 content/shanxi/trip.md + day01.md..day15.md，本脚本即可弃用。
# ============================================================================

import os
import re
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN = os.path.join(ROOT, 'reference', 'shanxi-golden.html')
OUT = os.path.join(ROOT, 'content', 'shanxi')


def md_inline(s):
    """HTML 内联 → markdown：<strong>→**，<br>→空格，去其余标签，反转义实体。"""
    if s is None:
        return ''
    s = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)          # 去掉残余标签（如 lv-label span）
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def img_name(src):
    """丫斌哥山西遊記/photos/02_太原晨景.jpg → 02_太原晨景.jpg；img-*.jpg（不存在）→ None"""
    base = src.split('/')[-1]
    if base.startswith('img-'):
        return None
    return base


def grab(pat, text, flags=re.S):
    m = re.search(pat, text, flags)
    return m.group(1) if m else None


def extract_sites(section):
    """返回 [(name, desc, img_or_None)]"""
    out = []
    for m in re.finditer(
        r"background-image:url\('([^']+)'\).*?"
        r'<div class="site-name">(.*?)</div>\s*'
        r'<div class="site-desc">(.*?)</div>', section, re.S):
        src, name, desc = m.group(1), md_inline(m.group(2)), md_inline(m.group(3))
        out.append((name, desc, img_name(src)))
    return out


def extract_history(section):
    """返回 (h3, items)；items 为 [('p'|'quote'|'tip'|'raw', content)]，保持顺序。"""
    start = section.find('<div class="history-panel">')
    if start == -1:
        return None, []
    after = section[start:]
    end = after.find('<div class="live-dispatch">')
    if end == -1:
        end = after.find('</section>')
    block = after[:end]
    inner = block[len('<div class="history-panel">'): block.rstrip().rfind('</div>')]

    h3 = md_inline(grab(r'<h3>(.*?)</h3>', inner))
    rest = inner[inner.find('</h3>') + 5:] if '</h3>' in inner else inner

    # Day15 内嵌时间轴 div → raw 保留
    raw_html = None
    tl = rest.find('<div style="margin-top:20px')
    if tl != -1:
        raw_html = rest[tl:].rstrip()
        rest = rest[:tl]

    items = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>|<div class="extra-tip">(.*?)</div>', rest, re.S):
        if m.group(2) is not None:           # <p>
            style, content = m.group(1), md_inline(m.group(2))
            if not content:
                continue
            if 'border-left' in style or 'color:#888' in style:
                items.append(('quote', content))
            else:
                items.append(('p', content))
        elif m.group(3) is not None:          # extra-tip
            items.append(('tip', md_inline(m.group(3))))
    if raw_html:
        items.append(('raw', raw_html.strip()))
    return h3, items


def extract_live(section):
    """返回 (date_override, [card])；card = dict(time, tag, feature, img, descs[], quote)"""
    start = section.find('<div class="live-dispatch">')
    if start == -1:
        return None, []
    inner = section[start:]
    date_override = md_inline(grab(r'<span class="live-date">(.*?)</span>', inner))

    cards = []
    chunks = inner.split('<div class="live-card')
    for ch in chunks[1:]:
        feature = ch[:60].find(' live-feature') != -1 or ch[:60].find('live-feature') != -1
        img = grab(r'<img class="live-img" src="([^"]+)"', ch)
        img = img_name(img) if img else None

        time_block = grab(r'<div class="live-time">(.*?)</div>', ch)
        caption = grab(r'<div class="live-caption">(.*?)</div>', ch)

        if time_block is not None:
            tag = grab(r'<span class="live-tag">(.*?)</span>', time_block)
            time_text = md_inline(re.sub(r'<span class="live-tag">.*?</span>', '', time_block, flags=re.S))
            descs = [md_inline(d) for d in re.findall(r'<div class="live-desc">(.*?)</div>', ch, re.S)]
            quote = grab(r'<blockquote>(.*?)</blockquote>', ch)
            quote = md_inline(quote) if quote else None
            cards.append({'time': time_text, 'tag': tag, 'feature': feature,
                          'img': img, 'descs': descs, 'quote': quote})
        elif caption is not None:             # Day11 旧结构
            cards.append({'time': '', 'tag': None, 'feature': feature,
                          'img': img, 'descs': [md_inline(caption)], 'quote': None})

    # Day11 独立 feature-text（背水一战）
    ft = grab(r'<div class="feature-text">(.*?)</div>', inner)
    if ft:
        cards.append({'time': '', 'tag': None, 'feature': True,
                      'img': None, 'descs': [md_inline(ft)], 'quote': None})
    return date_override, cards


def day_md(section):
    num = grab(r'<div class="num">(\d+)</div>', section)
    date = md_inline(grab(r'<div class="date">(.*?)</div>', section))
    h2 = md_inline(grab(r'<h2>(.*?)</h2>', section))
    route = md_inline(grab(r'<div class="route">(.*?)</div>', section))
    acc = md_inline(grab(r'<div class="acc-name">(.*?)</div>', section))

    lines = []
    # H1：Day N ｜ 日期 ｜ 路线 — 标题
    h1 = 'Day %s ｜ %s ｜ %s — %s' % (num, date, route, h2)
    lines.append('# ' + h1)
    if acc:
        lines.append(':::meta lodging=%s' % acc)
    lines.append('')

    sites = extract_sites(section)
    if sites:
        lines.append('## 古蹟')
        for name, desc, img in sites:
            head = '### ' + name
            if img:
                head += ' ![](%s)' % img
            lines.append(head)
            if desc:
                lines.append(desc)
            lines.append('')

    h3, items = extract_history(section)
    if h3 is not None:
        lines.append('## 歷史')
        lines.append('### ' + h3)
        for kind, content in items:
            if kind == 'p':
                lines.append(content)
                lines.append('')
            elif kind == 'quote':
                lines.append('> ' + content)
                lines.append('')
            elif kind == 'tip':
                lines.append('✦ ' + content)
                lines.append('')
            elif kind == 'raw':
                lines.append(':::raw')
                lines.append(content)
                lines.append(':::')
                lines.append('')

    date_override, cards = extract_live(section)
    if cards:
        lines.append('## 現場')
        if date_override:
            lines.append(date_override)
        for c in cards:
            head = '### '
            parts = []
            if c['time']:
                parts.append(c['time'])
            if c['tag']:
                parts.append('{tag:%s}' % c['tag'])
            elif c['feature']:
                parts.append('{feature}')
            head += ' '.join(parts)
            if c['img']:
                head += ' ![](%s)' % c['img']
            lines.append(head.rstrip())
            for d in c['descs']:
                if d:
                    lines.append(d)
                    lines.append('')
            if c['quote']:
                lines.append('> ' + c['quote'])
                lines.append('')

    # 收尾：折叠多余空行
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return num, text.strip() + '\n'


def main():
    with open(GOLDEN, encoding='utf-8') as f:
        doc = f.read()

    sections = re.findall(r'<section class="day-section.*?</section>', doc, re.S)
    os.makedirs(OUT, exist_ok=True)

    # trip.md（旅程元数据）
    trip = '''---
slug: shanxi
number: World Journey #001
title: 山西漫遊 {15} 日
subtitle: 2026年6月10日 — 6月24日　深度文化歷史之旅
traveler: 丫斌哥
status: done
date_start: 2026-06-10
date_end: 2026-06-24
hero_badge: 深度文化歷史之旅
hero_quote: 用餘生走遍天下，用雙腳丈量世界，用心去感受每一片土地的呼吸。
summary: 從雲岡石窟、五台山、平遙古城到壺口瀑布與晉祠，用腳步閱讀山西 2700 年文明。
tags: [中國, 山西]
stats:
  - { num: "15", label: 天 }
  - { num: "12", label: 座城市 }
  - { num: "30+", label: 歷史古蹟 }
  - { num: "2700", label: 年文明縱深 }
---
'''
    with open(os.path.join(OUT, 'trip.md'), 'w', encoding='utf-8') as f:
        f.write(trip)

    count = 0
    for sec in sections:
        num, text = day_md(sec)
        fname = 'day%02d.md' % int(num)
        with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
        print('  ✓ %s (Day %s)' % (fname, num))
    print('共提取 %d 天 → content/shanxi/' % count)


if __name__ == '__main__':
    main()
