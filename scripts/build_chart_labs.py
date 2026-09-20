#!/usr/bin/env python3
"""Chart 2 — Open vs. Closed Model Spend, closed split by lab (four series).

Input : data/raw/labs-all-*.json   (from scripts/fetch.py)
Output: charts/2-open-vs-closed-spend-by-lab.svg

Identical to chart 1 except the closed bloc is split into Anthropic / OpenAI /
Other Closed across a single-hue yellow ramp, so it still reads as one group.
Stack order bottom -> top: Anthropic, OpenAI, Other Closed, Open Weights.

The chart window is fixed in scripts/window.py; see that file for how to extend it.
"""
import json, collections, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from window import (FROM, TO, OPEN, BLUE, ANTH, OAI, OTHC, PLOT_BG, CARD_BG, INK,
                    MUTED, DIM, STAMP, SANS, MONO, REPO_URL, ATTRIBUTION, fmt_date)

ROOT = Path(__file__).resolve().parent.parent
BAR_FILL = 0.78
GAP = 2

# bottom -> top
SEGS = [('Anthropic', ANTH), ('OpenAI', OAI), ('Other Closed', OTHC), ('Open Weights', BLUE)]


def load():
    src = sorted(ROOT.glob('data/raw/labs-all-*.json'))[-1]
    rows = json.loads(src.read_text())['rows']
    acc = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in rows:
        if r['metric'] != 'spend' or not (FROM <= r['date'] <= TO):
            continue
        n = r['name']
        key = ('Open Weights' if n in OPEN else 'Anthropic' if n == 'anthropic'
               else 'OpenAI' if n == 'openai' else 'Other Closed')
        acc[r['date']][key] += r['share_percent']
    out = []
    for d in sorted(acc):
        v = acc[d]; t = sum(v.values())
        if t:
            out.append((d, {k: 100 * v.get(k, 0.0) / t for k, _ in SEGS}))
    return out


def render(series):
    W, H = 1600, 1144
    L, R, T, B = 96, 1504, 300, 800
    pw, ph = R - L, B - T
    n = len(series); slot = pw / n; bw = slot * BAR_FILL

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{SANS}">']
    s.append(f'<rect width="{W}" height="{H}" rx="28" fill="{CARD_BG}"/>')
    s.append(f'<rect x="{L-40}" y="{T-140}" width="{pw+80}" height="{ph+464}" rx="18" fill="{PLOT_BG}"/>')

    s.append(f'<text x="{L}" y="{T-78}" font-size="40" font-weight="700" fill="{INK}">'
             f'Open vs. Closed Model Spend</text>')
    s.append(f'<text x="{L}" y="{T-40}" font-size="21" fill="{MUTED}">'
             f'Share of Vercel AI Gateway spend on models that publish their weights for '
             f'download, versus everything else — with closed weights split by lab.</text>')
    s.append(f'<text x="{R}" y="{T-110}" text-anchor="end" font-family="{MONO}" '
             f'font-size="20" fill="{STAMP}">{REPO_URL}</text>')

    for i, (d, v) in enumerate(series):
        x = L + i * slot + (slot - bw) / 2
        y = B
        for name, col in SEGS:
            h = ph * v[name] / 100
            y -= h
            s.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bw:.2f}" '
                     f'height="{max(h-GAP,0):.2f}" fill="{col}"/>')

    s.append(f'<text x="{L}" y="{B+40}" font-family="{MONO}" font-size="19" fill="{DIM}">'
             f'{fmt_date(series[0][0])}</text>')
    s.append(f'<text x="{R}" y="{B+40}" text-anchor="end" font-family="{MONO}" '
             f'font-size="19" fill="{DIM}">{fmt_date(series[-1][0])}</text>')

    last = series[-1][1]
    ly = B + 110
    for i, (name, col) in enumerate(SEGS):
        y = ly + i * 44
        s.append(f'<circle cx="{L+8}" cy="{y}" r="8" fill="{col}"/>')
        s.append(f'<text x="{L+30}" y="{y+7}" font-size="21" fill="{INK}">{name}</text>')
        s.append(f'<text x="{R}" y="{y+7}" text-anchor="end" font-family="{MONO}" '
                 f'font-size="21" fill="{INK}">{last[name]:.1f}%</text>')

    for i, line in enumerate(ATTRIBUTION):
        s.append(f'<text x="{L}" y="{H-54+i*24}" font-family="{MONO}" font-size="16" '
                 f'fill="{DIM}">{line}</text>')
    s.append('</svg>')
    return '\n'.join(s)


if __name__ == '__main__':
    series = load()
    out = ROOT / 'charts' / '2-open-vs-closed-spend-by-lab.svg'
    out.parent.mkdir(exist_ok=True)
    out.write_text(render(series))
    last = series[-1][1]
    print(f'{len(series)} days  {series[0][0]} -> {series[-1][0]}')
    print('last day: ' + '  '.join(f'{k}={last[k]:.1f}%' for k, _ in SEGS))
    for k, _ in SEGS:
        m = sum(x[1][k] for x in series) / len(series)
        print(f'  window mean {k:14} {m:5.1f}%')
    print(f'wrote {out}')
