#!/usr/bin/env python3
"""Draw the front page of 'The World Today' for Friday 20 November 2026.

One 1024x1024 PNG summing up the day's world news, drawn offline with
Pillow. Six real stories, researched from news reports of 20 Nov 2026:

  1. Trump, Xi and Putin hold the first-ever trilateral summit in China
  2. GTA VI launches to a 99 Metacritic score, $1.84bn on day one
  3. Cyclone Akvan bears down on India's Odisha coast, 80,000 evacuated
  4. ICJ rules Myanmar 'likely' intended to destroy part of the Rohingya
  5. Anthropic reportedly valued at $1.5 trillion
  6. Ukraine hits the Crimean Bridge, disrupting the rail link

Run: python3 gen_image.py  ->  writes entry.png next to this script.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
PANEL = (255, 253, 247)
INK = (22, 21, 19)
MUTED = (91, 86, 74)
RULE = (201, 192, 168)
RED = (166, 30, 30)
BLUE = (29, 78, 160)
TEAL = (14, 116, 144)
ORANGE = (194, 65, 12)
PURPLE = (124, 58, 237)
SLATE = (51, 65, 85)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, fill=INK, leading=1.28):
    """Draw wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def headline(draw, x, y, max_w, text, fnt, fill=INK, leading=1.05):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, text, color):
    fnt = font(SANS_B, 15)
    w = int(draw.textlength(text, font=fnt)) + 16
    draw.rectangle([x, y, x + w, y + 22], fill=color)
    draw.text((x + 8, y + 3), text, font=fnt, fill=(255, 255, 255))
    return w


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=RULE, width=1)
    draw.rectangle([x, y, x + w, y + 3], fill=INK)


def draw_us_flag(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=col)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            sx = x + 4 + c * (cw - 8) / 5
            sy = y + 4 + r * (ch - 8) / 4
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))


def draw_cn_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.18, y + h * 0.22, h * 0.16, (255, 222, 0))
    for sx, sy in [(0.42, 0.10), (0.52, 0.22), (0.52, 0.38), (0.42, 0.48)]:
        star(draw, x + w * sx, y + h * sy, h * 0.06, (255, 222, 0))


def draw_ru_flag(draw, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(186, 219, 240),
                 outline=BLUE, width=3)
    for k in range(-2, 3):
        rx = r * abs(k) / 3.0
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=(255, 255, 255), width=2)
    for k in (-0.55, 0.0, 0.55):
        yy = cy + r * k
        half = math.sqrt(max(r * r - (r * k) ** 2, 0))
        draw.arc([cx - half, yy - half * 0.45, cx + half, yy + half * 0.45],
                 start=180, end=360, fill=(255, 255, 255), width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=360, fill=BLUE, width=3)


def draw_cyclone(draw, cx, cy, r):
    for turn in range(5):
        rr = r * (0.25 + 0.19 * turn)
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                 start=turn * 55, end=turn * 55 + 300, fill=TEAL, width=7)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=TEAL)


def draw_scales(draw, cx, y, h, color):
    top = y
    base = y + h
    draw.line([cx, top, cx, base - 14], fill=color, width=4)
    draw.line([cx - 52, top + 12, cx + 52, top + 12], fill=color, width=4)
    draw.line([cx - 8, base - 14, cx + 8, base - 14], fill=color, width=4)
    draw.line([cx - 34, base, cx + 34, base], fill=color, width=4)
    for sx in (cx - 52, cx + 52):
        draw.line([sx, top + 12, sx - 16, top + 44], fill=color, width=2)
        draw.line([sx, top + 12, sx + 16, top + 44], fill=color, width=2)
        draw.arc([sx - 20, top + 30, sx + 20, top + 58], start=0, end=180,
                 fill=color, width=3)
    draw.ellipse([cx - 5, top - 5, cx + 5, top + 5], fill=color)


def draw_chip(draw, cx, cy, s, color):
    half = s // 2
    draw.rounded_rectangle([cx - half, cy - half, cx + half, cy + half],
                           radius=10, fill=color, outline=INK, width=2)
    draw.rounded_rectangle([cx - half + 14, cy - half + 14,
                            cx + half - 14, cy + half - 14],
                           radius=5, outline=(255, 255, 255), width=2)
    for i in range(3):
        off = -s // 4 + i * s // 4
        draw.line([cx + off, cy - half - 8, cx + off, cy - half], fill=INK, width=3)
        draw.line([cx + off, cy + half, cx + off, cy + half + 8], fill=INK, width=3)
        draw.line([cx - half - 8, cy + off, cx - half, cy + off], fill=INK, width=3)
        draw.line([cx + half, cy + off, cx + half + 8, cy + off], fill=INK, width=3)
    fnt = font(SANS_B, max(16, s // 2 - 2))
    tw = draw.textlength("AI", font=fnt)
    draw.text((cx - tw / 2, cy - fnt.size // 2), "AI", font=fnt, fill=(255, 255, 255))


def draw_bridge(draw, x, y, w, h, color):
    """Small suspension bridge with a blast star above the deck."""
    deck = y + h * 0.62
    t1, t2 = x + w * 0.20, x + w * 0.80
    for tx in (t1, t2):
        draw.line([tx, y + 6, tx, deck], fill=color, width=4)
    draw.line([x + 4, deck, x + w - 4, deck], fill=color, width=4)
    # suspension cables: tower top to deck quarter points
    draw.line([t1, y + 6, x + w * 0.5, deck], fill=color, width=2)
    draw.line([t2, y + 6, x + w * 0.5, deck], fill=color, width=2)
    draw.line([t1, y + 6, x + 4, deck], fill=color, width=2)
    draw.line([t2, y + 6, x + w - 4, deck], fill=color, width=2)
    for i in range(6):
        wx = x + 8 + i * (w - 16) / 5
        draw.arc([wx - 18, deck + 8, wx + 18, deck + 26], start=0, end=180,
                 fill=(90, 140, 190), width=2)
    star(draw, x + w / 2, y + h * 0.22, 15, (245, 158, 11))
    star(draw, x + w / 2, y + h * 0.22, 7, (220, 38, 38))


def draw_sunset(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(253, 224, 171))
    cx, cy = x + w // 2, y + h * 0.52
    draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=(249, 115, 22))
    draw.rectangle([x, cy + 30, x + w, y + h], fill=(40, 20, 60))
    heights = [0.42, 0.62, 0.34, 0.55, 0.46, 0.70, 0.38]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 2
        by = cy + 30 - hh * 70
        draw.rectangle([bx, by, bx + bw - 4, cy + 30], fill=(24, 12, 40))
    # palm fronds
    px, py = x + w - 26, cy + 28
    for ang in (-160, -130, -100, -70, -40):
        rad = math.radians(ang)
        ex, ey = px + 34 * math.cos(rad), py + 26 * math.sin(rad)
        draw.line([px, py, ex, ey], fill=(24, 12, 40), width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([24, 18, 1000, 18], fill=INK, width=3)
    mast = font(SERIF, 62)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=mast)) / 2, 26), t, font=mast, fill=INK)
    d.line([24, 102, 1000, 102], fill=INK, width=2)
    d.line([24, 106, 1000, 106], fill=INK, width=1)
    small = font(SANS_B, 19)
    d.text((24, 116), "FRIDAY, 20 NOVEMBER 2026", font=small, fill=RED)
    right = "WORLD EDITION  •  ONE DAY, ONE PAGE"
    d.text((1000 - d.textlength(right, font=small), 116), right, font=small, fill=INK)

    # ---------- lead story: trilateral summit ----------
    ly, lh = 150, 252
    panel(d, 24, ly, 976, lh)
    kicker(d, 40, ly + 14, "SUMMIT IN CHINA", RED)
    y = headline(d, 40, ly + 48, 600, "THREE POWERS, ONE TABLE",
                 font(SERIF, 38))
    y = para(d, 40, y + 10, 600,
             "Trump, Xi and Putin hold the first-ever three-way summit "
             "in China \u2014 nuclear arms, energy security and the "
             "world\u2019s wars on the agenda.",
             font(SANS, 18), leading=1.32)
    d.text((40, ly + lh - 32), "APEC, SHENZHEN  •  A FIRST IN HISTORY",
           font=font(SANS_B, 14), fill=MUTED)
    # illustration: globe + three flags
    draw_globe(d, 830, ly + 96, 74)
    fw, fh = 84, 52
    draw_us_flag(d, 716, ly + 178, fw, fh)
    draw_cn_flag(d, 808, ly + 178, fw, fh)
    draw_ru_flag(d, 900, ly + 178, fw, fh)
    d.text((716, ly + 234), "USA  •  CHINA  •  RUSSIA",
           font=font(SANS_B, 13), fill=MUTED)

    # ---------- row 2: GTA VI + Cyclone Akvan ----------
    ry, rh = 414, 272
    # GTA VI (left)
    panel(d, 24, ry, 478, rh)
    kicker(d, 40, ry + 14, "GAMES", PURPLE)
    headline(d, 40, ry + 46, 446, "GTA VI SCORES 99", font(SERIF, 34))
    draw_sunset(d, 40, ry + 100, 210, 96)
    badge = font(SERIF, 52)
    d.rounded_rectangle([268, ry + 100, 344, ry + 166], radius=10, fill=PURPLE)
    d.text((306 - d.textlength("99", font=badge) / 2, ry + 106), "99",
           font=badge, fill=(255, 255, 255))
    d.text((268, ry + 172), "ON METACRITIC", font=font(SANS_B, 13), fill=MUTED)
    para(d, 40, ry + 208, 446,
         "Rockstar\u2019s epic launches to near-perfect reviews \u2014 the "
         "highest-rated game ever; $1.84bn and 19m copies on day one.",
         font(SANS, 16), leading=1.3)
    # Cyclone Akvan (right)
    panel(d, 522, ry, 478, rh)
    kicker(d, 538, ry + 14, "WEATHER", TEAL)
    headline(d, 538, ry + 46, 300, "CYCLONE AKVAN NEARS INDIA",
             font(SERIF, 30))
    draw_cyclone(d, 918, ry + 98, 50)
    para(d, 538, ry + 158, 446,
         "80,000 evacuated as the severe storm bears down on the "
         "Odisha coast; schools shut, landfall expected today.",
         font(SANS, 16), leading=1.3)

    # ---------- row 3: ICJ + Anthropic + Crimea bridge ----------
    by, bh = 698, 250
    cols = [(24, 312), (352, 312), (680, 320)]
    # ICJ Myanmar
    x, w = cols[0]
    panel(d, x, by, w, bh)
    kicker(d, x + 14, by + 12, "ICJ RULING", SLATE)
    headline(d, x + 14, by + 42, w - 28,
             "MYANMAR \u2018LIKELY\u2019 SOUGHT ROHINGYA DESTRUCTION",
             font(SERIF, 22))
    draw_scales(d, x + w // 2, by + 128, 52, SLATE)
    para(d, x + 14, by + 190, w - 28,
         "World court: the 2017 crackdown likely intended to destroy "
         "a substantial part of the Rohingya.",
         font(SANS, 15), leading=1.3)
    # Anthropic
    x, w = cols[1]
    panel(d, x, by, w, bh)
    kicker(d, x + 14, by + 12, "TECHNOLOGY", ORANGE)
    headline(d, x + 14, by + 42, w - 28,
             "ANTHROPIC \u2018WORTH $1.5 TRILLION\u2019",
             font(SERIF, 22))
    draw_chip(d, x + w // 2, by + 154, 52, ORANGE)
    para(d, x + 14, by + 190, w - 28,
         "The reported valuation shows the scale of the AI boom as the "
         "industry\u2019s biggest names keep climbing.",
         font(SANS, 15), leading=1.3)
    # Crimea bridge
    x, w = cols[2]
    panel(d, x, by, w, bh)
    kicker(d, x + 14, by + 12, "UKRAINE", RED)
    headline(d, x + 14, by + 42, w - 28, "UKRAINE HITS CRIMEA BRIDGE",
             font(SERIF, 22))
    draw_bridge(d, x + 14, by + 112, w - 28, 66, (90, 60, 50))
    para(d, x + 14, by + 190, w - 28,
         "Attack disrupts the rail link between Russia and Crimea.",
         font(SANS, 15), leading=1.3)

    # ---------- footer ticker ----------
    fy = 960
    d.rectangle([24, fy, 1000, fy + 40], fill=INK)
    tick = font(SANS_B, 15)
    line = ("ALSO TODAY:  NICHOLLS 113* AS NZ BAT INDIA  •  FIJI DROUGHT "
            "DISASTER  •  SEOUL CLEARS EX-PM HAN")
    tw = d.textlength(line, font=tick)
    d.text(((W - tw) / 2, fy + 11), line, font=tick, fill=(255, 255, 255))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
