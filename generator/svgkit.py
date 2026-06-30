"""
svgkit.py — tiny toolkit for generating the terminal/hacker-themed
SVG assets used in the joembolinas GitHub profile README.

Pure stdlib, no deps. Every function returns/writes a self-contained
SVG string (safe to render via <img src="..."> on GitHub).
"""
import html
import os

# ---------------------------------------------------------------- palette
BG       = "#05070a"      # panel / card background
BG_DEEP  = "#000000"      # outer page bg (banners)
GREEN    = "#39FF14"      # neon accent
GREEN_DIM= "#1f8c0d"
WHITE    = "#e9f5e9"      # body copy
GRAY     = "#7d8b7d"      # secondary / muted copy
BORDER   = "#1c3a14"      # faint green border
FONT     = "'JetBrains Mono','Fira Code',Consolas,'SFMono-Regular',Menlo,monospace"

CHAR_W_RATIO = 0.60  # monospace width approximation, * font-size

def esc(s):
    return html.escape(s, quote=True)

def text_w(s, size):
    return int(len(s) * size * CHAR_W_RATIO)

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- frame
def frame_open(width, height, title, rx=10, bg=BG, border=GREEN, border_op=0.55,
                bar=True, extra_defs=""):
    bar_h = 30 if bar else 0
    parts = []
    parts.append(f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
                  f'xmlns="http://www.w3.org/2000/svg">')
    parts.append(f'<defs>{extra_defs}</defs>')
    parts.append(f'<style>text{{font-family:{FONT};}}</style>')
    parts.append(f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="{rx}" '
                 f'fill="{bg}" stroke="{border}" stroke-opacity="{border_op}" stroke-width="1.4"/>')
    if bar:
        parts.append(f'<path d="M1,{rx+1} a{rx},{rx} 0 0 1 {rx},-{rx} h{width-2*rx-2} '
                     f'a{rx},{rx} 0 0 1 {rx},{rx} v{bar_h-rx} h-{width-2} z" '
                     f'fill="{border}" fill-opacity="0.10"/>')
        parts.append(f'<line x1="0" y1="{bar_h}" x2="{width}" y2="{bar_h}" '
                     f'stroke="{border}" stroke-opacity="0.5" stroke-width="1"/>')
        for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
            parts.append(f'<circle cx="{18+i*16}" cy="{bar_h/2}" r="5" fill="{c}" fill-opacity="0.85"/>')
        if title:
            parts.append(f'<text x="{width/2}" y="{bar_h/2+4}" text-anchor="middle" '
                         f'font-size="12" fill="{GRAY}">{esc(title)}</text>')
    return "\n".join(parts), bar_h

def frame_close():
    return "</svg>"

# ---------------------------------------------------------------- 1. typing banner (H2 headers)
def typing_banner(path, prompt, width=860, height=46, size=19, dur=5.0,
                   color=GREEN, bg="transparent"):
    """Single-line SVG that 'types' `prompt` then erases, looping forever."""
    pad_x = 14
    full_w = text_w(prompt, size)
    cursor_x = pad_x + full_w + 4
    type_end   = dur * 0.42
    hold_end   = dur * 0.62
    erase_end  = dur * 0.92
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"
     xmlns="http://www.w3.org/2000/svg">
  <style>
    text{{font-family:{FONT}; font-weight:700;}}
    .cursor{{animation:blink 1s steps(1) infinite;}}
    @keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
  </style>
  <rect width="{width}" height="{height}" fill="{bg}"/>
  <line x1="2" y1="{height-3}" x2="{width-2}" y2="{height-3}" stroke="{color}" stroke-opacity="0.35" stroke-width="1.5"/>
  <clipPath id="reveal">
    <rect x="0" y="0" height="{height}" width="0">
      <animate attributeName="width"
        values="0;{full_w+6};{full_w+6};0;0"
        keyTimes="0;{type_end/dur:.3f};{hold_end/dur:.3f};{erase_end/dur:.3f};1"
        dur="{dur}s" repeatCount="indefinite"/>
    </rect>
  </clipPath>
  <g clip-path="url(#reveal)">
    <text x="{pad_x}" y="{height/2+size*0.34}" font-size="{size}" fill="{color}">{esc(prompt)}</text>
  </g>
  <rect class="cursor" x="{cursor_x}" y="{height/2-size*0.6}" width="{size*0.5}" height="{size*0.95}" fill="{color}"/>
</svg>'''
    write(path, svg)

# ---------------------------------------------------------------- generic multi-line terminal panel
def terminal_panel(path, lines, width=860, title="joembolinas@kali:~$", line_h=24,
                    pad_top=46, pad_x=20, size=14.5, bg=BG, extra_h=0, bar=True):
    height = pad_top + line_h * len(lines) + 16 + extra_h
    svg_open, bar_h = frame_open(width, height, title, bg=bg, bar=bar)
    body = []
    y = pad_top
    for ln in lines:
        segs = ln if isinstance(ln, list) else [(ln, WHITE, False)]
        x = pad_x
        row = [f'<text x="{x}" y="{y}" font-size="{size}">']
        inline = []
        for seg_text, color, bold in segs:
            w = "700" if bold else "400"
            inline.append(f'<tspan fill="{color}" font-weight="{w}">{esc(seg_text)}</tspan>')
        row.append("".join(inline))
        row.append("</text>")
        body.append("".join(row))
        y += line_h
    svg = svg_open + "\n" + "\n".join(body) + "\n" + frame_close()
    write(path, svg)
    return width, height
