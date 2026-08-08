#!/usr/bin/env python3
"""Genera el banner synthwave del perfil de GitHub."""
import math, os, sys

W, H = 1280, 420
HORIZON = 250
VPX, VPY = W / 2, HORIZON  # punto de fuga

out = []
w = out.append

w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'role="img" aria-label="Jesus Ricardo Rosales — Software Developer">')

# ── defs ────────────────────────────────────────────────────────────────────
w('<defs>')
w('''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#160029"/>
  <stop offset="55%" stop-color="#3b0a52"/>
  <stop offset="100%" stop-color="#7a1a5e"/>
</linearGradient>''')
w('''<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ffe259"/>
  <stop offset="45%" stop-color="#ff8a3d"/>
  <stop offset="100%" stop-color="#ff2e9a"/>
</linearGradient>''')
w('''<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#1b0033"/>
  <stop offset="100%" stop-color="#070010"/>
</linearGradient>''')
w('''<linearGradient id="gridfade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0.15"/>
  <stop offset="35%" stop-color="#ffffff" stop-opacity="0.75"/>
  <stop offset="100%" stop-color="#ffffff" stop-opacity="1"/>
</linearGradient>''')
w('<mask id="gridmask"><rect x="0" y="%d" width="%d" height="%d" fill="url(#gridfade)"/></mask>'
  % (HORIZON, W, H - HORIZON))
# resplandor neón
w('''<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="7" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>''')
w('''<filter id="softglow" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="16"/>
</filter>''')
# el sol se recorta en bandas horizontales
w('<clipPath id="sunbands">')
y = HORIZON - 92
band = 13
i = 0
while y < HORIZON:
    gap = 2 + i * 1.6           # las bandas se separan hacia abajo
    w(f'<rect x="{VPX-100}" y="{y:.1f}" width="200" height="{max(band-gap,1.5):.1f}"/>')
    y += band
    i += 1
w('</clipPath>')
w('</defs>')

# ── cielo y estrellas ───────────────────────────────────────────────────────
w(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
stars = [(97, 38, 1.4), (210, 72, 1.0), (318, 30, 1.7), (405, 96, 1.1), (150, 130, 1.0),
         (60, 175, 1.3), (930, 44, 1.5), (1035, 88, 1.1), (1140, 34, 1.6), (1215, 120, 1.2),
         (860, 150, 1.0), (1190, 190, 1.3), (740, 40, 1.1), (520, 58, 1.2), (275, 190, 1.0)]
for sx, sy, sr in stars:
    w(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#fff" opacity="0.75"/>')

# ── sol ─────────────────────────────────────────────────────────────────────
w(f'<circle cx="{VPX}" cy="{HORIZON-5}" r="95" fill="#ff2e9a" opacity="0.35" filter="url(#softglow)"/>')
w(f'<g clip-path="url(#sunbands)"><circle cx="{VPX}" cy="{HORIZON-5}" r="92" fill="url(#sun)"/></g>')

# ── suelo ───────────────────────────────────────────────────────────────────
w(f'<rect x="0" y="{HORIZON}" width="{W}" height="{H-HORIZON}" fill="url(#floor)"/>')
w(f'<rect x="0" y="{HORIZON-1.5}" width="{W}" height="3" fill="#ff5fc8" filter="url(#glow)"/>')

# rejilla en perspectiva
w('<g mask="url(#gridmask)" stroke="#00e5ff" stroke-opacity="0.55" fill="none">')
for k in range(-14, 15):                       # líneas que convergen al punto de fuga
    x_bottom = VPX + k * 128
    w(f'<line x1="{VPX}" y1="{VPY}" x2="{x_bottom:.1f}" y2="{H}" stroke-width="1.4"/>')
d = 0.0
step = 3.2
while True:                                     # líneas horizontales, más juntas al fondo
    d += step
    step *= 1.34
    yy = HORIZON + d
    if yy > H:
        break
    w(f'<line x1="0" y1="{yy:.1f}" x2="{W}" y2="{yy:.1f}" stroke-width="1.4"/>')
w('</g>')

# ── texto ───────────────────────────────────────────────────────────────────
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"
# textLength fija el ancho: el banner no se rompe aunque el navegador sustituya la fuente
NAME, SUB, STACK = "JESUS RICARDO ROSALES", "SOFTWARE DEVELOPER", "C · PYTHON · SQL · LINUX · 42 PORTO"
for fill, extra in (("#ff2e9a", ' opacity="0.85" filter="url(#glow)"'), ("#ffffff", "")):
    w(f'<text x="{VPX}" y="112" text-anchor="middle" font-family="{FONT}" font-size="58" '
      f'font-weight="bold" textLength="960" lengthAdjust="spacingAndGlyphs" fill="{fill}"{extra}>'
      f'{NAME}</text>')
w(f'<text x="{VPX}" y="152" text-anchor="middle" font-family="{FONT}" font-size="20" '
  f'textLength="470" lengthAdjust="spacingAndGlyphs" fill="#00e5ff" filter="url(#glow)">{SUB}</text>')
w(f'<text x="{VPX}" y="{H-36}" text-anchor="middle" font-family="{FONT}" font-size="16" '
  f'textLength="620" lengthAdjust="spacingAndGlyphs" fill="#c9a7ff" opacity="0.9">{STACK}</text>')

w('</svg>')

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banner.svg")
open(path, "w", encoding="utf-8").write("\n".join(out))
print("escrito", path, os.path.getsize(path), "bytes")
