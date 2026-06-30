import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svgkit import (write, esc, text_w, frame_open, frame_close, typing_banner,
                     terminal_panel, BG, BG_DEEP, GREEN, GREEN_DIM, WHITE, GRAY,
                     BORDER, FONT)

OUT = "/home/claude/proj/assets/svg"

# =====================================================================
# 1) H2 SECTION BANNERS — animated typing SVGs
# =====================================================================
BANNERS = [
    ("header-01-whoami",    "> whoami"),
    ("header-02-skills",    "> ls --color=auto ./skills"),
    ("header-03-career",    "> cat career_timeline.log"),
    ("header-04-mission",   "> cat current_mission.log"),
    ("header-05-projects",  "> tree ./projects"),
    ("header-06-progress",  "> watch -n 1 progress"),
    ("header-07-stats",     "> sudo cat /proc/github_stats"),
    ("header-08-contact",   "> curl contact.info"),
    ("header-09-finger",    "> finger joembolinas"),
]
for name, prompt in BANNERS:
    typing_banner(f"{OUT}/{name}.svg", prompt, width=880, height=44, size=19, dur=5.5)

# top hero tagline banner (bigger, slower)
typing_banner(f"{OUT}/banner-tagline.svg",
              "> IT Student | Operations Professional | Future Cybersecurity Analyst",
              width=880, height=40, size=16, dur=7)

print("banners done")

# =====================================================================
# 2) WHOAMI — pixel-matrix hoodie avatar + bio terminal panel
# =====================================================================
import random
random.seed(7)

def gen_avatar(path, w=210, h=330, cols=24, rows=38):
    cell = w / cols
    rows_h = h / rows
    cells = []
    hood_end   = int(rows * 0.30)
    shoulder_end = int(rows * 0.46)
    for r in range(rows):
        t = r / rows
        if r <= hood_end:
            # rounded hood: parabolic widen
            k = r / max(hood_end, 1)
            half = (0.10 + 0.34 * (k ** 0.6)) * cols
        elif r <= shoulder_end:
            k = (r - hood_end) / max(shoulder_end - hood_end, 1)
            half = (0.44 + 0.14 * k) * cols
        else:
            k = (r - shoulder_end) / max(rows - shoulder_end, 1)
            half = (0.58 - 0.10 * k) * cols
        c0 = cols / 2 - half
        c1 = cols / 2 + half
        for c in range(cols):
            if c0 <= c <= c1:
                # face void: dark hollow inside the hood
                in_face = (0.16*rows <= r <= 0.34*rows) and (cols*0.30 <= c <= cols*0.70)
                edge = (c < c0 + 1 or c > c1 - 1)
                cells.append((r, c, "face" if in_face else ("edge" if edge else "fill")))
    rects = []
    for r, c, kind in cells:
        x, y = c*cell, r*rows_h
        if kind == "face":
            shade = random.choice([BG, BG, "#06150a"])
            op = 1
        else:
            shade = random.choice([GREEN, GREEN, GREEN_DIM, "#28e30f", "#0c4a08"])
            op = round(random.uniform(0.55, 1), 2)
        rects.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell*0.82:.1f}" height="{rows_h*0.82:.1f}" '
                     f'fill="{shade}" fill-opacity="{op}"/>')
    frame, bar_h = frame_open(w, h, "", bar=False, rx=10)
    svg = frame + "\n" + "\n".join(rects) + "\n" + frame_close()
    write(path, svg)

gen_avatar(f"{OUT}/avatar-whoami.svg")

terminal_panel(f"{OUT}/panel-whoami-bio.svg",
    lines=[
        [("Hey, I'm ", WHITE, False), ("Joem Bolinas", GREEN, True), (".", WHITE, False)],
        [("", WHITE, False)],
        [("BSIT Student majoring in", WHITE, False)],
        [("Network & Cybersecurity.", WHITE, False)],
        [("", WHITE, False)],
        [("I bridge operations, data, and", WHITE, False)],
        [("technology to solve real-world", WHITE, False)],
        [("problems.", WHITE, False)],
        [("", WHITE, False)],
        [("Always learning.", GREEN_DIM, False)],
        [("Always building.", GREEN_DIM, False)],
        [("Always improving.", GREEN_DIM, False)],
    ],
    width=600, title="", pad_top=22, line_h=24.5, size=15, bar=False)

print("whoami done")

# =====================================================================
# 3) CURRENT MISSION LOG
# =====================================================================
STATUS_COLOR = {"ACTIVE": GREEN, "QUEUED": GRAY, "ONGOING": "#ffd23f"}
def status_line(label, dots, status):
    return [(f"[+] {label} ", WHITE, False), (dots, GREEN_DIM, False),
            (f" [{status}]", STATUS_COLOR[status], True)]

mission_lines = [
    [("[*] boot sequence initiated...", GRAY, False)],
    [("[*] loading modules...", GRAY, False)],
    status_line("linux fundamentals", "."*17, "ACTIVE"),
    status_line("networking & security basics", "."*9, "ACTIVE"),
    status_line("web application security", "."*12, "QUEUED"),
    status_line("exploitation & privilege escalation", "."*2, "QUEUED"),
    status_line("ctf rooms & challenges", "."*15, "ONGOING"),
    [("", WHITE, False)],
    [("[>] ", GREEN, True), ("current objective: ", GREEN, True),
     ("build skills, secure systems,", WHITE, False)],
    [("    automate tasks, and create impact.", WHITE, False)],
]
terminal_panel(f"{OUT}/panel-mission-log.svg", mission_lines,
               width=600, title="", pad_top=22, line_h=23, size=13.6, bar=False)

# =====================================================================
# 4) CAREER TIMELINE
# =====================================================================
TIMELINE = [
    ("2016", "Customer Service / Food Service"),
    ("2017", "Inventory Operations"),
    ("2021", "S&R Receiving / Data Encoding"),
    ("2023", "Resumed BSIT Studies"),
    ("2023", "AllHome Receiving Encoder"),
    ("2025", "Network & Cybersecurity Specialization"),
    ("2026+","Building projects, labs, and real-world experience"),
]
def gen_timeline(path, items, width=600):
    row_h = 40
    pad_top = 22
    height = pad_top + row_h*len(items) + 14
    svg_open, _ = frame_open(width, height, "", bar=False)
    parts = [svg_open]
    yr_x = 24
    dot_x = 108
    label_x = 128
    # connecting line
    y0 = pad_top + 8
    y1 = pad_top + row_h*(len(items)-1) + 8
    parts.append(f'<line x1="{dot_x}" y1="{y0}" x2="{dot_x}" y2="{y1}" stroke="{GREEN}" stroke-opacity="0.45" stroke-width="2"/>')
    for i, (yr, label) in enumerate(items):
        y = pad_top + row_h*i + 8
        parts.append(f'<text x="{yr_x}" y="{y+5}" font-size="14.5" fill="{GREEN}" font-weight="700">{esc(yr)}</text>')
        parts.append(f'<circle cx="{dot_x}" cy="{y}" r="5.5" fill="{BG}" stroke="{GREEN}" stroke-width="2.4"/>')
        # wrap long labels at ~46 chars
        words = label.split(" ")
        wlines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if len(test) > 40:
                wlines.append(cur); cur = w
            else:
                cur = test
        if cur: wlines.append(cur)
        for li, wl in enumerate(wlines):
            parts.append(f'<text x="{label_x}" y="{y+5+li*18}" font-size="13.6" fill="{WHITE}">{esc(wl)}</text>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_timeline(f"{OUT}/panel-career-timeline.svg", TIMELINE)

# =====================================================================
# 5) FINGER PANEL + fingerprint glyph
# =====================================================================
finger_lines = [
    [("Login   : ", GRAY, False), ("joembolinas", WHITE, False)],
    [("Role    : ", GRAY, False), ("IT Student | Future Cybersecurity Analyst", WHITE, False)],
    [("Shell   : ", GRAY, False), ("/bin/bash", WHITE, False)],
    [("Focus   : ", GRAY, False), ("Networking, Security, Automation, Data", WHITE, False)],
    [("Location: ", GRAY, False), ("Philippines \U0001F1F5\U0001F1ED", WHITE, False)],
]
terminal_panel(f"{OUT}/panel-finger.svg", finger_lines,
               width=560, title="", pad_top=24, line_h=25, size=14, bar=False)

def gen_fingerprint(path, w=170, h=170):
    cx, cy = w/2, h/2
    parts = []
    svg_open, _ = frame_open(w, h, "", bar=False, rx=12)
    parts.append(svg_open)
    for i, r in enumerate(range(18, 78, 9)):
        gap = 28 + (i % 3) * 10
        parts.append(f'<path d="M {cx-r},{cy-8} A {r},{r} 0 1 1 {cx-r},{cy+8}" '
                     f'fill="none" stroke="{GREEN}" stroke-opacity="{0.45+0.07*i:.2f}" '
                     f'stroke-width="3" stroke-linecap="round" '
                     f'transform="rotate({(-90)},{cx},{cy})"/>')
    for i, r in enumerate(range(14, 74, 9)):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                     f'stroke="{GREEN}" stroke-opacity="{0.30+0.06*i:.2f}" stroke-width="2.6" '
                     f'stroke-dasharray="{18+i*4} {6+i}"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{GREEN}"/>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_fingerprint(f"{OUT}/icon-fingerprint.svg")
print("mission/career/finger done")

# =====================================================================
# 6) STATS MINI-CARDS  (contributions / repos / followers)
# =====================================================================
def icon_glyph(kind, cx, cy, s, color=GREEN):
    """Tiny inline vector glyphs (no external logo deps)."""
    if kind == "terminal":
        return (f'<rect x="{cx-s}" y="{cy-s*0.7}" width="{s*2}" height="{s*1.4}" rx="4" '
                f'fill="none" stroke="{color}" stroke-width="2"/>'
                f'<path d="M {cx-s*0.55},{cy-s*0.2} l {s*0.35},{s*0.2} l -{s*0.35},{s*0.2}" '
                f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<line x1="{cx+s*0.05}" y1="{cy+s*0.35}" x2="{cx+s*0.55}" y2="{cy+s*0.35}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
    if kind == "repo":
        return (f'<rect x="{cx-s*0.75}" y="{cy-s}" width="{s*1.5}" height="{s*2}" rx="3" '
                f'fill="none" stroke="{color}" stroke-width="2"/>'
                f'<line x1="{cx-s*0.75}" y1="{cy-s*0.35}" x2="{cx+s*0.75}" y2="{cy-s*0.35}" stroke="{color}" stroke-width="1.6"/>'
                f'<line x1="{cx-s*0.3}" y1="{cy+s*0.15}" x2="{cx+s*0.3}" y2="{cy+s*0.15}" stroke="{color}" stroke-width="1.6"/>'
                f'<line x1="{cx-s*0.3}" y1="{cy+s*0.5}" x2="{cx+s*0.15}" y2="{cy+s*0.5}" stroke="{color}" stroke-width="1.6"/>')
    if kind == "followers":
        return (f'<circle cx="{cx-s*0.35}" cy="{cy-s*0.45}" r="{s*0.42}" fill="none" stroke="{color}" stroke-width="2"/>'
                f'<path d="M {cx-s*0.95},{cy+s*0.7} q 0,-{s*0.75} {s*0.6},-{s*0.75} q {s*0.6},0 {s*0.6},{s*0.75}" '
                f'fill="none" stroke="{color}" stroke-width="2"/>'
                f'<circle cx="{cx+s*0.45}" cy="{cy-s*0.3}" r="{s*0.34}" fill="none" stroke="{color}" stroke-opacity="0.6" stroke-width="2"/>'
                f'<path d="M {cx},{cy+s*0.7} q 0,-{s*0.62} {s*0.5},-{s*0.62} q {s*0.5},0 {s*0.5},{s*0.62}" '
                f'fill="none" stroke="{color}" stroke-opacity="0.6" stroke-width="2"/>')
    return ""

def gen_stat_card(path, kind, label, value, w=260, h=88):
    svg_open, _ = frame_open(w, h, "", bar=False, rx=10)
    parts = [svg_open]
    parts.append(icon_glyph(kind, 40, h/2, 16))
    parts.append(f'<text x="74" y="{h/2-6}" font-size="13" fill="{GRAY}">{esc(label)}</text>')
    parts.append(f'<text x="74" y="{h/2+22}" font-size="24" font-weight="700" fill="{GREEN}">{esc(value)}</text>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_stat_card(f"{OUT}/stat-contributions.svg", "terminal", "Total Contributions", "1,234+")
gen_stat_card(f"{OUT}/stat-repos.svg", "repo", "Public Repositories", "26")
gen_stat_card(f"{OUT}/stat-followers.svg", "followers", "Followers", "45+")

# =====================================================================
# 7) TOP LANGUAGES BAR CHART
# =====================================================================
LANGS = [("Python", 43.2), ("Java", 24.7), ("Django", 8.9), ("JavaScript", 7.1), ("HTML", 5.2)]
def gen_lang_chart(path, langs, w=420, h=190):
    svg_open, _ = frame_open(w, h, "Top Languages", bg=BG, rx=10)
    parts = [svg_open]
    bar_x = 110
    bar_max = w - bar_x - 70
    y = 56
    row_h = 26
    for name, pct in langs:
        bw = bar_max * (pct/45)
        parts.append(f'<text x="20" y="{y+5}" font-size="13" fill="{WHITE}">{esc(name)}</text>')
        parts.append(f'<rect x="{bar_x}" y="{y-9}" width="{bar_max}" height="9" rx="4" fill="{BORDER}"/>')
        parts.append(f'<rect x="{bar_x}" y="{y-9}" width="{bw:.1f}" height="9" rx="4" fill="{GREEN}"/>')
        parts.append(f'<text x="{bar_x+bar_max+10}" y="{y+5}" font-size="12.5" fill="{GRAY}">{pct}%</text>')
        y += row_h
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_lang_chart(f"{OUT}/chart-top-languages.svg", LANGS)
print("stats done")

# =====================================================================
# 8) PROJECT CARDS
# =====================================================================
def proj_icon(kind, cx, cy, s):
    g = GREEN
    if kind == "moto":
        return (f'<circle cx="{cx-s*0.55}" cy="{cy+s*0.4}" r="{s*0.32}" fill="none" stroke="{g}" stroke-width="2"/>'
                f'<circle cx="{cx+s*0.55}" cy="{cy+s*0.4}" r="{s*0.32}" fill="none" stroke="{g}" stroke-width="2"/>'
                f'<path d="M {cx-s*0.55},{cy+s*0.4} l {s*0.3},-{s*0.5} h {s*0.4} m -{s*0.15},-{s*0.15} l {s*0.4},{s*0.65} m -{s*0.55},0 h {s*0.65} l {s*0.3},{s*0.4}" '
                f'fill="none" stroke="{g}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "network":
        pts = [(cx, cy-s*0.55), (cx-s*0.5, cy+s*0.35), (cx+s*0.5, cy+s*0.35)]
        out = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{g}"/>' for x, y in pts)
        out += f'<circle cx="{cx}" cy="{cy}" r="4" fill="{g}" fill-opacity="0.7"/>'
        for x, y in pts:
            out += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{g}" stroke-width="2"/>'
        return out
    if kind == "collab":
        out = ""
        for dx in (-s*0.5, 0, s*0.5):
            out += f'<circle cx="{cx+dx}" cy="{cy}" r="5" fill="{g}" fill-opacity="0.85"/>'
        out += (f'<path d="M {cx-s*0.5},{cy} a {s*0.5},{s*0.5} 0 0 1 {s*0.5},-{s*0.45}" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<path d="M {cx+s*0.5},{cy} a {s*0.5},{s*0.5} 0 0 0 -{s*0.5},-{s*0.45}" fill="none" stroke="{g}" stroke-width="2"/>')
        return out
    if kind == "notes":
        return (f'<rect x="{cx-s*0.55}" y="{cy-s*0.7}" width="{s*1.1}" height="{s*1.4}" rx="3" fill="none" stroke="{g}" stroke-width="2"/>'
                f'<line x1="{cx-s*0.32}" y1="{cy-s*0.3}" x2="{cx+s*0.32}" y2="{cy-s*0.3}" stroke="{g}" stroke-width="1.6"/>'
                f'<line x1="{cx-s*0.32}" y1="{cy}" x2="{cx+s*0.32}" y2="{cy}" stroke="{g}" stroke-width="1.6"/>'
                f'<line x1="{cx-s*0.32}" y1="{cy+s*0.3}" x2="{cx+s*0.05}" y2="{cy+s*0.3}" stroke="{g}" stroke-width="1.6"/>')
    if kind == "ai":
        out = f'<circle cx="{cx}" cy="{cy}" r="{s*0.32}" fill="none" stroke="{g}" stroke-width="2"/>'
        for ang in (0,60,120,180,240,300):
            import math
            x2 = cx + s*0.62*math.cos(math.radians(ang)); y2 = cy + s*0.62*math.sin(math.radians(ang))
            out += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{g}" stroke-width="1.6" stroke-opacity="0.8"/>'
            out += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3" fill="{g}"/>'
        return out
    if kind == "chart":
        bars = [0.35, 0.6, 0.45, 0.75]
        out = ""
        bx = cx - s*0.6
        for i, bh in enumerate(bars):
            out += f'<rect x="{bx+i*s*0.35:.1f}" y="{cy+s*0.6-s*1.2*bh:.1f}" width="{s*0.22}" height="{s*1.2*bh:.1f}" fill="{g}" fill-opacity="{0.5+0.15*i:.2f}"/>'
        out += f'<line x1="{bx-4}" y1="{cy+s*0.6}" x2="{bx+s*1.5}" y2="{cy+s*0.6}" stroke="{g}" stroke-width="1.6"/>'
        return out
    return ""

def gen_project_card(path, kind, title, desc, w=270, h=168):
    svg_open, _ = frame_open(w, h, "", bar=False, rx=10)
    parts = [svg_open]
    parts.append(proj_icon(kind, 34, 38, 22))
    # title (wrap)
    words, lines, cur = title.split(" "), [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if text_w(test, 14.5) > w - 64:
            lines.append(cur); cur = word
        else:
            cur = test
    if cur: lines.append(cur)
    ty = 26
    for i, ln in enumerate(lines):
        parts.append(f'<text x="64" y="{ty+i*19}" font-size="14.5" font-weight="700" fill="{GREEN}">{esc(ln)}</text>')
    # description (wrap)
    dwords, dlines, cur = desc.split(" "), [], ""
    for word in dwords:
        test = (cur + " " + word).strip()
        if text_w(test, 12.5) > w - 40:
            dlines.append(cur); cur = word
        else:
            cur = test
    if cur: dlines.append(cur)
    dy = max(ty + len(lines)*19, 64) + 12
    for i, dl in enumerate(dlines):
        parts.append(f'<text x="20" y="{dy+i*18}" font-size="12.5" fill="{GRAY}">{esc(dl)}</text>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

PROJECTS = [
    ("moto",    "MotorPH Payroll System",      "Django + MySQL payroll management for MotorPH.",       "card-project-motorph"),
    ("network", "FinMark Network Architecture","Secure network design for a financial company.",       "card-project-finmark"),
    ("collab",  "Connectly Project",           "Collaboration platform for teams.",                    "card-project-connectly"),
    ("notes",   "Cybersecurity Lab Notes",     "Documenting labs, tools, and key takeaways.",           "card-project-cyberlab"),
    ("ai",      "AI Study Assistant System",   "NotebookLM + AI workflows for smarter learning.",       "card-project-ai-study"),
    ("chart",   "Inventory Analytics Dashboard","Excel/Sheets dashboard for inventory insights.",       "card-project-inventory"),
]
for kind, title, desc, fname in PROJECTS:
    gen_project_card(f"{OUT}/{fname}.svg", kind, title, desc)

print("projects done")

# =====================================================================
# 9) SKILL CATEGORY PANELS
# =====================================================================
import math
def skill_icon(kind, cx, cy, s, color):
    g = color
    if kind == "kali":
        return (f'<path d="M {cx-s*0.7},{cy-s*0.5} q {s*0.7},{s*1.2} {s*1.4},0" fill="none" stroke="{g}" stroke-width="2.2" stroke-linecap="round"/>'
               f'<path d="M {cx-s*0.45},{cy-s*0.7} q {s*0.45},{s*1.3} {s*0.9},0" fill="none" stroke="{g}" stroke-width="1.6" stroke-opacity="0.7" stroke-linecap="round"/>')
    if kind == "nmap":
        out = f'<circle cx="{cx}" cy="{cy}" r="{s*0.7}" fill="none" stroke="{g}" stroke-width="2"/>'
        out += f'<circle cx="{cx}" cy="{cy}" r="{s*0.22}" fill="{g}"/>'
        out += f'<line x1="{cx+s*0.5}" y1="{cy+s*0.5}" x2="{cx+s*0.95}" y2="{cy+s*0.95}" stroke="{g}" stroke-width="2.4" stroke-linecap="round"/>'
        return out
    if kind == "wireshark":
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.85}" ry="{s*0.55}" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<circle cx="{cx}" cy="{cy}" r="{s*0.18}" fill="{g}"/>')
    if kind == "burp":
        return (f'<circle cx="{cx}" cy="{cy}" r="{s*0.7}" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<path d="M {cx},{cy-s*0.4} L {cx-s*0.3},{cy+s*0.15} L {cx+s*0.05},{cy+s*0.15} L {cx-s*0.15},{cy+s*0.5}" '
               f'fill="none" stroke="{g}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>')
    if kind == "thm":
        return (f'<path d="M {cx-s*0.6},{cy+s*0.5} L {cx-s*0.6},{cy-s*0.1} L {cx},{cy-s*0.65} L {cx+s*0.6},{cy-s*0.1} L {cx+s*0.6},{cy+s*0.5} Z" '
               f'fill="none" stroke="{g}" stroke-width="2" stroke-linejoin="round"/>')
    if kind == "sap":
        return f'<text x="{cx}" y="{cy+s*0.32}" font-size="{s*0.9}" font-weight="800" fill="{g}" text-anchor="middle">SAP</text>'
    if kind == "nav":
        out = ""
        for i,(dx,dy) in enumerate([(-0.45,-0.2),(0,-0.5),(0.45,-0.2)]):
            out += f'<rect x="{cx+dx*s-s*0.18}" y="{cy+dy*s}" width="{s*0.36}" height="{s*0.9}" fill="{g}" fill-opacity="{0.5+0.2*i:.2f}" rx="2"/>'
        return out
    if kind == "excel":
        return (f'<rect x="{cx-s*0.6}" y="{cy-s*0.7}" width="{s*1.2}" height="{s*1.4}" rx="3" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<line x1="{cx-s*0.45}" y1="{cy-s*0.5}" x2="{cx+s*0.45}" y2="{cy+s*0.5}" stroke="{g}" stroke-width="1.8"/>'
               f'<line x1="{cx+s*0.45}" y1="{cy-s*0.5}" x2="{cx-s*0.45}" y2="{cy+s*0.5}" stroke="{g}" stroke-width="1.8"/>')
    if kind == "sheets":
        return (f'<rect x="{cx-s*0.55}" y="{cy-s*0.7}" width="{s*1.1}" height="{s*1.4}" rx="3" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<line x1="{cx-s*0.35}" y1="{cy-s*0.3}" x2="{cx+s*0.35}" y2="{cy-s*0.3}" stroke="{g}" stroke-width="1.5"/>'
               f'<line x1="{cx-s*0.35}" y1="{cy}" x2="{cx+s*0.35}" y2="{cy}" stroke="{g}" stroke-width="1.5"/>'
               f'<line x1="{cx-s*0.35}" y1="{cy+s*0.3}" x2="{cx+s*0.35}" y2="{cy+s*0.3}" stroke="{g}" stroke-width="1.5"/>'
               f'<line x1="{cx}" y1="{cy-s*0.4}" x2="{cx}" y2="{cy+s*0.4}" stroke="{g}" stroke-width="1.5"/>')
    if kind == "python":
        return (f'<path d="M {cx-s*0.5},{cy-s*0.15} h{s*0.6} v-{s*0.4} a{s*0.25},{s*0.25} 0 0 0 -{s*0.25},-{s*0.25} h-{s*0.1} a{s*0.25},{s*0.25} 0 0 0 -{s*0.25},{s*0.25} z" fill="{g}"/>'
               f'<path d="M {cx+s*0.5},{cy+s*0.15} h-{s*0.6} v{s*0.4} a{s*0.25},{s*0.25} 0 0 0 {s*0.25},{s*0.25} h{s*0.1} a{s*0.25},{s*0.25} 0 0 0 {s*0.25},-{s*0.25} z" fill="{g}" fill-opacity="0.65"/>')
    if kind == "java":
        return (f'<path d="M {cx-s*0.4},{cy+s*0.5} q {s*0.9},{s*0.25} {s*0.8},-{s*0.15}" fill="none" stroke="{g}" stroke-width="2" stroke-linecap="round"/>'
               f'<path d="M {cx-s*0.15},{cy-s*0.6} q {s*0.5},{s*0.5} -{s*0.05},{s*0.95}" fill="none" stroke="{g}" stroke-width="2" stroke-linecap="round"/>')
    if kind == "django":
        return f'<text x="{cx-s*0.55}" y="{cy+s*0.35}" font-size="{s*1.1}" font-weight="800" fill="{g}">D</text>'
    if kind == "vscode":
        return (f'<path d="M {cx+s*0.6},{cy-s*0.7} L {cx-s*0.2},{cy} L {cx+s*0.6},{cy+s*0.7} L {cx+s*0.25},{cy+s*0.7} L {cx-s*0.65},{cy+s*0.15} L {cx-s*0.85},{cy+s*0.3} L {cx-s*0.95},{cy+s*0.2} L {cx-s*0.55},{cy} L {cx-s*0.95},{cy-s*0.2} L {cx-s*0.85},{cy-s*0.3} L {cx-s*0.65},{cy-s*0.15} L {cx+s*0.25},{cy-s*0.7} Z" '
               f'fill="none" stroke="{g}" stroke-width="1.6" stroke-linejoin="round"/>')
    if kind == "github":
        return (f'<circle cx="{cx}" cy="{cy}" r="{s*0.7}" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<path d="M {cx-s*0.25},{cy+s*0.45} v-{s*0.3} q -{s*0.3},{s*0.05} -{s*0.35},-{s*0.2} q -{s*0.05},-{s*0.2} -{s*0.18},-{s*0.25} M {cx-s*0.25},{cy+s*0.3} q -{s*0.4},{s*0.1} -{s*0.4},-{s*0.35} q 0,-{s*0.15} {s*0.1},-{s*0.25} q -{s*0.04},-{s*0.15} {s*0.1},-{s*0.3} q {s*0.15},0 {s*0.25},{s*0.12} q {s*0.2},-{s*0.06} {s*0.4},0 q {s*0.1},-{s*0.12} {s*0.25},-{s*0.12} q {s*0.14},{s*0.15} {s*0.1},{s*0.3} q {s*0.1},{s*0.1} {s*0.1},{s*0.25} q 0,{s*0.45} -{s*0.4},{s*0.35} q {s*0.1},{s*0.1} {s*0.1},{s*0.25} v{s*0.3}" '
               f'fill="none" stroke="{g}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "linux":
        return (f'<ellipse cx="{cx}" cy="{cy-s*0.1}" rx="{s*0.45}" ry="{s*0.6}" fill="none" stroke="{g}" stroke-width="2"/>'
               f'<circle cx="{cx-s*0.18}" cy="{cy-s*0.25}" r="3" fill="{g}"/>'
               f'<circle cx="{cx+s*0.18}" cy="{cy-s*0.25}" r="3" fill="{g}"/>'
               f'<path d="M {cx-s*0.3},{cy+s*0.55} q {s*0.3},{s*0.25} {s*0.6},0" fill="none" stroke="{g}" stroke-width="2" stroke-linecap="round"/>')
    if kind == "obsidian":
        return (f'<path d="M {cx},{cy-s*0.75} L {cx+s*0.65},{cy} L {cx},{cy+s*0.75} L {cx-s*0.65},{cy} Z" '
               f'fill="none" stroke="{g}" stroke-width="2" stroke-linejoin="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{s*0.5}" fill="{g}"/>'

def gen_skill_panel(path, category_label, items, width=420):
    # items: list of (kind, label, color)
    cols = 3 if len(items) > 4 else len(items)
    cell_w = (width - 40) / cols
    cell_h = 92
    rows = math.ceil(len(items)/cols)
    height = 50 + rows*cell_h
    svg_open, _ = frame_open(width, height, "", bar=False, rx=10)
    parts = [svg_open]
    parts.append(f'<text x="20" y="32" font-size="13.5" fill="{GREEN}" font-weight="700">$ {esc(category_label)}</text>')
    parts.append(f'<line x1="20" y1="42" x2="{width-20}" y2="42" stroke="{BORDER}" stroke-width="1"/>')
    for i, (kind, label, color) in enumerate(items):
        col, row = i % cols, i // cols
        cx = 20 + cell_w*col + cell_w/2
        cy = 70 + cell_h*row
        parts.append(skill_icon(kind, cx, cy-6, 17, color))
        words, lines, cur = label.split(" "), [], ""
        for w in words:
            test=(cur+" "+w).strip()
            if text_w(test, 11.5) > cell_w-6:
                lines.append(cur); cur=w
            else: cur=test
        if cur: lines.append(cur)
        for li, ln in enumerate(lines):
            parts.append(f'<text x="{cx}" y="{cy+22+li*14}" font-size="11.5" fill="{WHITE}" text-anchor="middle">{esc(ln)}</text>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_skill_panel(f"{OUT}/skills-security.svg", "security/", [
    ("kali", "Kali Linux", "#4C82C9"),
    ("nmap", "Nmap", "#4682B4"),
    ("wireshark", "Wireshark", "#3399CC"),
    ("burp", "Burp Suite", "#FF6633"),
    ("thm", "TryHackMe", GREEN),
], width=420)

gen_skill_panel(f"{OUT}/skills-systems.svg", "systems & enterprise/", [
    ("sap", "SAP", "#1FA0DB"),
    ("nav", "MS Dynamics NAV", "#7C4DFF"),
    ("excel", "Excel", "#1D6F42"),
    ("sheets", "Google Sheets", "#0F9D58"),
], width=420)

gen_skill_panel(f"{OUT}/skills-dev.svg", "development/", [
    ("python", "Python", "#FFD43B"),
    ("java", "Java", "#E76F00"),
    ("django", "Django", "#0C4B33"),
], width=420)

gen_skill_panel(f"{OUT}/skills-workflow.svg", "workflow/", [
    ("vscode", "VS Code", "#007ACC"),
    ("github", "GitHub", WHITE),
    ("linux", "Linux", "#FCC624"),
    ("obsidian", "Obsidian", "#7C3AED"),
], width=420)

print("skills done")

# =====================================================================
# 10) CONTACT BAR
# =====================================================================
def contact_icon(kind, cx, cy, s, color):
    if kind == "mail":
        return (f'<rect x="{cx-s}" y="{cy-s*0.7}" width="{s*2}" height="{s*1.4}" rx="3" fill="none" stroke="{color}" stroke-width="2"/>'
               f'<path d="M {cx-s},{cy-s*0.6} L {cx},{cy+s*0.1} L {cx+s},{cy-s*0.6}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>')
    if kind == "linkedin":
        return (f'<rect x="{cx-s}" y="{cy-s}" width="{s*2}" height="{s*2}" rx="4" fill="none" stroke="{color}" stroke-width="2"/>'
               f'<circle cx="{cx-s*0.45}" cy="{cy-s*0.4}" r="2.6" fill="{color}"/>'
               f'<line x1="{cx-s*0.45}" y1="{cy-s*0.1}" x2="{cx-s*0.45}" y2="{cy+s*0.5}" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
               f'<path d="M {cx-s*0.05},{cy+s*0.5} v-{s*0.35} q 0,-{s*0.3} {s*0.3},-{s*0.3} q {s*0.3},0 {s*0.3},{s*0.3} v{s*0.35}" '
               f'fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>')
    if kind == "github":
        return skill_icon("github", cx, cy, s, color)
    return ""

def gen_contact_bar(path, items, width=860, h=64):
    n = len(items)
    seg = width / n
    svg_open, _ = frame_open(width, h, "", bar=False, rx=12)
    parts = [svg_open]
    for i, (kind, label, color) in enumerate(items):
        cx0 = seg*i + 30
        parts.append(contact_icon(kind, cx0, h/2, 12, color))
        parts.append(f'<text x="{cx0+24}" y="{h/2+5}" font-size="13.5" fill="{WHITE}">{esc(label)}</text>')
        if i < n-1:
            parts.append(f'<line x1="{seg*(i+1)}" y1="14" x2="{seg*(i+1)}" y2="{h-14}" stroke="{BORDER}" stroke-width="1"/>')
    parts.append(frame_close())
    write(path, "\n".join(parts))

gen_contact_bar(f"{OUT}/contact-bar.svg", [
    ("mail", "joembolinas23@gmail.com", GREEN),
    ("linkedin", "linkedin.com/in/joembolinas", "#0A66C2"),
    ("github", "github.com/joembolinas", WHITE),
], width=860)

print("ALL DONE")






