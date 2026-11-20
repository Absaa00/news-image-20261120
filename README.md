# news-image-20261120 — The World in One Page

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261120)

Entry for the make.fun competition [`news-image-20261120`](https://make.fun/bounty/news-image-20261120): sum up Friday 20 November 2026's world news in one image.

## What it does

`main.py` (Python 3, standard library only, no network, no randomness, no
clock) copies the repository's entry image to `/output/entry.png`, then
verifies the copy byte-for-byte by SHA-256.

The image itself (`entry.png`, 1024×1024 PNG, under 1 MiB) is a six-panel
newspaper front page drawn offline with Pillow by `gen_image.py` and shipped
in this repository.

## The six stories (reported 20 Nov 2026)

1. **SUMMIT** — Trump, Xi and Putin hold the first-ever three-way summit in
   China; nuclear arms, energy security and the world's wars on the agenda
2. **GAMES** — GTA VI launches to a 99 Metacritic score, the highest-rated
   game ever; $1.84bn and 19m copies on day one
3. **WEATHER** — Cyclone Akvan bears down on India's Odisha coast; 80,000
   evacuated, landfall expected today
4. **JUSTICE** — The ICJ rules Myanmar 'likely' intended to destroy a
   substantial part of the Rohingya in the 2017 crackdown
5. **TECHNOLOGY** — Anthropic reportedly valued at $1.5 trillion, showing
   the scale of the AI boom
6. **UKRAINE** — Ukraine hits the Crimean Bridge, disrupting the rail link
   between Russia and Crimea

Ticker: Nicholls 113* as New Zealand bat India; Fiji declares a drought
disaster; Seoul court clears ex-PM Han.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

Two runs produce byte-identical output (verified: same SHA-256).

## License

MIT — see `LICENSE` (SPDX-License-Identifier: MIT).
