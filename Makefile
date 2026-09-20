# Build everything from the committed snapshot. No API key required.
.PHONY: all charts png fetch clean

all: charts png

charts:
	python3 scripts/build_chart.py
	python3 scripts/build_chart_labs.py

png: charts
	bash scripts/render_png.sh

# Re-pull the snapshot from Vercel's public export endpoint (optional).
# Widen SNAPSHOT_FROM/SNAPSHOT_TO in scripts/window.py first to get newer data.
fetch:
	python3 scripts/fetch.py

clean:
	rm -f charts/*.svg charts/*.png
