#!/usr/bin/env bash
# Rasterize the SVG charts to PNG with headless Chrome.
#
# SVG is the primary, reproducible artifact — it is generated deterministically from
# the committed JSON. PNG output is NOT guaranteed byte-identical across Chrome
# versions or platforms, so treat these as a convenience render, not a build target
# to diff against.
#
# Any SVG rasterizer works; these are equivalent:
#   rsvg-convert -w 1600 charts/1-open-vs-closed-spend.svg -o out.png
#   cairosvg charts/1-open-vs-closed-spend.svg -o out.png
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at: $CHROME" >&2
  echo "Set CHROME=/path/to/chrome, or use rsvg-convert/cairosvg (see header)." >&2
  exit 1
fi

render() {  # render <svg-basename> <width> <height>
  "$CHROME" --headless --disable-gpu \
    --screenshot="charts/$1.png" --window-size="$2,$3" \
    "file://$PWD/charts/$1.svg" 2>/dev/null
  echo "charts/$1.png"
}

render 1-open-vs-closed-spend        1600 1064
render 2-open-vs-closed-spend-by-lab 1600 1144
