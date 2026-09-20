"""Shared configuration: the data window, the lab classification, and the palette.

THE SNAPSHOT WINDOW
-------------------
FROM/TO pin the charts to a fixed 90-day period so the committed PNGs and SVGs are
reproducible forever. This window matches the original @rauchg token-volume chart
(Jun 21 - Sep 18, 2026) so the two are directly comparable.

To extend the charts to more recent data:
  1. Widen the window below, e.g. TO = '2026-12-31'. The build scripts read these
     constants; nothing else needs to change.
  2. Re-run `python3 scripts/fetch.py` to pull a snapshot that covers the new range
     (fetch.py reads SNAPSHOT_FROM/SNAPSHOT_TO, not FROM/TO, and already pulls the
     full available history).
  3. Re-run the build scripts.

The full committed snapshot already runs 2025-10-01 -> 2026-09-19, so widening FROM
backwards to 2025-10-01 needs no re-fetch at all. 2025-10-01 is the earliest date the
export endpoint serves; an earlier `from` returns HTTP 400.

Note that bar width is computed from the day count, so a much longer window will
produce thinner bars; adjust BAR_FILL in the build scripts if it gets too dense.
"""

# --- chart window (what the committed charts show) ---------------------------
FROM, TO = '2026-06-21', '2026-09-18'

# --- snapshot window (what fetch.py downloads) -------------------------------
# Deliberately wider than FROM/TO so the window can be opened up without re-fetching.
SNAPSHOT_FROM, SNAPSHOT_TO = '2025-10-01', '2026-09-19'

REPO_URL = 'github.com/jeremiahdillon/vercel-open-vs-closed-spend'

# Two lines, carried on the face of every chart.
# Line 1 is Vercel's prescribed CC BY 4.0 notice, scoped explicitly to the DATA so the
# copyright is not read as covering the chart. The license URL is included because the
# PNG travels on its own, where the README's hyperlink is unavailable.
# Line 2 claims authorship of the chart and forecloses the endorsement reading — the
# styling here deliberately mirrors Vercel's, and CC BY 4.0 forbids implying sponsorship.
ATTRIBUTION = (
    'Data: "AI Gateway Leaderboard Data" © 2026 Vercel · CC BY 4.0 · creativecommons.org/licenses/by/4.0',
    'Chart by Jeremiah Dillon · Independent analysis, not affiliated with or endorsed by Vercel',
)

# --- open-weight classification ----------------------------------------------
# Labs whose flagship models publish weights for download. This is necessarily
# LAB-level: the public export has no per-model license field over full history, so
# a lab is assigned wholesale. Known imprecision: Alibaba publishes most Qwen weights
# but Qwen-Max is proprietary; OpenAI has gpt-oss; Google has Gemma. See README.
OPEN = {
    'deepseek', 'meta', 'alibaba', 'moonshotai', 'zai', 'minimax', 'stepfun',
    'tencent', 'bytedance', 'xiaomi', 'inclusionai', 'arcee-ai', 'nvidia',
    'mistral', 'sakana', 'mixedbread',
}

# --- palette ------------------------------------------------------------------
# Blue and the base yellow are sampled pixel-exact from the original chart image.
# The two darker yellows extend that hue into a ramp; the set is validated for
# colour-vision separation and contrast (see README).
BLUE = '#0D59E0'
ANTH, OAI, OTHC = '#FDB103', '#C98200', '#8A5A00'
YELLOW = ANTH

PLOT_BG, CARD_BG = '#000000', '#0C0C0C'
INK, MUTED, DIM, STAMP = '#FFFFFF', '#A1A1A1', '#6E6E6E', '#8F8F8F'
SANS = 'Inter, Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, Menlo, monospace'
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def fmt_date(iso):
    y, m, d = iso.split('-')
    return f'{MONTHS[int(m)-1]} {int(d)}, {y}'
