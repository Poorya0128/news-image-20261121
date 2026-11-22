"""Saturday 21 November 2026 - the world's news in one image.
Draws /output/entry.png deterministically (no network, no randomness)."""
import json, os, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2                      # supersampling factor
W = H = 1024
img = Image.new("RGB", (W * S, H * S), "#F6F1E7")
d = ImageDraw.Draw(img)

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name + ".ttf"), int(round(size * S)))
HEAD = lambda s: font("Newsreader-SemiBold", s)
SERIF = lambda s: font("SourceSerif4-Regular", s)
SERIFB = lambda s: font("SourceSerif4-SemiBold", s)
SANS = lambda s: font("Inter-Regular", s)
SANSB = lambda s: font("Inter-SemiBold", s)
COND = lambda s: font("BarlowCondensed-SemiBold", s)

INK = "#1A1A1A"; GREY = "#555049"; RULE = "#CFC6B4"; PAPER = "#F6F1E7"; CARD = "#FFFDF8"
RED = "#B3261E"
REG = {"ME": ("Middle East", "#B3261E"), "EU": ("Europe", "#2B5BA8"), "AS": ("Asia", "#B7791F"),
       "AF": ("Africa", "#2F7D4F"), "NA": ("N. America", "#6B46A8"), "LA": ("Latin America", "#C2185B"),
       "OC": ("Oceania", "#16808A"), "GL": ("Global", "#4A4A4A")}
SHORT = {"ME": "ME", "EU": "EU", "AS": "Asia", "AF": "Afr.", "NA": "N.Am.", "LA": "Lat. Am.", "OC": "Oce.", "GL": "Glob."}
SHORTN = {"ME": "Middle East", "EU": "Europe", "AS": "Asia", "AF": "Africa", "NA": "N. America", "LA": "Lat. America", "OC": "Oceania", "GL": "Global"}
BADGE = {"CONFIRMED": "#2F7D4F", "OFFICIAL": "#2B5BA8", "CLAIM": "#B3261E", "REPORTED": "#6E6A62"}

def R(v): return int(round(v * S))
def box(x0, y0, x1, y1, **kw):
    if "width" in kw: kw["width"] = R(kw["width"])
    d.rectangle([R(x0), R(y0), R(x1), R(y1)], **kw)
def poly(pts, **kw): d.polygon([(R(x), R(y)) for x, y in pts], **kw)
def line(pts, fill, w): d.line([(R(x), R(y)) for x, y in pts], fill=fill, width=R(w), joint="curve")
def ell(x0, y0, x1, y1, **kw):
    if "width" in kw: kw["width"] = R(kw["width"])
    d.ellipse([R(x0), R(y0), R(x1), R(y1)], **kw)
def T(x, y, s, f, fill=INK, anchor="la"): d.text((R(x), R(y)), s, font=f, fill=fill, anchor=anchor)
def tw(s, f): return d.textlength(s, font=f) / S

def wrap(s, f, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, f) <= width or not cur: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def fit(s, maker, size, width, maxlines, minsize):
    while size >= minsize:
        f = maker(size); ls = wrap(s, f, width)
        if len(ls) <= maxlines and all(tw(l, f) <= width for l in ls): return f, ls, size
        size -= 0.5
    print("WARN: text does not fit:", s)
    f = maker(minsize); return f, wrap(s, f, width)[:maxlines], minsize

def para(x, y, lines, f, lh, fill=INK):
    for l in lines: T(x, y, l, f, fill); y += lh
    return y

def badge(x, y, kind, size=10.5):
    f = SANSB(size); w = tw(kind, f) + 10
    box(x, y, x + w, y + size + 6, fill=BADGE[kind])
    T(x + 5, y + 2.4, kind, f, "white")
    return w

def label(x, y, s, size=13, bg=RED):
    f = COND(size); w = tw(s, f) + 10
    box(x, y, x + w, y + size + 5, fill=bg)
    T(x + 5, y + 1, s, f, "white")

# ------------------------------------------------------------------ illustrations
def ship(x, y, s=1.0, hull="#3A3F47", fire=True):
    poly([(x, y), (x + 54 * s, y), (x + 48 * s, y + 9 * s), (x + 5 * s, y + 9 * s)], fill=hull)
    box(x + 36 * s, y - 9 * s, x + 46 * s, y, fill="#E9E4D8")
    box(x + 8 * s, y - 4 * s, x + 32 * s, y, fill="#8C3B2E")
    if fire:
        cx = x + 20 * s
        for i, c in enumerate(["#55504A", "#6E6862", "#8A847D"]):
            ell(cx - 6 * s + i * 7 * s, y - 22 * s - i * 7 * s, cx + 8 * s + i * 7 * s, y - 10 * s - i * 7 * s, fill=c)
        poly([(cx - 7 * s, y - 3 * s), (cx, y - 16 * s), (cx + 7 * s, y - 3 * s)], fill="#F08A24")
        poly([(cx - 3 * s, y - 3 * s), (cx, y - 10 * s), (cx + 3 * s, y - 3 * s)], fill="#FFD34D")

def burst(cx, cy, r, c1="#F08A24", c2="#FFD34D"):
    pts = []
    for i in range(16):
        a = math.pi * 2 * i / 16; rr = r if i % 2 == 0 else r * 0.5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(pts, fill=c1); ell(cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3, fill=c2)

def art_tankers(x, y, w, h):
    box(x, y, x + w, y + h, fill="#A9CBE0")
    poly([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.62), (x + w * 0.86, y + h * 0.5),
          (x + w * 0.78, y + h * 0.28), (x + w * 0.64, y + h * 0.18)], fill="#E3D3AE")
    poly([(x, y + h * 0.05), (x + w * 0.22, y), (x + w * 0.2, y + h * 0.22), (x, y + h * 0.3)], fill="#E3D3AE")
    T(x + w * 0.80, y + h * 0.22, "OMAN", SANSB(12), "#6B5B3A", "mm")
    pass  # (small label removed for 300px legibility)
    ship(x + w * 0.22, y + h * 0.62, 1.15); ship(x + w * 0.52, y + h * 0.80, 0.95)
    T(x + w * 0.62, y + h * 0.42, "KHASAB", SANSB(12), "#1F3B57")
    label(x + 8, y + h - 24, "2 TANKERS HIT", 12, "#1F3B57")

def art_cop(x, y, w, h):
    box(x, y, x + w, y + h, fill="#DCEBD8")
    gx, gy, cw = x + 12, y + h * 0.36, (w - 90) / 7
    for i in range(13):
        r_, c_ = divmod(i, 7)
        bx, by = gx + c_ * cw, gy + r_ * (cw * 0.78)
        last = i == 12
        box(bx, by, bx + cw - 4, by + cw * 0.78 - 4, fill=RED if last else "#3E7A55")
        T(bx + (cw - 4) / 2, by + (cw * 0.78 - 4) / 2, str(i + 1), SANSB(10 if last else 9), "white", "mm")
    pass  # (small label removed for 300px legibility)
    tx = x + w - 40
    box(tx - 5, y + 18, tx + 5, y + h - 30, fill="white", outline="#7A7A7A", width=1)
    box(tx - 2.5, y + h * 0.42, tx + 2.5, y + h - 30, fill=RED)
    ell(tx - 10, y + h - 38, tx + 10, y + h - 18, fill=RED)
    label(x + 12, y + 8, "DAY 13 · NO DEAL", 12)

def art_mexico(x, y, w, h):
    box(x, y, x + w, y + h, fill="#F2D9A6")
    box(x, y + h * 0.72, x + w, y + h, fill="#C9A66B")
    for i, (bw, bh) in enumerate([(34, 30), (26, 22), (40, 36), (30, 26), (36, 32)]):
        bx = x + 14 + i * 46
        box(bx, y + h * 0.72 - bh, bx + bw, y + h * 0.72, fill=["#E8C48A", "#D9AE73", "#EBCB94"][i % 3])
        box(bx + 6, y + h * 0.72 - bh + 7, bx + 12, y + h * 0.72 - bh + 13, fill="#7A5A33")
    hx, hy = x + w * 0.66, y + h * 0.26
    ell(hx, hy, hx + 46, hy + 18, fill="#3B4A3A")
    poly([(hx + 40, hy + 7), (hx + 80, hy + 4), (hx + 80, hy + 9), (hx + 40, hy + 12)], fill="#3B4A3A")
    line([(hx - 18, hy - 5), (hx + 66, hy - 5)], "#3B4A3A", 2.5)
    line([(hx + 23, hy - 5), (hx + 23, hy + 1)], "#3B4A3A", 2.5)
    line([(hx + 8, hy + 22), (hx + 40, hy + 22)], "#3B4A3A", 2)
    box(x + w - 78, y + h - 22, x + w - 8, y + h - 6, fill="white", outline=INK, width=1)
    T(x + w - 43, y + h - 14, "FBI TOP TEN", SANSB(9), INK, "mm")
    label(x + 8, y + 8, "GUASAVE, SINALOA", 12, "#6B3E1E")

def art_quake(x, y, w, h):
    box(x, y, x + w, y + h, fill="#EFE1C7")
    poly([(x, y + h), (x, y + h * 0.62), (x + w * 0.3, y + h * 0.3), (x + w * 0.5, y + h * 0.55),
          (x + w * 0.72, y + h * 0.25), (x + w, y + h * 0.6), (x + w, y + h)], fill="#A98B67")
    pts, n = [], 40
    for i in range(n + 1):
        t = i / n; amp = 10 * math.exp(-((t - 0.45) ** 2) / 0.01)
        pts.append((x + 6 + t * (w - 12), y + h * 0.72 + amp * (1 if i % 2 else -1)))
    line(pts, RED, 1.6)
    T(x + w - 6, y + 4, "M6.7", HEAD(20), INK, "ra")
    pass  # (small label removed for 300px legibility)

def art_finland(x, y, w, h):
    box(x, y, x + w, y + h, fill="#B9CCD8")
    box(x, y + h * 0.66, x + w, y + h, fill="#7F9DB2")
    ship(x + w * 0.28, y + h * 0.70, 0.8, "#2F343B")
    for k in range(2):
        dx, dy = x + 20 + k * 30, y + 14 + k * 8
        poly([(dx, dy), (dx + 14, dy + 4), (dx, dy + 8), (dx + 3, dy + 4)], fill="#2F343B")
    pass  # (small label removed for 300px legibility)

def art_basra(x, y, w, h):
    box(x, y, x + w, y + h, fill="#2E2A33")
    box(x, y + h * 0.78, x + w, y + h, fill="#4A4350")
    for i in range(3):
        cx = x + 30 + i * 34
        poly([(cx, y + h * 0.78), (cx + 8, y + h * 0.25), (cx + 16, y + h * 0.25), (cx + 24, y + h * 0.78)], fill="#8C8494")
    for i in range(5):
        fx = x + w * 0.55 + i * 13
        poly([(fx, y + h * 0.8), (fx + 7, y + h * (0.32 + 0.05 * (i % 2))), (fx + 14, y + h * 0.8)], fill="#F08A24")
        poly([(fx + 3, y + h * 0.8), (fx + 7, y + h * 0.5), (fx + 11, y + h * 0.8)], fill="#FFD34D")
    T(x + w - 6, y + 5, "4 DEAD", SANSB(12), "white", "ra")

def art_trade(x, y, w, h):
    box(x, y, x + w, y + h, fill="#E7E3DA")
    fx, fy, fw, fh = x + 14, y + 8, 58, 32
    box(fx, fy, fx + fw, fy + fh, fill="#1F4BA5")
    for i in range(12):
        a = math.pi * 2 * i / 12
        cx, cy = fx + fw / 2 + 12 * math.cos(a), fy + fh / 2 + 12 * math.sin(a)
        ell(cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8, fill="#FFD34D")
    ix = x + w - 72
    box(ix, fy, ix + fw, fy + fh / 2, fill="#D3202A"); box(ix, fy + fh / 2, ix + fw, fy + fh, fill="white", outline="#BDB6A8", width=0.5)
    box(x + w / 2 - 13, y + 8, x + w / 2 + 13, y + 40, fill="white", outline="#8E877A", width=1)
    for k in range(3): line([(x + w / 2 - 8, y + 14 + k * 6), (x + w / 2 + 8, y + 14 + k * 6)], "#B8B1A4", 1)
    line([(x + w / 2 - 8, y + 35), (x + w / 2 - 2, y + 31), (x + w / 2 + 6, y + 35)], "#1F4BA5", 1.2)
    pass  # (small label removed for 300px legibility)

def art_drone(x, y, w, h):
    box(x, y, x + w, y + h, fill="#CFE0EA")
    box(x, y + h * 0.78, x + w, y + h, fill="#8FB0C4")
    cx, cy = x + w * 0.42, y + h * 0.42
    poly([(cx - 34, cy), (cx + 34, cy - 3), (cx + 34, cy + 3)], fill="#4A4F57")
    poly([(cx - 4, cy - 2), (cx + 6, cy - 15), (cx + 12, cy - 15), (cx + 8, cy)], fill="#4A4F57")
    poly([(cx - 4, cy + 2), (cx + 6, cy + 15), (cx + 12, cy + 15), (cx + 8, cy)], fill="#4A4F57")
    poly([(cx - 34, cy), (cx - 40, cy - 9), (cx - 36, cy)], fill="#4A4F57")
    ell(x + w - 52, y + 8, x + w - 20, y + 40, outline=RED, width=3)
    line([(x + w - 47, y + 13), (x + w - 25, y + 35)], RED, 3)
    pass  # (small label removed for 300px legibility)

def art_riyadh(x, y, w, h):
    box(x, y, x + w, y + h, fill="#1C2540")
    for i, bh in enumerate([22, 34, 18, 36, 26, 30, 20, 38, 24]):
        bx = x + 4 + i * (w - 8) / 9
        box(bx, y + h - bh, bx + (w - 8) / 9 - 3, y + h, fill="#2E3A5C")
    for k in range(3):
        sx, sy = x + 24 + k * 50, y + h - 10
        ex, ey = x + 40 + k * 58, y + 16 + (k % 2) * 8
        line([(sx, sy), (ex, ey)], "#C9D3E8", 1.2)
        burst(ex, ey, 9)
    pass  # (small label removed for 300px legibility)

def art_taiwan(x, y, w, h):
    box(x, y, x + w, y + h, fill="#F3E4E1")
    pts = [(x + 10, y + h * 0.2), (x + 40, y + h * 0.3), (x + 66, y + h * 0.42), (x + 90, y + h * 0.58), (x + 110, y + h * 0.66), (x + 128, y + h * 0.8)]
    line(pts, RED, 2.5)
    poly([(x + 132, y + h * 0.97), (x + 121, y + h * 0.74), (x + 139, y + h * 0.78)], fill=RED)
    T(x + w - 6, y + 6, "-17.5%", HEAD(19), RED, "ra")
    pass  # (small label removed for 300px legibility)

def art_bitcoin(x, y, w, h):
    box(x, y, x + w, y + h, fill="#22262E")
    pts = [(x + 12, y + 20), (x + 40, y + 30), (x + 62, y + h - 12), (x + 92, y + 36), (x + 122, y + 22)]
    line(pts, "#F7931A", 2.5)
    ell(x + 57, y + h - 17, x + 67, y + h - 7, fill="#F7931A")
    T(x + 62, y + h - 4, "", SANSB(7), "white", "ma")
    pass  # (small label removed for 300px legibility)
    pass  # (small label removed for 300px legibility)

def art_rugby(x, y, w, h):
    box(x, y, x + w, y + h, fill="#3E8A4F")
    for k in range(4): line([(x + 10 + k * 46, y + h), (x + 30 + k * 40, y)], "#5BA36A", 1)
    px = x + 24
    line([(px, y + 10), (px, y + h - 6)], "white", 2.5); line([(px + 22, y + 10), (px + 22, y + h - 6)], "white", 2.5)
    line([(px, y + h * 0.55), (px + 22, y + h * 0.55)], "white", 2.5)
    box(x + w - 98, y + 6, x + w - 8, y + h - 6, fill="#1B1B1B")
    pass  # (small label removed for 300px legibility)
    T(x + w - 53, y + h - 19, "37-12", HEAD(19), "#FFD34D", "mm")

def art_cricket(x, y, w, h):
    box(x, y, x + w, y + h, fill="#CFE3C3")
    poly([(x + 20, y + h - 6), (x + 64, y + 10), (x + 72, y + 13), (x + 30, y + h - 2)], fill="#C9A066")
    ell(x + 84, y + h - 26, x + 98, y + h - 12, fill=RED)
    T(x + w - 8, y + 8, "486-4", HEAD(20), INK, "ra")
    pass  # (small label removed for 300px legibility)

ART = {"tankers": art_tankers, "cop": art_cop, "mexico": art_mexico, "quake": art_quake,
       "finland": art_finland, "basra": art_basra, "trade": art_trade, "drone": art_drone,
       "riyadh": art_riyadh, "taiwan": art_taiwan, "bitcoin": art_bitcoin, "rugby": art_rugby,
       "cricket": art_cricket}

# ------------------------------------------------------------------ data
LEADS = [
    (1, "ME", "tankers", "OMAN · BAHRAIN · IRAN WAR", "CONFIRMED",
     "Two tankers hit off Oman; Iran claims Bahrain strikes",
     "UKMTO: projectiles hit 2 tankers off Khasab, no casualties. Bahrain says a civilian site burned; Iran's Guards claim US radars hit.",
     "Reuters · Al Jazeera · UKMTO"),
    (2, "EU", "cop", "ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 climate talks run into overtime",
     "Nearly 200 nations still split on fossil fuels; the final plenary is called for Sunday 06:00 GMT.",
     "Reuters · AFP"),
    (3, "NA", "mexico", "SINALOA, MEXICO · CRIME", "CONFIRMED",
     "Mexico seizes FBI-listed 'El Chapo Isidro'",
     "Fausto Isidro Meza Flores held in a Guasave raid; officials say 4 soldiers and 7 gunmen died.",
     "AP · Reuters"),
]
CARDS = [
    (4, "LA", "quake", "PERU · EARTHQUAKE", "OFFICIAL", "Deep 6.7 quake shakes central Peru",
     "108 km deep; felt in Lima; 1 dead, 16 hurt.", "USGS · INDECI · AFP"),
    (5, "EU", "finland", "FINLAND · UKRAINE WAR", "CONFIRMED", "Drones set Russian ship ablaze off Finland",
     "16 crew safe; Finland suspects Ukraine.", "Reuters · AFP"),
    (6, "ME", "basra", "BASRA, IRAQ · DISASTER", "CONFIRMED", "Fire at Basra power plant kills four",
     "Hartha thermal plant blaze; 35 injured.", "Reuters · Al Jazeera"),
    (7, "AS", "trade", "INDONESIA · EU · TRADE", "OFFICIAL", "Indonesia and EU sign trade pact",
     "Signed in Brussels after a decade of talks.", "European Commission · Antara"),
    (8, "ME", "drone", "STRAIT OF HORMUZ · WAR", "CLAIM", "Iran says it downed a US MQ-9 drone",
     "Revolutionary Guards' claim; no US comment.", "Al Jazeera · Reuters"),
    (9, "ME", "riyadh", "RIYADH · YEMEN WAR", "CLAIM", "Saudi coalition: 3 Houthi missiles intercepted",
     "Over Riyadh early Saturday, coalition says.", "Reuters · AFP"),
    (10, "AS", "taiwan", "TAIPEI · MARKETS", "OFFICIAL", "Taiwan curbs short-selling after rout",
     "TAIEX's worst week since 1991.", "Focus Taiwan · Bloomberg"),
    (11, "GL", "bitcoin", "WORLD · CRYPTO", "CONFIRMED", "Bitcoin hits 2-year low, then rebounds",
     "Low near $55,250; near $60k by 13:30 GMT.", "Reuters · CoinDesk"),
    (12, "EU", "rugby", "LONDON · RUGBY", "CONFIRMED", "England rout All Blacks 37-12",
     "Record winning margin over New Zealand.", "BBC · AP"),
    (13, "OC", "cricket", "WELLINGTON · CRICKET", "CONFIRMED", "Rahul's 136 puts India 118 ahead",
     "India 486-4 on day 3, after NZ's 368.", "Reuters · ESPNcricinfo"),
]
LIST = [
    (14, "EU", "France", "6th Saturday of cost-of-living marches", "Reuters"),
    (15, "ME", "Gaza", "strike on a van kills 3; Israel says militants", "AFP"),
    (16, "ME", "Lebanon", "Aoun demands Israel withdraw", "Al Jazeera"),
    (17, "ME", "Iran", "navy says a tanker hit a mine near Hormuz", "claim"),
    (18, "NA", "Washington", "US denies Iran hit an F-16", "ABC"),
    (19, "GL", "Geneva", "UN talks set path to robot-arms pact by 2028", "AFP"),
    (20, "EU", "Brussels", "EU on COP31: 'a good deal or no deal'", "Reuters"),
    (21, "EU", "Warsaw", "Rutte: NATO will defend 'every inch'", "Reuters"),
    (22, "EU", "Zagreb", "thousands protest a death in a clinic", "Reuters"),
    (23, "EU", "Pas-de-Calais", "floods hit 850 homes", "AFP"),
    (24, "AS", "New Delhi", "Pakistan minister at SCO forum", "Al Jazeera"),
    (25, "AS", "Manipur", "toxic liquor kills 16, officials say", "Reuters"),
    (26, "AS", "Fukushima", "snow cuts off a mountain village", "Kyodo"),
    (27, "AS", "Mastung", "Pakistan says 15 militants killed", "Dawn"),
    (28, "AF", "Ethiopia", "polio drive for 11.3m children starts", "WHO"),
    (29, "AF", "Abuja", "all 54 CAF members back Infantino", "AFP"),
    (30, "NA", "Las Vegas", "Verstappen gets pole after Antonelli penalty", "F1"),
    (31, "EU", "Dublin", "Ireland beat South Africa 20-17", "BBC"),
    (32, "EU", "Cardiff", "Australia edge Wales 29-26", "BBC"),
    (33, "EU", "Premier League", "Newcastle 2-2 Arsenal; Chelsea 1-4 Leeds", "AP"),
    (34, "OC", "Melbourne", "Australia beat England by 3 wickets in T20", "AFP"),
    (35, "NA", "NBA", "Harden's 51 is his 26th 50-point game", "AP"),
]
PINS = {1: (56.2, 26.2), 2: (30.7, 36.9), 3: (-108.5, 25.6), 4: (-76.0, -11.0), 5: (26.5, 60.0),
        6: (47.8, 30.5), 7: (106.8, -6.2), 8: (57.0, 24.2), 9: (46.7, 24.7), 10: (121.5, 25.0),
        12: (-0.1, 51.5), 13: (174.8, -41.3)}
DOTS = {14: (2.3, 48.9), 15: (34.45, 31.5), 16: (35.5, 33.9), 17: (58.0, 25.0), 18: (-77.0, 38.9),
        19: (6.1, 46.2), 20: (4.4, 50.8), 21: (21.0, 52.2), 22: (16.0, 45.8), 23: (2.3, 50.5),
        24: (77.2, 28.6), 25: (93.9, 24.8), 26: (140.0, 37.7), 27: (66.8, 29.8), 28: (38.7, 9.0),
        29: (7.5, 9.1), 30: (-115.1, 36.2), 31: (-6.3, 53.3), 32: (-3.2, 51.5), 33: (-1.6, 55.0),
        34: (145.0, -37.8), 35: (-81.7, 41.5)}

# ------------------------------------------------------------------ data
LEADS = [
    (1, "ME", "tankers", "MIDDLE EAST · IRAN WAR", "CONFIRMED",
     "Tankers hit off Oman; Iran claims Bahrain strike",
     "UKMTO: 2 tankers hit off Khasab, no casualties. Bahrain says a civilian site burned; Iran's Guards claim US radars.",
     "REUTERS · AL JAZEERA · UKMTO"),
    (2, "EU", "cop", "TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 climate talks run into overtime",
     "Nations still split on fossil fuels; final plenary called for Sunday 06:00 GMT.",
     "REUTERS · AFP"),
    (3, "NA", "mexico", "N. AMERICA · MEXICO", "CONFIRMED",
     "Mexico seizes FBI-listed 'El Chapo Isidro'",
     "Fausto Isidro Meza Flores held in Guasave raid; officials say 11 died.",
     "AP · REUTERS"),
]
CARDS = [
    (4, "LA", "quake", "LATIN AMERICA · QUAKE", "OFFICIAL", "M6.7 quake in Peru: 1 dead, 16 hurt", "USGS · INDECI"),
    (5, "EU", "finland", "EUROPE · FINLAND", "CONFIRMED", "Drones set Russian ship ablaze off Finland", "REUTERS · AFP"),
    (6, "ME", "basra", "MIDDLE EAST · IRAQ", "CONFIRMED", "Fire at Basra power plant kills four", "REUTERS · AL JAZEERA"),
    (7, "AS", "trade", "ASIA · TRADE", "OFFICIAL", "Indonesia and EU sign trade pact", "EU COMMISSION"),
    (8, "ME", "drone", "MIDDLE EAST · HORMUZ", "CLAIM", "Iran says it downed a US MQ-9 drone", "AL JAZEERA"),
    (9, "ME", "riyadh", "MIDDLE EAST · SAUDI", "CLAIM", "Saudis say 3 Houthi missiles intercepted", "REUTERS · AFP"),
    (10, "AS", "taiwan", "ASIA · MARKETS", "OFFICIAL", "Taiwan curbs short-selling after rout", "FOCUS TAIWAN"),
    (11, "GL", "bitcoin", "GLOBAL · CRYPTO", "CONFIRMED", "Bitcoin hits 2-year low, then rebounds", "REUTERS · COINDESK"),
    (12, "EU", "rugby", "EUROPE · RUGBY", "CONFIRMED", "England rout the All Blacks 37-12", "BBC · AP"),
    (13, "OC", "cricket", "OCEANIA · CRICKET", "CONFIRMED", "Rahul's 136 puts India 118 ahead", "ESPNCRICINFO"),
]
LIST = [
    (14, "EU", "France:", "82,500 march over living costs"),
    (15, "ME", "Gaza:", "van strike kills 3; Israel says militants"),
    (16, "ME", "Lebanon:", "Aoun demands Israel withdraw"),
    (17, "ME", "Iran:", "navy says tanker hit a mine"),
    (18, "NA", "US:", "denies Iran hit an F-16"),
    (19, "GL", "UN:", "path to robot-arms pact by 2028"),
    (20, "EU", "EU:", "'good deal or no deal' at COP31"),
    (21, "EU", "NATO:", "will defend 'every inch' of Poland"),
    (22, "EU", "Zagreb:", "protest over a death in a clinic"),
    (23, "EU", "France:", "floods hit 850 homes in north"),
    (24, "AS", "India:", "Pakistan minister at SCO forum"),
    (25, "AS", "Manipur:", "toxic liquor kills 16"),
    (26, "AS", "Japan:", "snow cuts off a Fukushima village"),
    (27, "AS", "Pakistan:", "says 15 militants killed"),
    (28, "AF", "Ethiopia:", "polio drive for 11.3m children"),
    (29, "AF", "CAF:", "all 54 members back Infantino"),
    (30, "NA", "F1:", "Verstappen on Vegas pole"),
    (31, "EU", "Rugby:", "Ireland 20-17 South Africa"),
    (32, "EU", "Rugby:", "Australia 29-26 Wales"),
    (33, "EU", "EPL:", "Newcastle 2-2 Arsenal; Leeds win"),
    (34, "OC", "Cricket:", "Australia beat England in T20"),
    (35, "NA", "NBA:", "Harden's 26th 50-point game"),
]
PINS = {1: (56.2, 26.2), 2: (30.7, 36.9), 3: (-108.5, 25.6), 4: (-76.0, -11.0), 5: (26.5, 60.0),
        6: (47.8, 30.5), 7: (106.8, -6.2), 8: (57.0, 24.2), 9: (46.7, 24.7), 10: (121.5, 25.0),
        12: (-0.1, 51.5), 13: (174.8, -41.3)}
DOTS = {14: (2.3, 48.9), 15: (34.45, 31.5), 16: (35.5, 33.9), 17: (58.0, 25.0), 18: (-77.0, 38.9),
        19: (6.1, 46.2), 20: (4.4, 50.8), 21: (21.0, 52.2), 22: (16.0, 45.8), 23: (2.3, 50.5),
        24: (77.2, 28.6), 25: (93.9, 24.8), 26: (140.0, 37.7), 27: (66.8, 29.8), 28: (38.7, 9.0),
        29: (7.5, 9.1), 30: (-115.1, 36.2), 31: (-6.3, 53.3), 32: (-3.2, 51.5), 33: (-1.6, 55.0),
        34: (145.0, -37.8), 35: (-81.7, 41.5)}

M = 12
# ------------------------------------------------------------------ masthead
kick = [("THE DAY IN WORLD NEWS", RED), ("  ·  35 STORIES  ·  8 REGIONS  ·  ALL FROM THIS SATURDAY", GREY)]
fk = SANSB(13); kw = sum(tw(a, fk) for a, _ in kick); kx = W / 2 - kw / 2
for a, c in kick: T(kx, 5, a, fk, c); kx += tw(a, fk)
T(W / 2, 56, "Saturday 21 November 2026", HEAD(70), INK, "mm")
box(M, 92, W - M, 93.2, fill=INK)

def rowlabel(y, l1, l2):
    T(M, y, l1, SANSB(12), RED); T(M, y + 15, l2, SANSB(12), RED)
LBLW = 92
# WORLD IN TIME
ty = 97
rowlabel(ty + 5, "WORLD IN", "TIME (UTC)")
TIMES = [("00:09", "Peru quake hits", "LA"), ("03:00", "Basra plant fire", "ME"), ("05:00", "Tankers hit off Oman", "ME"),
         ("13:30", "Bitcoin rebounds", "GL"), ("19:20", "Bahrain site burns", "ME")]
cw = (W - M - (M + LBLW)) / len(TIMES)
for i, (tm, what, rg) in enumerate(TIMES):
    cx = M + LBLW + cw * i + cw / 2
    if i: box(M + LBLW + cw * i, ty + 4, M + LBLW + cw * i + 0.8, ty + 42, fill=RULE)
    T(cx, ty + 12, tm, HEAD(21), REG[rg][1], "mm")
    f, ls, _ = fit(what, SERIFB, 17, cw - 8, 1, 13)
    T(cx, ty + 34, ls[0], f, INK, "mm")
box(M, ty + 48, W - M, ty + 48.8, fill=RULE)
# WORLD IN NUMBERS
ny = ty + 52
rowlabel(ny + 7, "WORLD IN", "NUMBERS")
NUMS = [("6.7", "Peru quake (USGS)", "LA"), ("2", "tankers hit off Oman", "ME"), ("11", "dead in Sinaloa raid", "NA"),
        ("82,500", "marched in France", "EU"), ("-17.5%", "Taiwan stocks, week", "AS"), ("37-12", "England v New Zealand", "EU")]
cw = (W - M - (M + LBLW)) / len(NUMS)
for i, (num, cap, rg) in enumerate(NUMS):
    cx = M + LBLW + cw * i + cw / 2
    if i: box(M + LBLW + cw * i, ny + 4, M + LBLW + cw * i + 0.8, ny + 46, fill=RULE)
    T(cx, ny + 15, num, HEAD(31), REG[rg][1], "mm")
    f, ls, _ = fit(cap, SERIFB, 17, cw - 6, 1, 12)
    T(cx, ny + 39, ls[0], f, INK, "mm")
box(M, ny + 52, W - M, ny + 53.2, fill=INK)

# ------------------------------------------------------------------ lead cards
gy = ny + 59; gap = 8; lw = (W - 2 * M - 2 * gap) / 3; ah = 90; LH = 232
LSZ = min(fit(L_[5], HEAD, 29, lw - 18, 2, 22)[2] for L_ in LEADS)
for i, (n, rg, art, kk, bd, head, sub, src) in enumerate(LEADS):
    x = M + i * (lw + gap)
    box(x, gy, x + lw, gy + LH, fill=CARD, outline=RULE, width=0.8)
    box(x, gy, x + lw, gy + 4, fill=REG[rg][1])
    ART[art](x, gy + 4, lw, ah)
    cy = gy + ah + 10
    ell(x + 8, cy, x + 24, cy + 16, fill=REG[rg][1]); T(x + 16, cy + 8, str(n), SANSB(10), "white", "mm")
    T(x + 30, cy + 2, kk, SANSB(11.5), REG[rg][1])
    f, ls, sz = fit(head, HEAD, LSZ, lw - 18, 2, 22)
    yy = para(x + 9, cy + 18, ls, f, sz * 1.02)
    fs, lss, szs = fit(sub, SANS, 12.5, lw - 18, 2, 10.5)
    para(x + 9, yy + 4, lss, fs, szs * 1.25, GREY)
    badge(x + 9, gy + LH - 21, bd, 12)
    fsr, lsr, _ = fit(src, SANSB, 10.5, lw - 110, 1, 8)
    T(x + lw - 9, gy + LH - 6, lsr[0], fsr, REG[rg][1], "rd")

# ------------------------------------------------------------------ small cards
sy0 = gy + LH + 7; sg = 7; sw = (W - 2 * M - 4 * sg) / 5; sh = 134; sah = 42
CSZ = min(fit(c[5], HEAD, 17, sw - 12, 3, 15)[2] for c in CARDS)
for k, (n, rg, art, kk, bd, head, src) in enumerate(CARDS):
    r_, c_ = divmod(k, 5)
    x, y = M + c_ * (sw + sg), sy0 + r_ * (sh + sg)
    box(x, y, x + sw, y + sh, fill=CARD, outline=RULE, width=0.8)
    box(x, y, x + sw, y + 3, fill=REG[rg][1])
    ART[art](x, y + 3, sw, sah)
    cy = y + sah + 7
    ell(x + 6, cy, x + 19, cy + 13, fill=REG[rg][1]); T(x + 12.5, cy + 6.5, str(n), SANSB(8.5), "white", "mm")
    f0, l0, _ = fit(kk, SANSB, 10, sw - 30, 1, 8)
    T(x + 23, cy + 1.5, l0[0], f0, REG[rg][1])
    f, ls, sz = fit(head, HEAD, CSZ, sw - 12, 3, 15)
    para(x + 7, cy + 15, ls, f, sz * 0.92)
    bw_ = badge(x + 7, y + sh - 19, bd, 10.5)
    fsrc, lsrc, _ = fit(src, SANSB, 9, sw - 20 - bw_, 1, 7)
    T(x + sw - 6, y + sh - 4, lsrc[0], fsrc, REG[rg][1], "rd")

# ------------------------------------------------------------------ map + date check (left)
by0 = sy0 + 2 * sh + sg + 6
mx0, my0, mw, mh = M, by0 + 17, 300, 112
box(mx0, my0, mx0 + mw, my0 + mh, fill="#C9DCE6")
LAT0, LAT1 = 72, -50
def proj(lon, lat): return (mx0 + (lon + 180) / 360 * mw, my0 + (LAT0 - lat) / (LAT0 - LAT1) * mh)
land = json.load(open(os.path.join(HERE, "data", "land.json")))
for ring in land:
    pts = [proj(lo, max(min(la, LAT0 + 5), LAT1 - 5)) for lo, la in ring]
    if len(pts) > 2: poly(pts, fill="#EFE6D2", outline="#A89878")
img.paste(Image.new("RGB", (R(mw + 4), R(12)), PAPER), (R(mx0 - 2), R(my0 + mh)))
img.paste(Image.new("RGB", (R(mw + 4), R(20)), PAPER), (R(mx0 - 2), R(my0 - 20)))
T(M, by0 + 2, "WHERE IT HAPPENED", SANSB(12), RED)
for n, (lo, la) in DOTS.items():
    rg = next(r for (m, r, *_) in LIST if m == n); px, py = proj(lo, la)
    ell(px - 2.4, py - 2.4, px + 2.4, py + 2.4, fill=REG[rg][1], outline="white")
for n, (lo, la) in PINS.items():
    rg = next(r for (m, r, *_) in LEADS + CARDS if m == n); px, py = proj(lo, la)
    off = {1: (6, -6), 8: (6, 7), 9: (-7, 4), 6: (-2, -8), 2: (-6, -6), 12: (-5, -5), 5: (0, -6)}.get(n, (0, 0))
    px += off[0]; py += off[1]
    px = min(max(px, mx0 + 7), mx0 + mw - 7); py = min(max(py, my0 + 7), my0 + mh - 7)
    ell(px - 6.5, py - 6.5, px + 6.5, py + 6.5, fill=REG[rg][1], outline="white", width=0.8)
    T(px, py, str(n), SANSB(7.5), "white", "mm")
counts = {}
for n, rg, *_ in LEADS + CARDS + LIST: counts[rg] = counts.get(rg, 0) + 1
order = ["EU", "ME", "AS", "NA", "AF", "LA", "OC", "GL"]
lx, lgy = mx0, my0 + mh + 3
for j, rg in enumerate(order):
    if j == 4: lx, lgy = mx0, lgy + 14
    s_ = f"{SHORTN[rg]} {counts[rg]}"; f_ = SANSB(10.5)
    ell(lx, lgy + 3, lx + 8, lgy + 11, fill=REG[rg][1]); T(lx + 11, lgy + 1, s_, f_, INK); lx += tw(s_, f_) + 22
dy = lgy + 18
DC = [("Kryvyi Rih strike", "Fri 20 Nov"), ("Missiles fall in Poland", "Fri 20 Nov"), ("Palisades Fire verdict", "Fri 20 Nov"),
      ("Denmark expels attaché", "Fri 20 Nov")]
dh = H - 16 - dy
box(mx0, dy, mx0 + mw, dy + dh, fill="#FADCD7", outline=RED, width=2.5)
box(mx0, dy, mx0 + mw, dy + 22, fill=RED)
T(mx0 + 7, dy + 4, "DATE CHECK · LEFT OUT AS OLDER NEWS", SANSB(13), "white")
yy = dy + 29
for a, b in DC:
    T(mx0 + 7, yy, a, SANSB(13.5), INK); T(mx0 + mw - 7, yy, b, SANSB(13.5), RED, "ra"); yy += 17
T(mx0 + 7, yy, "Not yet: COP31 final plenary", SANSB(13.5), INK); T(mx0 + mw - 7, yy, "Sun 22 Nov", SANSB(13.5), "#2B5BA8", "ra")

# ------------------------------------------------------------------ list (right)
lx0 = mx0 + mw + 14
colw = (W - M - lx0 - 14) / 2
heads = [("MORE FROM SATURDAY · 14-24", 0), ("MORE FROM SATURDAY · 25-35", 1)]
for h_, c_ in heads:
    x = lx0 + c_ * (colw + 14)
    T(x, by0 + 2, h_, SANSB(12), RED)
rowh = (dy + dh - (by0 + 20)) / 11
for i, (n, rg, place, what) in enumerate(LIST):
    c_, r_ = divmod(i, 11)
    x, y = lx0 + c_ * (colw + 14), by0 + 20 + r_ * rowh
    nf = SANSB(13); T(x, y + 2, str(n), nf, REG[rg][1])
    fp = SANSB(15); T(x + 22, y + 1, place, fp, INK)
    px = x + 22 + tw(place, fp) + 4
    sz = 15
    while tw(what, SANS(sz)) > x + colw - px and sz > 11: sz -= 0.25
    T(px, y + 1 + (15 - sz) * 0.8, what, SANS(sz), INK)
    if r_ < 10: box(x, y + rowh - 2.5, x + colw, y + rowh - 2, fill="#DDD5C4")

# ------------------------------------------------------------------ footer
T(M, H - 5, "Saturday 21 November 2026, UTC times. CONFIRMED = 2+ outlets · OFFICIAL = on the record · CLAIM = one side's account. "
  "Original drawings, not photos. Sources: Reuters, AP, AFP, BBC, Al Jazeera, USGS, UKMTO.", SANS(8.6), GREY, "ls")

# ------------------------------------------------------------------ output
out = img.resize((W, H), Image.LANCZOS)
out = out.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
path = "/output/entry.png" if os.path.isdir("/output") else os.path.join(HERE, "entry.png")
out.save(path, format="PNG", optimize=True)
