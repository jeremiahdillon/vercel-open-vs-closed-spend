#!/usr/bin/env python3
"""Chart 1 — Open vs. Closed Model Spend (two series).

Input : data/raw/labs-all-*.json   (from scripts/fetch.py)
Output: charts/1-open-vs-closed-spend.svg

The chart window is fixed in scripts/window.py; see that file for how to extend it
to more recent data. Pure standard library; hand-written SVG.
"""
import json, collections, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from window import (FROM, TO, OPEN, BLUE, YELLOW, PLOT_BG, INK, MUTED,
                    DIM, STAMP, SANS, MONO, REPO_URL, ATTRIBUTION, fmt_date)

ROOT = Path(__file__).resolve().parent.parent
BAR_FILL = 0.78          # bar width as a fraction of its slot
GAP = 2                  # surface gap between stacked fills, px


def load():
    src = sorted(ROOT.glob('data/raw/labs-all-*.json'))[-1]
    rows = json.loads(src.read_text())['rows']
    acc = collections.defaultdict(float)
    for r in rows:
        if r['metric'] == 'spend' and FROM <= r['date'] <= TO:
            acc[(r['date'], r['name'] in OPEN)] += r['share_percent']
    out = []
    for d in sorted({d for d, _ in acc}):
        o, c = acc.get((d, True), 0.0), acc.get((d, False), 0.0)
        t = o + c
        if t:
            out.append((d, 100 * o / t, 100 * c / t))
    return out


def render(series):
    W, H = 1600, 990
    L, R, T, B = 96, 1504, 210, 710
    pw, ph = R - L, B - T
    n = len(series); slot = pw / n; bw = slot * BAR_FILL

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{SANS}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{PLOT_BG}"/>')

    s.append(f'<text x="{L}" y="{T-78}" font-size="40" font-weight="700" fill="{INK}">'
             f'Open vs. Closed Model Spend</text>')
    s.append(f'<text x="{L}" y="{T-40}" font-size="21" fill="{MUTED}">'
             f'Share of Vercel AI Gateway spend on models that publish their weights for '
             f'download, versus everything else.</text>')
    s.append(f'<text x="{R}" y="{T-110}" text-anchor="end" font-family="{MONO}" '
             f'font-size="20" fill="{STAMP}">{REPO_URL}</text>')

    for i, (d, o, c) in enumerate(series):
        x = L + i * slot + (slot - bw) / 2
        ho = ph * o / 100
        s.append(f'<rect x="{x:.2f}" y="{T:.2f}" width="{bw:.2f}" '
                 f'height="{max(ho-GAP,0):.2f}" fill="{BLUE}"/>')
        s.append(f'<rect x="{x:.2f}" y="{T+ho:.2f}" width="{bw:.2f}" '
                 f'height="{max(ph*c/100,0):.2f}" fill="{YELLOW}"/>')

    s.append(f'<text x="{L}" y="{B+40}" font-family="{MONO}" font-size="19" fill="{DIM}">'
             f'{fmt_date(series[0][0])}</text>')
    s.append(f'<text x="{R}" y="{B+40}" text-anchor="end" font-family="{MONO}" '
             f'font-size="19" fill="{DIM}">{fmt_date(series[-1][0])}</text>')

    # legend in stack order, bottom -> top (parallel to chart 2)
    lo, lc = series[-1][1], series[-1][2]
    ly = B + 110
    for i, (lab, col, val) in enumerate(
            [('Closed Weights', YELLOW, lc), ('Open Weights', BLUE, lo)]):
        y = ly + i * 44
        s.append(f'<circle cx="{L+8}" cy="{y}" r="8" fill="{col}"/>')
        s.append(f'<text x="{L+30}" y="{y+7}" font-size="21" fill="{INK}">{lab}</text>')
        s.append(f'<text x="{R}" y="{y+7}" text-anchor="end" font-family="{MONO}" '
                 f'font-size="21" fill="{INK}">{val:.1f}%</text>')

    for i, line in enumerate(ATTRIBUTION):
        s.append(f'<text x="{L}" y="{H-66+i*24}" font-family="{MONO}" font-size="16" '
                 f'fill="{DIM}">{line}</text>')
    s.append('</svg>')
    return '\n'.join(s)


if __name__ == '__main__':
    series = load()
    out = ROOT / 'charts' / '1-open-vs-closed-spend.svg'
    out.parent.mkdir(exist_ok=True)
    out.write_text(render(series))
    print(f'{len(series)} days  {series[0][0]} -> {series[-1][0]}')
    print(f'last day: open={series[-1][1]:.1f}%  closed={series[-1][2]:.1f}%')
    print(f'wrote {out}')
