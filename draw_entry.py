#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a newspaper front page summing up
Friday 20 November 2026 in one 1024x1024 PNG. Deterministic, no network."""
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 238)
INK = (22, 22, 22)
GREY = (90, 90, 90)
RED = (178, 34, 34)
BLUE = (30, 70, 140)
NIGHT = (14, 22, 52)
RIVER = (18, 48, 92)
ORANGE = (255, 140, 30)
YELLOW = (255, 210, 80)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS_OBL = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def center(draw, y, s, fnt, fill=INK):
    draw.text(((W - text_w(draw, s, fnt)) / 2, y), s, font=fnt, fill=fill)


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def center_block(draw, cx, y, s, fnt, fill, max_w, line_h):
    for line in wrap(draw, s, fnt, max_w):
        draw.text((cx - text_w(draw, line, fnt) / 2, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def flash(draw, cx, cy, r):
    """Explosion starburst."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)
    pts2 = [(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in pts]
    draw.polygon(pts2, fill=YELLOW)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 245, 200))


def draw_lead_art(draw):
    x0, y0, x1, y1 = 46, 336, 978, 516
    # night sky in horizontal bands
    for i in range(24):
        t = i / 24
        col = tuple(int(NIGHT[c] + (40 - NIGHT[c]) * t) for c in range(3))
        draw.rectangle([x0, y0 + i * 5, x1, y0 + (i + 1) * 5 + 1], fill=col)
    # stars (seeded, deterministic)
    rng = random.Random(20261120)
    for _ in range(70):
        sx = rng.randint(x0 + 8, x1 - 8)
        sy = rng.randint(y0 + 6, y0 + 95)
        draw.point((sx, sy), fill=(230, 235, 255))
        if rng.random() < 0.3:
            draw.point((sx + 1, sy), fill=(180, 190, 230))
    # moon
    draw.ellipse([x1 - 92, y0 + 16, x1 - 48, y0 + 60], fill=(238, 240, 220))
    draw.ellipse([x1 - 84, y0 + 24, x1 - 76, y0 + 32], fill=(205, 208, 195))
    draw.ellipse([x1 - 66, y0 + 38, x1 - 58, y0 + 46], fill=(205, 208, 195))
    # river
    draw.rectangle([x0, y1 - 42, x1, y1], fill=RIVER)
    for i in range(9):
        ry = y1 - 36 + i * 4
        draw.line([x0 + 20 + (i * 53) % 120, ry, x0 + 90 + (i * 53) % 120, ry],
                  fill=(70, 120, 180), width=1)
    # bridge: towers, deck, cables
    deck_y = y1 - 42
    for tx in (x0 + 190, x1 - 190):
        draw.rectangle([tx - 10, y0 + 78, tx + 10, deck_y], fill=(52, 64, 96))
    draw.rectangle([x0 + 6, deck_y - 8, x1 - 6, deck_y], fill=(52, 64, 96))
    for tx in (x0 + 190, x1 - 190):
        draw.line([tx, y0 + 78, x0 + 30, deck_y - 8], fill=(150, 160, 190), width=2)
        draw.line([tx, y0 + 78, x1 - 30, deck_y - 8], fill=(150, 160, 190), width=2)
    mid = (x0 + x1) // 2
    draw.line([x0 + 190, y0 + 78, mid, deck_y - 26], fill=(150, 160, 190), width=2)
    draw.line([x1 - 190, y0 + 78, mid, deck_y - 26], fill=(150, 160, 190), width=2)
    for vx in range(x0 + 60, x1 - 40, 64):
        draw.line([vx, deck_y - 20, vx, deck_y - 8], fill=(120, 130, 160), width=1)
    # explosions + smoke
    flash(draw, x0 + 190, y0 + 66, 30)
    flash(draw, mid + 120, deck_y - 44, 24)
    flash(draw, x1 - 300, y0 + 92, 18)
    for (sx, sy, sr) in ((x0 + 250, y0 + 40, 16), (x0 + 285, y0 + 30, 12),
                         (mid + 170, deck_y - 78, 13)):
        draw.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2],
                     fill=(105, 108, 120))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---- panel icons (drawn in a box centred on cx, top at y) ----

def icon_fence(draw, cx, y):
    for dx in (-30, -10, 10, 30):
        draw.rectangle([cx + dx - 3, y, cx + dx + 3, y + 40], fill=INK)
        draw.polygon([(cx + dx - 3, y), (cx + dx + 3, y), (cx + dx, y - 6)], fill=INK)
    draw.rectangle([cx - 38, y + 10, cx + 38, y + 15], fill=RED)
    draw.rectangle([cx - 38, y + 26, cx + 38, y + 31], fill=RED)


def icon_flags(draw, cx, y):
    draw.line([cx - 24, y, cx - 24, y + 42], fill=INK, width=3)
    draw.line([cx + 24, y, cx + 24, y + 42], fill=INK, width=3)
    draw.rectangle([cx - 24, y, cx + 8, y + 20], fill=BLUE)
    for (sx, sy) in ((-16, 4), (-6, 4), (-11, 10), (-16, 15), (-6, 15)):
        draw.ellipse([cx + sx - 2, y + sy - 2, cx + sx + 2, y + sy + 2], fill=YELLOW)
    draw.rectangle([cx + 24, y, cx + 56, y + 20], outline=INK, fill=(245, 245, 245))
    draw.rectangle([cx + 36, y, cx + 44, y + 20], fill=RED)
    draw.rectangle([cx + 24, y + 7, cx + 56, y + 13], fill=RED)


def icon_dome(draw, cx, y):
    draw.arc([cx - 30, y - 2, cx + 30, y + 44], start=180, end=360, fill=INK, width=4)
    draw.line([cx, y - 10, cx, y - 1], fill=INK, width=3)
    draw.rectangle([cx - 34, y + 22, cx + 34, y + 27], fill=INK)
    for dx in (-26, -9, 9, 26):
        draw.rectangle([cx + dx - 2, y + 27, cx + dx + 2, y + 40], fill=INK)
    draw.rectangle([cx - 36, y + 40, cx + 36, y + 44], fill=RED)


def icon_chart(draw, cx, y):
    draw.line([cx - 38, y + 4, cx - 38, y + 40], fill=GREY, width=2)
    draw.line([cx - 38, y + 40, cx + 40, y + 40], fill=GREY, width=2)
    pts = [(cx - 34, y + 8), (cx - 16, y + 14), (cx + 2, y + 10),
           (cx + 18, y + 24), (cx + 34, y + 34)]
    draw.line(pts, fill=RED, width=4)
    draw.polygon([(cx + 34, y + 34), (cx + 22, y + 33), (cx + 33, y + 22)], fill=RED)


def icon_thermo(draw, cx, y):
    draw.rounded_rectangle([cx - 8, y - 4, cx + 8, y + 30], radius=8, outline=INK, width=3)
    draw.ellipse([cx - 13, y + 24, cx + 13, y + 50], outline=INK, width=3)
    draw.ellipse([cx - 8, y + 29, cx + 8, y + 45], fill=RED)
    draw.rectangle([cx - 3, y + 12, cx + 3, y + 34], fill=RED)
    # leaf
    draw.ellipse([cx + 16, y + 6, cx + 42, y + 24], fill=(46, 125, 50))
    draw.line([cx + 17, y + 23, cx + 41, y + 7], fill=(220, 240, 220), width=2)


def icon_cross(draw, cx, y):
    draw.ellipse([cx - 24, y - 4, cx + 24, y + 44], outline=RED, width=3)
    draw.rectangle([cx - 6, y + 6, cx + 6, y + 34], fill=RED)
    draw.rectangle([cx - 14, y + 14, cx + 14, y + 26], fill=RED)


def icon_shield(draw, cx, y):
    pts = [(cx, y - 4), (cx + 26, y + 4), (cx + 26, y + 22),
           (cx, y + 48), (cx - 26, y + 22), (cx - 26, y + 4)]
    draw.polygon(pts, fill=BLUE)
    import math
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 11 if i % 2 == 0 else 4.5
        star.append((cx + rr * math.cos(ang), y + 20 + rr * math.sin(ang)))
    draw.polygon(star, fill=(255, 255, 255))


def panel(draw, x0, y0, x1, y1, icon, headline, summary):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cx = (x0 + x1) // 2
    icon(draw, cx, y0 + 13)
    hf = font(SANS_BOLD, 18)
    sf = font(SANS, 14)
    y = center_block(draw, cx, y0 + 60, headline, hf, INK, x1 - x0 - 16, 22)
    center_block(draw, cx, y + 2, summary, sf, (45, 45, 45), x1 - x0 - 16, 18)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    draw.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    draw.rectangle([22, 22, W - 22, H - 22], outline=INK, width=1)

    # masthead
    center(draw, 34, "THE DAILY PICTURE", font(SERIF_BOLD, 57))
    draw.rectangle([40, 106, W - 40, 108], fill=INK)
    draw.rectangle([40, 112, W - 40, 116], fill=INK)
    date_f = font(SANS_BOLD, 39)
    center(draw, 126, "FRIDAY 20 NOVEMBER 2026", date_f, RED)
    draw.text((44, 138), "VOL. I", font=font(SANS_BOLD, 16), fill=GREY)
    right = "ONE PAGE"
    draw.text((W - 44 - text_w(draw, right, font(SANS_BOLD, 16)), 138),
              right, font=font(SANS_BOLD, 16), fill=GREY)
    draw.rectangle([40, 176, W - 40, 178], fill=INK)

    # lead story
    center(draw, 188, "UKRAINE WAR - LEAD STORY", font(SANS_BOLD, 18), RED)
    lead_f = font(SANS_BOLD, 45)
    center(draw, 214, "RUSSIA HITS KYIV BRIDGES;", lead_f)
    center(draw, 268, "MISSILES CROSS INTO POLAND", lead_f)
    draw_lead_art(draw)
    center(draw, 524, "Kyiv's bridges under fire in Russia's overnight strikes.",
           font(SANS_OBL, 15), GREY)
    sf = font(SANS, 21)
    center(draw, 552, "Overnight strikes killed 8 people and injured 28 across", sf)
    center(draw, 580, "nine regions, Kyiv's mayor said. Two missiles and a drone", sf)
    center(draw, 608, "from Russia also violated Poland's airspace overnight.", sf)
    draw.rectangle([40, 644, W - 40, 647], fill=INK)

    # grid of panels: row A (4), row B (3)
    panels_a = [
        (icon_fence, "ESTONIA SHUTS ITS BORDER",
         "Border with Russia closed at least 6 months; Moscow cries new 'Iron Curtain'."),
        (icon_flags, "EU-UK RESET GROWS",
         "Youth scheme: up to 100,000 a year each way to travel, work and study."),
        (icon_dome, "SENATE BLOCKS IRAN MOVE",
         "Republicans win 51-48; Trump decides next steps in the new year."),
        (icon_chart, "STOCKS FALL ON AI DOUBTS",
         "S&P 500 -2%, a 5th straight fall; Nikkei -4.8%. Anthropic IPO +17%."),
    ]
    panels_b = [
        (icon_thermo, "COP31 DROPS FOSSIL-FUEL EXIT",
         "Negotiators in Antalya drop any call to phase out fossil fuels from the draft deal."),
        (icon_cross, "KENYA EBOLA-FREE AT LAST",
         "Last Ebola patient discharged, 37 days after the country's first case."),
        (icon_shield, "HAITI: 34 GANG SUSPECTS KILLED",
         "National police say 34 suspected gang members were killed in operations."),
    ]
    gx0, gx1, gap = 40, W - 40, 10
    pw_a = (gx1 - gx0 - gap * 3) // 4
    for i, (ic, hd, sm) in enumerate(panels_a):
        x0 = gx0 + i * (pw_a + gap)
        panel(draw, x0, 658, x0 + pw_a, 822, ic, hd, sm)
    pw_b = (gx1 - gx0 - gap * 2) // 3
    for i, (ic, hd, sm) in enumerate(panels_b):
        x0 = gx0 + i * (pw_b + gap)
        panel(draw, x0, 832, x0 + pw_b, 990, ic, hd, sm)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    out = os.path.join(out_dir, "entry.png")
    img.save(out, format="PNG", optimize=False)
    print("wrote", out)


if __name__ == "__main__":
    main()
