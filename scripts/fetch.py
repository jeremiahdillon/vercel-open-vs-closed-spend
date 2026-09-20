#!/usr/bin/env python3
"""Download the Vercel AI Gateway leaderboard snapshot.

No API key, no account, no auth header — the export endpoint is public and the data
is CC BY 4.0. Re-running this overwrites data/raw/ with a fresh pull.

  python3 scripts/fetch.py

The snapshot window is SNAPSHOT_FROM/SNAPSHOT_TO in scripts/window.py, currently
2025-10-01 -> 2026-09-19. 2025-10-01 is the earliest date the endpoint serves (the
point from which Vercel's daily rollups are complete); an earlier `from` returns 400.

To pull data newer than the committed snapshot, raise SNAPSHOT_TO in window.py and
re-run. Note the endpoint caches for 24 hours, so the last day or two may shift.
"""
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from window import SNAPSHOT_FROM, SNAPSHOT_TO  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'data' / 'raw'
ENDPOINT = 'https://vercel.com/api/ai/leaderboard-export'


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    url = (f'{ENDPOINT}?dataset=labs&modality=all'
           f'&from={SNAPSHOT_FROM}&to={SNAPSHOT_TO}')
    dest = RAW / f'labs-all-{SNAPSHOT_FROM}_{SNAPSHOT_TO}.json'
    print(f'GET {url}')
    with urllib.request.urlopen(url, timeout=60) as r:
        body = r.read()
    dest.write_bytes(body)
    print(f'wrote {dest}  ({len(body):,} bytes)')


if __name__ == '__main__':
    main()
