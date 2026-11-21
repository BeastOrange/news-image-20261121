#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Saturday 21 November 2026.

Deterministic: fixed palette, fixed fonts, no randomness, no timestamps,
no network. Running it twice produces byte-identical PNG output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
SKY_TOP = (18, 32, 58)
SKY_BOT = (74, 96, 140)
GROUND = (52, 58, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rule(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_masthead(draw):
    title = font(SERIF, 76)
    draw.text((W // 2, 30), "THE WORLD TODAY", font=title, fill=INK,
              anchor="ma")
    rule(draw, 36, 988, 128, INK, 4)
    rule(draw, 36, 988, 134, INK, 1)
    small = font(SANS_B, 21)
    draw.text((W // 2, 144), "SATURDAY, 21 NOVEMBER 2026  |  ONE DAY, ONE IMAGE",
              font=small, fill=RED, anchor="ma")


LEAD_KICKER = "WAR IN EUROPE"
LEAD_HEAD = "MISSILES LAND IN POLAND"
LEAD_SUB = "Russian Kh-101 cruise missile comes down in the south-east"
LEAD_BODY = ("Two more objects fall nearby as Moscow mounts a huge "
             "overnight strike on Ukraine. PM Donald Tusk calls it an "
             "\u201cintentional provocation\u201d; NATO chief Mark Rutte "
             "a \u201cgrave violation\u201d.")


def draw_scene(draw, x0, y0, x1, y1):
    """Stylised night scene: sky, ground, three missile streaks, bursts."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY_TOP)
    bands = 24
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * t)
                    for c in range(3))
        yy = y0 + int((y1 - y0) * 0.72 * i / bands)
        draw.rectangle([x0, yy, x1, yy + 12], fill=col)
    gy = y0 + int((y1 - y0) * 0.72)
    draw.rectangle([x0, gy, x1, y1], fill=GROUND)
    # distant treeline
    for tx in range(x0 + 8, x1 - 8, 26):
        draw.polygon([(tx, gy), (tx + 9, gy - 16), (tx + 18, gy)],
                     fill=(38, 44, 34))
    # missile streaks arcing down to the ground
    streaks = [((x0 + 40, y0 + 18), (x0 + 120, gy - 6)),
               ((x0 + 190, y0 + 8), (x0 + 235, gy - 26)),
               ((x0 + 300, y0 + 30), (x0 + 330, gy - 10))]
    for (sx, sy), (ex, ey) in streaks:
        draw.line([(sx, sy), (ex, ey)], fill=(255, 176, 66), width=5)
        draw.line([(sx, sy), (ex, ey)], fill=(255, 236, 190), width=2)
        draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 240, 200))
    # explosion bursts where the streaks land
    for bx, by, r in [(x0 + 120, gy - 6, 26), (x0 + 235, gy - 26, 20),
                      (x0 + 330, gy - 10, 22)]:
        for k in range(8):
            a = math.pi * k / 4.0
            px, py = bx + int(r * math.cos(a)), by + int(r * math.sin(a))
            draw.line([(bx, by), (px, py)], fill=(255, 190, 60), width=4)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 214, 90))
    # small white four-point star (NATO-style compass) in the sky
    cx, cy = x0 + 300, y0 + 52
    draw.polygon([(cx, cy - 22), (cx + 5, cy - 5), (cx + 22, cy),
                  (cx + 5, cy + 5), (cx, cy + 22), (cx - 5, cy + 5),
                  (cx - 22, cy), (cx - 5, cy - 5)], fill=(240, 240, 235))
    lab = font(SANS_B, 17)
    draw.text((x0 + 12, y1 - 30), "NOWY LIPOWIEC, POLAND",
              font=lab, fill=(255, 255, 255))


def draw_lead(draw):
    x0, x1 = 36, 988
    y = 178
    kick = font(SANS_B, 22)
    draw.text((x0, y), LEAD_KICKER, font=kick, fill=RED)
    head = font(SERIF, 35)
    draw.text((x0, y + 28), LEAD_HEAD, font=head, fill=INK)
    sub = font(SERIF_REG, 24)
    sub_lines = wrap(draw, LEAD_SUB, sub, 560)
    sy = y + 82
    for i, line in enumerate(sub_lines):
        draw.text((x0, sy + i * 30), line, font=sub, fill=NAVY)
    body = font(SANS, 19)
    by = sy + 30 * len(sub_lines) + 12
    for i, line in enumerate(wrap(draw, LEAD_BODY, body, 560)):
        draw.text((x0, by + i * 25), line, font=body, fill=INK)
    draw_scene(draw, 620, y, x1, y + 300)
    rule(draw, x0, x1, y + 318, INK, 2)


STORIES = [
    ("MIDDLE EAST", "RIYADH UNDER FIRE",
     "Saudi defences down three Houthi missiles bound for Riyadh, days "
     "after one hit its tallest tower."),
    ("CYBERSECURITY", "BANKS HIT BY VENDOR BREACH",
     "JPMorgan, Visa and Mastercard disclose a vendor breach claimed "
     "by \u201cn0n\u201d; payments were not hit."),
    ("CLIMATE", "COP31 SPILLS INTO OVERTIME",
     "Antalya talks run past their Friday deadline; the draft deal "
     "drops all mention of fossil fuels."),
    ("EUROPE", "UK-EU RESET DEAL AGREED",
     "Brussels agrees eased food trade, youth mobility for 100,000 a "
     "year and linked carbon markets."),
    ("WEATHER", "CYCLONE AKVAN MAKES LANDFALL",
     "The storm crosses the Odisha coast near Gopalpur after 80,000 "
     "people were moved to safety."),
    ("SPORT", "INDIA FIGHT BACK IN WELLINGTON",
     "India reach 159 for 1 at stumps on day two of the first Test, "
     "trailing New Zealand by 209."),
]

FOOTER_LINES = [
    "ICJ finds Myanmar guilty of genocide against the Rohingya \u2014 a first for any state",
    "US floats NATO membership for Ukraine for territory  \u2022  Kushner: Moscow \u201ccomfortable\u201d with NATO-like guarantees",
]


def draw_card(draw, x0, y0, w, kicker, headline, blurb):
    kf = font(SANS_B, 17)
    draw.text((x0, y0), kicker, font=kf, fill=RED)
    hf = font(SERIF, 21)
    draw.text((x0, y0 + 24), headline, font=hf, fill=INK)
    bf = font(SANS, 16)
    blines = wrap(draw, blurb, bf, w)[:2]
    for i, line in enumerate(blines):
        draw.text((x0, y0 + 58 + i * 21), line, font=bf, fill=INK)


def draw_footer(draw):
    y = 944
    rule(draw, 36, 988, y, INK, 2)
    ff = font(SANS, 15)
    for i, line in enumerate(FOOTER_LINES):
        draw.text((W // 2, y + 12 + i * 22), line, font=ff, fill=GREY,
                  anchor="ma")


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    # story grid: 2 columns x 3 rows
    gx, gy = 36, 522
    cw, ch = 466, 126
    gap_x, gap_y = 20, 14
    for idx, (kicker, head, blurb) in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cw + gap_x)
        y0 = gy + row * (ch + gap_y)
        draw_card(draw, x0, y0, cw, kicker, head, blurb)
        if col == 0:
            draw.line([(x0 + cw + 10, y0 + 4), (x0 + cw + 10, y0 + ch - 4)],
                      fill=(200, 192, 175), width=1)
    draw_footer(draw)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
