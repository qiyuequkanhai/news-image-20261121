#!/usr/bin/env python3
"""Render a newspaper front page for Saturday, 21 November 2026.

Pure Python standard library only. Draws text with a hand-built 5x7
bitmap font and writes the PNG by hand (zlib + struct), so the build
needs no third-party packages, no fonts on disk and no network.

Usage:
    python3 tools/build_image.py [output-path]
Default output is entry.png in the repository root.
"""

import binascii
import os
import struct
import sys
import zlib

WIDTH = 1024
HEIGHT = 1024

# ---------------------------------------------------------------------------
# 5x7 bitmap font. Each glyph is 7 rows of 5 bits ("1" = ink).
# ---------------------------------------------------------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    ";": ("00000", "01100", "00000", "01100", "00100", "01000", "00000"),
    ":": ("00000", "01100", "00000", "01100", "00000", "01100", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "\\": ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
    "~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    "`": ("01000", "00100", "00000", "00000", "00000", "00000", "00000"),
    "^": ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    "\u2022": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}

# Normalise fancy punctuation to glyphs we have.
NORMALISE = {
    "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": ".", "\u00a0": " ",
}

BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")

# Colours.
INK = (20, 20, 20)
PAPER = (250, 248, 240)
GREY = (110, 108, 100)
RULE = (40, 40, 40)
NIGHT_TOP = (13, 28, 52)
NIGHT_MID = (30, 58, 92)
NIGHT_LOW = (52, 84, 120)
BUILDING = (8, 12, 20)
WINDOW = (255, 214, 110)
FIRE_CORE = (255, 226, 90)
FIRE_MID = (255, 140, 40)
FIRE_OUT = (214, 60, 30)
SMOKE = (120, 120, 124)
RED = (178, 34, 34)
GREEN = (34, 120, 60)


class Canvas:
    """A plain RGB pixel buffer with tiny drawing helpers."""

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.buf = bytearray(PAPER * width * height)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + len(row)] = row

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill_rect(x, y, t, h, color)

    def border(self, x, y, w, h, color, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    # -- text -------------------------------------------------------------
    @staticmethod
    def text_width(text, scale):
        return len(text) * 6 * scale

    def draw_text(self, x, y, text, scale, color=INK):
        for ch in text:
            glyph = FONT.get(NORMALISE.get(ch, ch), BLANK)
            for row_i, row in enumerate(glyph):
                for col_i, bit in enumerate(row):
                    if bit == "1":
                        self.fill_rect(
                            x + col_i * scale, y + row_i * scale,
                            scale, scale, color)
            x += 6 * scale

    def draw_centered(self, cx, y, text, scale, color=INK):
        self.draw_text(cx - self.text_width(text, scale) // 2, y,
                       text, scale, color)

    def wrap(self, text, scale, max_w):
        lines, cur = [], ""
        for word in text.split(" "):
            trial = (cur + " " + word).strip()
            if self.text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def draw_wrapped(self, x, y, text, scale, max_w, leading, color=INK):
        """Draw wrapped text; return the y just below the last line."""
        lines = self.wrap(text, scale, max_w)
        for i, line in enumerate(lines):
            self.draw_text(x, y + i * leading, line, scale, color)
        return y + len(lines) * leading


# ---------------------------------------------------------------------------
# Illustrations (drawn, no external images)
# ---------------------------------------------------------------------------
def draw_night_skyline(cv, x, y, w, h):
    """Night sky over a city skyline with two explosion bursts."""
    # Sky: three horizontal bands, darker at the top.
    cv.fill_rect(x, y, w, h // 3, NIGHT_TOP)
    cv.fill_rect(x, y + h // 3, w, h // 3, NIGHT_MID)
    cv.fill_rect(x, y + 2 * h // 3, w, h - 2 * h // 3, NIGHT_LOW)
    # Stars: a fixed, deterministic scatter.
    stars = [(18, 12), (52, 30), (96, 8), (140, 26), (188, 14), (232, 34),
             (268, 10), (312, 28), (348, 12), (392, 30), (428, 16),
             (470, 26), (512, 10), (60, 52), (210, 48), (360, 50)]
    for sx, sy in stars:
        if sx < w and sy < h // 2:
            cv.fill_rect(x + sx, y + sy, 2, 2, (235, 235, 255))
    # Explosion bursts: concentric discs plus radiating bars.
    for cx, cy, r in [(x + int(w * 0.30), y + int(h * 0.42), 34),
                      (x + int(w * 0.72), y + int(h * 0.34), 26)]:
        cv.disc(cx, cy, r, FIRE_OUT)
        cv.disc(cx, cy, int(r * 0.66), FIRE_MID)
        cv.disc(cx, cy, int(r * 0.36), FIRE_CORE)
        for dx, dy in [(r, 0), (-r, 0), (0, -r), (0, r),
                       (int(r * 0.7), int(r * 0.7)),
                       (-int(r * 0.7), -int(r * 0.7))]:
            cv.fill_rect(cx + dx - 2, cy + dy - 2, 4, 4, FIRE_MID)
    # Smoke puffs above the skyline.
    for cx, cy, r in [(x + int(w * 0.30), y + int(h * 0.30), 16),
                      (x + int(w * 0.72), y + int(h * 0.22), 12),
                      (x + int(w * 0.52), y + int(h * 0.36), 10)]:
        cv.disc(cx, cy, r, SMOKE)
        cv.disc(cx - 6, cy + 4, int(r * 0.7), SMOKE)
    # Buildings: deterministic heights across the width.
    base = y + h
    heights = [62, 96, 74, 118, 88, 132, 70, 104, 80, 122, 66, 92]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        cv.fill_rect(bx + 2, base - bh, bw - 4, bh, BUILDING)
        # Lit windows in a fixed pattern.
        for wy in range(base - bh + 8, base - 10, 16):
            for wx in range(bx + 7, bx + bw - 7, 12):
                if (wx * 7 + wy * 3) % 5 < 2:
                    cv.fill_rect(wx, wy, 3, 4, WINDOW)
    cv.hline(x, base - 1, w, BUILDING, 2)


def draw_market_chart(cv, x, y, w, h):
    """Simple bar chart of Friday's market falls (percent)."""
    cv.border(x, y, w, h, RULE, 1)
    cv.draw_text(x + 8, y + 6, "FRIDAY'S FALLS, %", 1, GREY)
    baseline = y + h - 26
    cv.hline(x + 8, baseline, w - 16, RULE, 1)
    data = [("S&P", -3.7, RED), ("NAS", -5.0, RED), ("DOW", -3.5, RED),
            ("FTSE", -1.2, RED), ("NIK", -2.1, RED)]
    bw = (w - 32) // len(data)
    for i, (label, val, color) in enumerate(data):
        bx = x + 16 + i * bw
        bar_h = int(abs(val) / 5.0 * (h - 44))
        cv.fill_rect(bx + 4, baseline - bar_h, bw - 12, bar_h, color)
        cv.draw_text(bx + 2, baseline + 4, label, 1, INK)
        cv.draw_text(bx + 2, baseline + 14, "%.1f" % val, 1, GREY)


# ---------------------------------------------------------------------------
# PNG writer (stdlib only)
# ---------------------------------------------------------------------------
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, cv):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        raw.extend(cv.buf[yy * stride:(yy + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
           + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


# ---------------------------------------------------------------------------
# Page composition
# ---------------------------------------------------------------------------
def build(out_path):
    cv = Canvas(WIDTH, HEIGHT)
    m = 36                      # page margin
    right = WIDTH - m           # right edge of the text area
    cw = right - m              # content width = 952

    # Masthead.
    cv.draw_centered(WIDTH // 2, 22, "THE WORLD TODAY", 8)
    cv.hline(m, 92, cw, RULE, 3)
    cv.draw_text(m, 102, "SATURDAY, 21 NOVEMBER 2026", 2)
    cv.draw_centered(WIDTH // 2, 102, "WORLD EDITION", 2, GREY)
    cv.draw_text(right - cv.text_width("NO. 325", 2), 102, "NO. 325", 2)
    cv.hline(m, 124, cw, RULE, 1)

    # Lead kicker + headline.
    cv.draw_text(m, 136, "WAR IN UKRAINE", 2, RED)
    cv.draw_text(m, 158, "RUSSIA'S BIGGEST NOVEMBER BARRAGE", 4)
    cv.draw_text(m, 194, "HITS KYIV; MISSILES LAND IN POLAND", 4)
    cv.draw_text(m, 232, "Kyiv counts its dead as the war spills across the "
                         "Polish border.", 2, GREY)

    # Lead illustration (left) and lead story (right).
    img_x, img_y, img_w, img_h = m, 258, 560, 200
    draw_night_skyline(cv, img_x, img_y, img_w, img_h)
    cv.border(img_x, img_y, img_w, img_h, RULE, 1)
    cv.draw_text(m, 464, "Smoke rises over Kyiv after the overnight barrage. "
                         "Two missiles", 1, GREY)
    cv.draw_text(m, 478, "and a drone also came down inside Poland.",
                 1, GREY)
    lead = ("Russia fired 404 drones and 111 missiles at Ukraine overnight "
            "on Nov. 19-20, its biggest strike package of November. At least "
            "eight people were killed in Kyiv, where three bridges were "
            "damaged. Two missiles and a drone came down inside Poland. "
            "Prime Minister Donald Tusk called it a deliberate provocation.")
    body_x = img_x + img_w + 16
    body_w = right - body_x
    end_y = cv.draw_wrapped(body_x, 258, lead, 2, body_w, 18)
    assert end_y <= 496, "lead story overflowed: %d" % end_y
    cv.draw_text(body_x, end_y + 10, "KYIV - Continued on Page 2", 1, GREY)

    # Rule above the second row.
    cv.hline(m, 516, cw, RULE, 2)

    # Second row: three columns.
    col_w = 300
    col_xs = [m, m + 326, m + 652]
    row2_y = 532

    # Column 1: World Court / Myanmar.
    x = col_xs[0]
    for i, line in enumerate(["WORLD COURT", "FINDS MYANMAR",
                              "GUILTY OF", "GENOCIDE"]):
        cv.draw_text(x, row2_y + i * 22, line, 3)
    end_y = cv.draw_wrapped(
        x, row2_y + 94,
        "In a landmark 9-6 judgment, the International Court of Justice "
        "held Myanmar responsible for genocide against the Rohingya, the "
        "first time a state has been found guilty of genocide. "
        "Reparations were ordered.",
        2, col_w, 16)
    assert end_y <= 790, "column 1 overflowed: %d" % end_y

    # Column 2: markets.
    x = col_xs[1]
    for i, line in enumerate(["AI SELL-OFF", "PUSHES S&P 500",
                              "INTO CORRECTION"]):
        cv.draw_text(x, row2_y + i * 22, line, 3)
    end_y = cv.draw_wrapped(
        x, row2_y + 72,
        "US stocks fell sharply on Friday as an AI sell-off pushed the "
        "S&P 500 down 3.7 percent into correction territory, with the "
        "Nasdaq sliding about 5 percent.",
        2, col_w, 16)
    draw_market_chart(cv, x, end_y + 8, col_w, 72)
    assert end_y + 8 + 72 <= 796, "column 2 overflowed"

    # Column 3: climate talks.
    x = col_xs[2]
    for i, line in enumerate(["CLIMATE TALKS", "RUN PAST",
                              "DEADLINE IN", "ANTALYA"]):
        cv.draw_text(x, row2_y + i * 22, line, 3)
    end_y = cv.draw_wrapped(
        x, row2_y + 94,
        "The UN climate summit in Antalya ran into overtime as nearly 200 "
        "nations failed to agree on a final deal. A new draft dropped "
        "explicit promises to move away from coal, oil and gas, drawing "
        "fire from small island states.",
        2, col_w, 16)
    assert end_y <= 790, "column 3 overflowed: %d" % end_y

    # Rule above the third row.
    cv.hline(m, 796, cw, RULE, 2)

    # Third row, left: UK-EU deal.
    y3 = 812
    cv.draw_text(m, y3, "UK AND EU SIGN BIGGEST", 3)
    cv.draw_text(m, y3 + 24, "POST-BREXIT DEAL", 3)
    end_y = cv.draw_wrapped(
        m, y3 + 54,
        "British Prime Minister Andy Burnham and EU leaders signed three "
        "agreements in Brussels on food, carbon markets and youth "
        "mobility, the biggest post-Brexit package yet. Most food checks "
        "end in 2028.",
        2, 452, 18)
    assert end_y <= 984, "UK-EU story overflowed: %d" % end_y

    # Third row, right: briefs.
    bx = m + 500
    cv.draw_text(bx, y3, "ALSO IN THE NEWS", 2, RED)
    cv.hline(bx, y3 + 20, right - bx, RULE, 1)
    by = y3 + 30
    by = cv.draw_wrapped(
        bx, by,
        "SHENZHEN SUMMIT: Trump, Xi and Putin met for 90 minutes and "
        "signed a four-point peace declaration that said nothing about "
        "Ukraine.", 2, right - bx, 18)
    by = cv.draw_wrapped(
        bx, by + 8,
        "PERU QUAKE: A magnitude 6.8 earthquake shook central Peru. No "
        "deaths or major damage were reported.", 2, right - bx, 18)
    assert by <= 984, "briefs overflowed: %d" % by

    # Footer.
    cv.hline(m, 984, cw, RULE, 1)
    cv.draw_centered(
        WIDTH // 2, 996,
        "THE WORLD TODAY - Saturday, 21 November 2026", 1, GREY)

    size = write_png(out_path, cv)
    print("wrote %s (%d bytes, %dx%d)" % (out_path, size, WIDTH, HEIGHT))
    return size


def main(argv):
    out = argv[1] if len(argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "entry.png")
    build(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
