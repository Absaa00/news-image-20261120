#!/usr/bin/env python3
"""news-image-20261120 — sum up the world's news of Friday 20 November 2026.

The entry image is drawn by gen_image.py (Pillow, offline) from real news
reported on 20 November 2026 and stored in this repository as entry.png:

  * Trump, Xi and Putin hold the first-ever trilateral summit in China
  * GTA VI launches to a 99 Metacritic score, $1.84bn on day one
  * Cyclone Akvan bears down on India's Odisha coast, 80,000 evacuated
  * ICJ rules Myanmar 'likely' intended to destroy part of the Rohingya
  * Anthropic reportedly valued at $1.5 trillion
  * Ukraine hits the Crimean Bridge, disrupting the rail link

This program (standard library only) copies entry.png to /output/entry.png
and verifies its SHA-256, so two runs write byte-identical output.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "83e7cced39cc4a78ccd50756aa39542a261e2f007f498ed6c379a939357e3980"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("entry.png sha256 mismatch: got %s" % digest, file=sys.stderr)
        return 1
    with open(dst, "wb") as fh:
        fh.write(data)
    shutil.copystat(src, dst)
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
