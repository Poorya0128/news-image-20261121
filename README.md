[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday Finale: Saturday 21 November 2026

An entry for make.fun's one-day world news image contest ([news-image-20261121](https://make.fun/bounty/news-image-20261121)).

One 1024×1024 newspaper front page summing up Saturday 21 November 2026: 35 stories across 8 regions — tankers hit off Oman and Iran's Bahrain-strike claim, COP31 running into overtime, Mexico seizing FBI-listed 'El Chapo Isidro', the M6.7 Peru quake, the Basra power plant fire, the Indonesia–EU trade pact, Taiwan curbing short-selling, Bitcoin's rebound, England routing the All Blacks 37-12 — plus a UTC timeline and world-in-numbers rows, a world map with numbered story pins, 22 numbered briefs, and a Date Check box of older news left out.

- `main.py` copies the committed `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Standard library only. It verifies the image (real PNG, 1024×1024, within 1 MiB) before shipping it, and reads the delivered file back to confirm the copy is byte-identical.
- `entry.png` is the finished front page itself, drawn with Pillow: the three lead cards, ten small cards, timeline, world-in-numbers rows, world map and numbered briefs.
- `data/land.json` holds the simplified map outlines.
- `fonts/` holds Newsreader, Source Serif 4, Inter and Barlow Condensed, all under the SIL Open Font License 1.1.

Every illustration on the page is an original Pillow drawing. No photos, no network calls at build time.

Code is under the MIT License (see `LICENSE`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=yp1rdj4t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
