#!/usr/bin/env python3
"""Generate every SVG used by profile/README.md.

    python3 -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python tools/build_assets.py

Output lands in profile/assets/. Content is taken from inzox.com, inzox.ai
and the INZOX website source; keep it in sync when the company copy changes.
"""

import json
import math
import os

from brand import C, chip, esc, measure, stars, svg, text

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile", "assets")
W = 1280


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"{name:28s} {len(content) / 1024:7.1f} KB")


def typing_clip(cid, x, y, h, text_w, n_chars, start, per, hold, dur):
    """clipPath whose width grows one character at a time, then resets."""
    cw = text_w / max(n_chars, 1)
    vals, times = ["0"], [0.0]
    t = start
    for i in range(1, n_chars + 1):
        vals.append(f"{cw * i:.1f}")
        times.append(t / dur)
        t += per
    vals.append(f"{text_w + 4:.1f}")
    times.append(min((t + hold) / dur, 0.999))
    vals.append("0")
    times.append(1.0)
    kt = ";".join(f"{k:.4f}" for k in times)
    clip = (
        f'<clipPath id="{cid}"><rect x="{x}" y="{y}" height="{h}" width="0">'
        f'<animate attributeName="width" dur="{dur}s" repeatCount="indefinite" calcMode="discrete" '
        f'values="{";".join(vals)}" keyTimes="{kt}"/>'
        f"</rect></clipPath>"
    )
    caret = (
        f'<animate attributeName="x" dur="{dur}s" repeatCount="indefinite" calcMode="discrete" '
        f'values="{";".join(f"{x + 3 + float(v):.1f}" for v in vals)}" keyTimes="{kt}"/>'
    )
    return clip, caret


# --------------------------------------------------------------------- hero
def hero():
    H = 560
    cx, cy = 915, 262
    defs = f"""
<linearGradient id="wm" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="{C['ice']}"/>
  <stop offset="1" stop-color="{C['blue']}"/></linearGradient>
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="0" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/>
  <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1400 0;1400 0" keyTimes="0;.55;1" dur="6s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="{C['aqua']}"/><stop offset="1" stop-color="{C['violet']}"/></linearGradient>
<linearGradient id="minutes" gradientUnits="userSpaceOnUse" x1="410" y1="0" x2="580" y2="0"><stop offset="0" stop-color="{C['aqua']}"/><stop offset="1" stop-color="{C['blue']}"/></linearGradient>
<radialGradient id="coreglow"><stop offset="0" stop-color="{C['aqua']}" stop-opacity=".55"/><stop offset=".4" stop-color="{C['blue']}" stop-opacity=".18"/><stop offset="1" stop-color="{C['blue']}" stop-opacity="0"/></radialGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['aqua']}" stop-opacity="0"/><stop offset="1" stop-color="{C['aqua']}" stop-opacity=".35"/></linearGradient>
<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
<mask id="floormask"><rect x="0" y="392" width="{W}" height="{H - 392}" fill="url(#floorfade)"/></mask>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['aqua']}"/><stop offset=".5" stop-color="{C['blue']}"/><stop offset="1" stop-color="{C['violet']}"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>
"""
    term_cmd = "inzox deliver --weeks-to-minutes"
    cmd_w = measure(term_cmd, "IZ Mono", 16)
    clip, caret = typing_clip("type", 162, 430, 30, cmd_w, len(term_cmd), 0.6, 0.07, 3.6, 7)
    defs += clip

    css = f"""
.core1{{transform-origin:{cx}px {cy}px;animation:spin 48s linear infinite}}
.core2{{transform-origin:{cx}px {cy}px;animation:spin 26s linear infinite reverse}}
.core3{{transform-origin:{cx}px {cy}px;animation:spin 14s linear infinite}}
.radar{{transform-origin:{cx}px {cy}px;animation:spin 7s linear infinite}}
.ok{{animation:okfade 7s linear infinite}}
@keyframes okfade{{0%,47%{{opacity:0}}52%,94%{{opacity:1}}100%{{opacity:0}}}}
.lbl{{animation:pulse 3.2s ease-in-out infinite}}
"""

    b = []
    b.append(stars(W, H, 90, seed=11, ymax=390))

    # perspective floor: rays from vanishing point + rolling horizontal lines
    vx, vy, hz = 640, 300, 392
    floor = []
    for i in range(-24, 25):
        x2 = vx + i * 120
        t = (hz - vy) / (H - vy)
        x1 = vx + (x2 - vx) * t
        floor.append(f'<line x1="{x1:.1f}" y1="{hz}" x2="{x2:.1f}" y2="{H}"/>')
    ys = [hz + (H - hz) * (k / 9) ** 1.9 for k in range(0, 11)]
    for k in range(len(ys) - 1):
        dy = ys[k + 1] - ys[k]
        floor.append(
            f'<line x1="0" x2="{W}" y1="{ys[k]:.1f}" y2="{ys[k]:.1f}">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {dy:.1f}" dur="2.4s" repeatCount="indefinite"/></line>'
        )
    b.append(
        f'<g mask="url(#floormask)" stroke="{C["blue"]}" stroke-opacity=".45" stroke-width="1">{"".join(floor)}</g>'
        f'<line x1="0" x2="{W}" y1="{hz}" y2="{hz}" stroke="url(#accent)" stroke-opacity=".7"/>'
    )

    # ---- core (right): ZOX-style reticle rings
    core = [f'<circle cx="{cx}" cy="{cy}" r="230" fill="url(#coreglow)"/>']
    core.append(
        f'<g class="radar"><path d="M{cx},{cy} L{cx + 205},{cy} A205,205 0 0,0 {cx + 205 * math.cos(math.radians(-38)):.1f},{cy + 205 * math.sin(math.radians(-38)):.1f} Z" fill="url(#sweep)" opacity=".7"/></g>'
    )
    core.append(
        f'<g class="core1"><circle cx="{cx}" cy="{cy}" r="205" stroke="{C["sky"]}" stroke-opacity=".35" stroke-dasharray="2 7"/>'
        + "".join(
            f'<circle cx="{cx + 205 * math.cos(math.radians(a)):.1f}" cy="{cy + 205 * math.sin(math.radians(a)):.1f}" r="{r}" fill="{col}"/>'
            for a, r, col in [(20, 4, C["aqua"]), (140, 3, C["violet"]), (250, 3.5, C["sky"])]
        )
        + "</g>"
    )
    ticks = "".join(
        f'<line x1="{cx + 178 * math.cos(math.radians(a)):.1f}" y1="{cy + 178 * math.sin(math.radians(a)):.1f}" '
        f'x2="{cx + (170 if a % 30 else 162) * math.cos(math.radians(a)):.1f}" y2="{cy + (170 if a % 30 else 162) * math.sin(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 5)
    )
    core.append(f'<g class="core2" stroke="{C["ice"]}" stroke-opacity=".5">{ticks}</g>')
    core.append(
        f'<g class="core3"><circle cx="{cx}" cy="{cy}" r="132" stroke="url(#ring)" stroke-width="3" '
        f'stroke-dasharray="120 40 30 40 200 60 80 259" stroke-linecap="round" filter="url(#glow)"/></g>'
    )
    hexp = " ".join(
        f"{cx + 86 * math.cos(math.radians(60 * k + 30)):.1f},{cy + 86 * math.sin(math.radians(60 * k + 30)):.1f}"
        for k in range(6)
    )
    core.append(f'<polygon points="{hexp}" stroke="{C["sky"]}" stroke-opacity=".55" fill="{C["deep"]}" fill-opacity=".6"/>')
    core.append(f'<circle cx="{cx}" cy="{cy}" r="52" stroke="{C["cyan"]}" stroke-width="2"/>')
    core.append(
        f'<circle cx="{cx}" cy="{cy}" r="26" stroke="{C["blue"]}" stroke-width="1.6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="9" fill="{C["aqua"]}" filter="url(#glow)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="9" stroke="{C["aqua"]}" fill="none">'
        f'<animate attributeName="r" values="9;60" dur="2.6s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".9;0" dur="2.6s" repeatCount="indefinite"/></circle>'
    )
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        core.append(
            f'<line x1="{cx + dx * 60}" y1="{cy + dy * 60}" x2="{cx + dx * 84}" y2="{cy + dy * 84}" stroke="{C["cyan"]}" stroke-width="1.6"/>'
        )
    # orbiting satellites on hidden circular paths
    for r, dur, col, beg in [(132, 9, C["aqua"], 0), (205, 22, C["violet"], -7), (162, 15, C["mint"], -4)]:
        pid = f"orb{r}"
        core.append(
            f'<path id="{pid}" d="M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0" fill="none"/>'
            f'<circle r="4.5" fill="{col}" filter="url(#glow)"><animateMotion dur="{dur}s" begin="{beg}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>'
        )
    # capability labels around the core
    labels = [
        (-140, "AI ENGINEERING", C["aqua"]),
        (-40, "CLOUD & FINOPS", C["sky"]),
        (40, "DEVSECOPS", C["mint"]),
        (140, "AUTOMATION", C["lilac"]),
    ]
    for i, (ang, lab, col) in enumerate(labels):
        a = math.radians(ang)
        x1, y1 = cx + 205 * math.cos(a), cy + 205 * math.sin(a)
        x2, y2 = cx + 226 * math.cos(a), cy + 226 * math.sin(a)
        right = math.cos(a) > 0
        x3 = x2 + (26 if right else -26)
        core.append(
            f'<g class="lbl" style="animation-delay:-{i * 0.8:.1f}s">'
            f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} L{x3:.1f},{y2:.1f}" stroke="{col}" stroke-opacity=".8"/>'
            f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2.5" fill="{col}"/>'
            + text(x3 + (8 if right else -8), y2 + 4.5, lab, "m", 13, col, "start" if right else "end", 'letter-spacing="1.5"')
            + "</g>"
        )
    # data packets dropping from the core into the floor grid
    for k, (px, dly) in enumerate([(cx - 60, 0), (cx + 30, -1.1), (cx + 90, -2.0), (cx - 120, -0.6)]):
        core.append(
            f'<rect x="{px}" y="{cy + 230}" width="2" height="18" rx="1" fill="{C["aqua"]}" opacity="0">'
            f'<animate attributeName="y" values="{cy + 110};{H}" dur="2.6s" begin="{dly}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.9;0" dur="2.6s" begin="{dly}s" repeatCount="indefinite"/></rect>'
        )
    b.append("".join(core))

    # ---- copy (left)
    x0 = 72
    b.append(f'<rect x="{x0}" y="86" width="10" height="10" fill="{C["aqua"]}" transform="rotate(45 {x0 + 5} 91)"/>')
    b.append(text(x0 + 24, 96, "DEEPTECH R&D LAB  ·  EST. 2018", "m", 15, C["aqua"], extra='letter-spacing="3"'))
    b.append(text(x0 - 6, 236, "INZOX", "d", 156, "url(#wm)", extra='letter-spacing="-4"'))
    b.append(text(x0 - 6, 236, "INZOX", "d", 156, "url(#shine)", extra='letter-spacing="-4" opacity=".55"'))
    b.append(
        f'<text x="{x0}" y="296" class="d" font-size="38" fill="{C["text"]}" letter-spacing="-.5">Turning weeks into '
        f'<tspan fill="url(#minutes)">minutes.</tspan></text>'
    )
    b.append(text(x0, 334, "AI  ·  DevSecOps  ·  Cloud Engineering  ·  Automation", "m", 16, C["soft"], extra='letter-spacing=".5"'))

    # terminal strip
    tw = 640
    b.append(
        f'<rect x="{x0}" y="418" width="{tw}" height="56" rx="12" fill="{C["void"]}" fill-opacity=".85" stroke="{C["line"]}"/>'
        + "".join(
            f'<circle cx="{x0 + 18 + i * 14}" cy="436" r="3.5" fill="{c}" opacity=".8"/>'
            for i, c in enumerate([C["rose"], C["amber"], C["mint"]])
        )
    )
    b.append(text(x0 + 70, 452, "$", "mb", 16, C["mint"]))
    b.append(f'<g clip-path="url(#type)">{text(162, 452, term_cmd, "m", 16, C["text"])}</g>')
    b.append(
        f'<rect x="165" y="438" width="9" height="18" fill="{C["aqua"]}" class="blink">{caret}</rect>'
    )
    b.append(
        f'<g class="ok">{text(x0 + tw - 20, 452, "✓ We Deliver First", "mb", 15, C["mint"], "end")}</g>'
    )

    # bottom rail
    b.append(text(x0, 528, "EGYPT (HQ)  ·  USA  ·  MALAYSIA", "m", 12.5, C["muted"], extra='letter-spacing="2.5"'))
    b.append(
        f'<circle cx="{W - 250}" cy="524" r="4" fill="{C["mint"]}" class="pulse"/>'
        + text(W - 238, 528, "inzox.com  ·  inzox.ai", "m", 12.5, C["muted"], extra='letter-spacing="2"')
    )

    write(
        "hero.svg",
        svg(
            W, H, "".join(b),
            "INZOX — Turning weeks into minutes",
            "Animated INZOX banner: the INZOX wordmark, the tagline Turning weeks into minutes, "
            "and a rotating AI core labelled AI Engineering, Cloud & FinOps, DevSecOps and Automation.",
            css=css, defs=defs,
        ),
    )




# ----------------------------------------------------------- section header
def header(name, idx, eyebrow, title):
    """Transparent section header. Mid-tone blues read on light and dark."""
    H = 112
    defs = (
        f'<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="120" y1="0" x2="720" y2="0">'
        f'<stop offset="0" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["violet"]}"/></linearGradient>'
        f'<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{C["blue"]}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="{C["violet"]}" stop-opacity="0"/></linearGradient>'
    )
    tw = measure(title, "IZ Display", 36, -0.5)
    lx = 128 + tw + 28
    b = [
        text(8, 86, idx, "d", 78, "none", extra=f'stroke="{C["blue"]}" stroke-width="1.4" stroke-opacity=".75" letter-spacing="-2"'),
        f'<rect x="128" y="34" width="8" height="8" fill="{C["blue"]}" transform="rotate(45 132 38)"/>',
        text(146, 43, eyebrow, "m", 14, C["blue"], extra='letter-spacing="4"'),
        text(128, 86, title, "d", 36, "url(#tg)", extra='letter-spacing="-.5"'),
        f'<path id="rail" d="M{lx:.0f},74 H{W - 8}" stroke="url(#ln)" stroke-width="1.5"/>',
    ]
    for k in range(6):
        x = lx + 30 + k * ((W - lx - 60) / 6)
        b.append(f'<line x1="{x:.0f}" x2="{x:.0f}" y1="70" y2="78" stroke="{C["blue"]}" stroke-opacity="{0.6 - k * 0.09:.2f}"/>')
    b.append(
        f'<circle r="3.5" fill="{C["blue"]}"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.7;1" calcMode="linear"><mpath href="#rail"/></animateMotion>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.6;.7;1" dur="5s" repeatCount="indefinite"/></circle>'
    )
    write(name, svg(W, H, "".join(b), f"{idx} — {title}", f"Section header: {eyebrow.title()} — {title}", defs=defs, panel=False))


# ----------------------------------------------------------------- manifesto
def manifesto():
    H = 440
    css = """
.squash{transform-origin:212px 0;animation:squash 9s cubic-bezier(.7,0,.3,1) infinite}
@keyframes squash{0%,18%{transform:scaleX(1)}42%,82%{transform:scaleX(.075)}96%,100%{transform:scaleX(1)}}
.bar{animation:barc 9s cubic-bezier(.7,0,.3,1) infinite}
@keyframes barc{0%,18%{fill:#2A3A66}42%,82%{fill:#4FD2FF}96%,100%{fill:#2A3A66}}
.weeks{animation:wk 9s ease infinite}
@keyframes wk{0%,22%{opacity:1}34%,86%{opacity:0}96%,100%{opacity:1}}
.mins{animation:mn 9s ease infinite}
@keyframes mn{0%,36%{opacity:0}46%,82%{opacity:1}92%,100%{opacity:0}}
.strike{stroke-dasharray:200;animation:strike 9s ease infinite}
@keyframes strike{0%,30%{stroke-dashoffset:200}44%,86%{stroke-dashoffset:0}96%,100%{stroke-dashoffset:200}}
"""
    defs = (
        f'<linearGradient id="num" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/>'
        f'<stop offset="1" stop-color="{C["sky"]}"/></linearGradient>'
        f'<linearGradient id="mg" gradientUnits="userSpaceOnUse" x1="950" x2="1180" y1="0" y2="0"><stop offset="0" stop-color="{C["aqua"]}"/>'
        f'<stop offset="1" stop-color="{C["blue"]}"/></linearGradient>'
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )
    b = []
    # left: compressing gantt
    gx, gy, cw = 212, 120, 58
    b.append(f'<rect x="32" y="32" width="676" height="{H - 64}" rx="16" fill="{C["void"]}" fill-opacity=".55" stroke="{C["line"]}"/>')
    ls = 'letter-spacing="2.5"'
    b.append('<g class="weeks">' + text(56, 74, "TRADITIONAL DELIVERY  ·  WEEKS", "m", 13, C["muted"], extra=ls) + "</g>")
    b.append('<g class="mins">' + text(56, 74, "WITH INZOX  ·  MINUTES", "mb", 13, C["aqua"], extra=ls) + "</g>")
    grid = []
    for k in range(9):
        x = gx + k * cw
        grid.append(f'<line x1="{x}" x2="{x}" y1="{gy - 14}" y2="{gy + 6 * 44}" stroke="{C["grid"]}"/>')
        if k < 8:
            grid.append(text(x + cw / 2, gy - 22, f"W{k + 1}", "m", 11, C["dim"], "middle"))
    b.append(f'<g class="weeks">{"".join(grid)}</g>')
    rows = [("DISCOVERY", 0, 1.6), ("PROVISIONING", 1.0, 3.0), ("CI/CD SETUP", 2.4, 4.6),
            ("SECURITY REVIEW", 3.8, 6.0), ("REPORTING", 5.0, 7.1), ("RELEASE", 6.4, 8.0)]
    bars = []
    for i, (lab, s0, s1) in enumerate(rows):
        y = gy + i * 44
        b.append(text(56, y + 20, lab, "m", 12, C["soft"], extra='letter-spacing="1"'))
        bars.append(f'<rect class="bar" x="{gx + s0 * cw + 3:.0f}" y="{y + 6}" width="{(s1 - s0) * cw - 6:.0f}" height="20" rx="5"/>')
    b.append(f'<g class="squash">{"".join(bars)}</g>')
    b.append(
        f'<g class="mins"><line x1="{gx + 50}" x2="{gx + 50}" y1="{gy - 4}" y2="{gy + 6 * 44 - 8}" stroke="{C["aqua"]}" stroke-dasharray="3 4"/>'
        f'<path d="M{gx + 60},{gy + 128} h70" stroke="{C["aqua"]}" stroke-width="1.5"/>'
        f'<path d="M{gx + 124},{gy + 122} l7,6 -7,6" stroke="{C["aqua"]}" stroke-width="1.5"/>'
        + text(gx + 144, gy + 126, "Automated, AI-assisted,", "b", 18, C["text"])
        + text(gx + 144, gy + 150, "secure-by-default delivery", "b", 18, C["text"])
        + text(gx + 144, gy + 182, "same scope · a fraction of the time", "m", 12, C["aqua"], extra='letter-spacing="1"')
        + "</g>"
    )

    # right: mission + stats
    x0 = 760
    b.append(text(x0, 84, "OUR MISSION", "m", 13, C["aqua"], extra='letter-spacing="4"'))
    b.append(text(x0, 146, "Weeks", "d", 58, C["dim"], extra='letter-spacing="-1"'))
    ww = measure("Weeks", "IZ Display", 58, -1)
    b.append(f'<path class="strike" d="M{x0 - 4},128 h{ww + 8:.0f}" stroke="{C["rose"]}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<path d="M{x0 + ww + 22:.0f},126 h30 m-10,-10 l10,10 -10,10" stroke="{C["soft"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(text(x0 + ww + 70, 146, "Minutes.", "d", 58, "url(#mg)", extra='letter-spacing="-1"'))
    for k, line in enumerate(["We empower organizations through intelligent products,",
                              "automation and engineering excellence that turn",
                              "weeks of work into minutes of execution."]):
        b.append(text(x0, 190 + k * 25, line, "b", 17, C["soft"]))
    stats = [("7+", "YEARS OF DEEPTECH R&D"), ("300+", "PROJECTS DELIVERED"),
             ("100+", "TEAM MEMBERS"), ("3", "GLOBAL OFFICES")]
    for k, (n, lab) in enumerate(stats):
        sx = x0 + (k % 2) * 245
        sy = 318 + (k // 2) * 72
        b.append(f'<rect x="{sx - 16}" y="{sy - 40}" width="3" height="52" rx="1.5" fill="{[C["aqua"], C["blue"], C["violet"], C["mint"]][k]}"/>')
        b.append(text(sx, sy, n, "d", 40, "url(#num)", extra='letter-spacing="-1"'))
        b.append(text(sx, sy + 20, lab, "m", 11.5, C["muted"], extra='letter-spacing="1.8"'))
    write("manifesto.svg", svg(W, H, "".join(b), "Weeks to minutes",
          "Animated Gantt chart of six delivery phases spanning eight weeks compressing into minutes, beside the INZOX mission "
          "and stats: 7+ years of DeepTech R&D, 300+ projects delivered, 100+ team members, 3 global offices.", css=css, defs=defs))


# -------------------------------------------------------------------- icons
ICONS = {
    "cloud": '<path d="M14 36h21a8.5 8.5 0 0 0 1.4-16.9A12 12 0 0 0 13.6 17 9.6 9.6 0 0 0 14 36z"/><path d="M17 27l5 4 5-6 6 5"/>',
    "loop": '<path d="M6 24c0-5 3.6-8.5 8.5-8.5C22 15.5 26 32.5 33.5 32.5 38.4 32.5 42 29 42 24s-3.6-8.5-8.5-8.5C26 15.5 22 32.5 14.5 32.5 9.6 32.5 6 29 6 24z"/>',
    "shield": '<path d="M24 5l15 6v11c0 10-6.4 17.4-15 21C15.4 39.4 9 32 9 22V11z"/><path d="M17 24l5 5 9-10"/>',
    "neural": '<path d="M10 14L24 10 38 24 24 38 10 34M10 14L24 24 10 34M24 10v28M24 24h14"/><circle cx="10" cy="14" r="3.5"/><circle cx="10" cy="34" r="3.5"/><circle cx="24" cy="10" r="3.5"/><circle cx="24" cy="24" r="3.5"/><circle cx="24" cy="38" r="3.5"/><circle cx="38" cy="24" r="3.5"/>',
    "code": '<path d="M16 14l-10 10 10 10M32 14l10 10-10 10M28 9l-8 30"/>',
    "academy": '<path d="M3 18l21-9 21 9-21 9z"/><path d="M11 22v9c0 3.5 6 6.5 13 6.5s13-3 13-6.5v-9M45 18v11"/>',
}


def icon(name, x, y, color, scale=1.0, sw=2.2):
    return (
        f'<g transform="translate({x},{y}) scale({scale})" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round" fill="none">{ICONS[name]}</g>'
    )


# -------------------------------------------------------------- capabilities
def capabilities():
    H = 720
    cards = [
        ("cloud", "Cloud & FinOps", ["Cut cloud spend and tune performance", "with FinOps best practices."], ["AWS", "AZURE", "GCP"], C["sky"]),
        ("loop", "DevOps & Automation", ["Delivery pipelines automated end to end", "with CI/CD, IaC and Kubernetes."], ["CI/CD", "IAC", "K8S"], C["blue"]),
        ("shield", "DevSecOps & Security", ["Secure-by-design architecture,", "compliance and threat protection."], ["ZERO TRUST", "POLICY", "AUDIT"], C["mint"]),
        ("neural", "AI & Innovation Lab", ["Machine learning, NLP, computer vision", "and intelligent automation."], ["LLM", "ML", "VISION"], C["aqua"]),
        ("code", "Software Engineering", ["Custom software on modern stacks,", "built to solve complex problems."], ["WEB", "API", "DATA"], C["violet"]),
        ("academy", "Tech Academy", ["Hands-on training designed by engineers", "working on real-world projects."], ["TRACKS", "LABS", "MENTORSHIP"], C["amber"]),
    ]
    css = "".join(
        f".c{i}{{animation:cg 6s ease-in-out infinite;animation-delay:-{(6 - i) * 1.0:.1f}s}}" for i in range(6)
    ) + "@keyframes cg{0%,100%{stroke-opacity:.18}12%{stroke-opacity:1}30%{stroke-opacity:.18}}"
    css += ".chiprot{transform-origin:640px 360px;animation:spin 18s linear infinite}"
    defs = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<linearGradient id="chipg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["panel2"]}"/><stop offset="1" stop-color="{C["void"]}"/></linearGradient>'
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{C["grid"]}"/></pattern>'
    )
    b = [f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']
    cw, ch = 372, 196
    positions = []
    for i in range(6):
        left = i < 3
        x = 36 if left else W - 36 - cw
        y = 44 + (i % 3) * (ch + 22)
        positions.append((x, y))
    # traces
    traces = []
    for i, (x, y) in enumerate(positions):
        left = i < 3
        cy_card = y + ch / 2
        sy = 330 + (i % 3) * 30
        if left:
            sx, ex, mx = 520, x + cw, 470 - (i % 3) * 14
        else:
            sx, ex, mx = 760, x, 810 + (i % 3) * 14
        d = f"M{sx},{sy} H{mx} V{cy_card:.0f} H{ex}"
        col = cards[i][4]
        traces.append(f'<path id="tr{i}" d="{d}" stroke="{col}" stroke-opacity=".35" stroke-width="1.5"/>')
        traces.append(f'<circle cx="{sx}" cy="{sy}" r="3" fill="{col}"/><circle cx="{ex}" cy="{cy_card:.0f}" r="3.5" fill="{col}"/>')
        traces.append(
            f'<circle r="3.5" fill="{col}" filter="url(#glow)"><animateMotion dur="6s" begin="-{(6 - i) * 1.0 + 5.3:.1f}s" repeatCount="indefinite" '
            f'keyPoints="0;1;1" keyTimes="0;.15;1" calcMode="linear"><mpath href="#tr{i}"/></animateMotion></circle>'
        )
    b.append("".join(traces))
    # core chip
    b.append(f'<rect x="520" y="285" width="240" height="150" rx="18" fill="url(#chipg)" stroke="{C["sky"]}" stroke-opacity=".6"/>')
    for k in range(9):
        px = 548 + k * 23
        b.append(f'<rect x="{px}" y="276" width="8" height="9" rx="2" fill="{C["line"]}"/><rect x="{px}" y="435" width="8" height="9" rx="2" fill="{C["line"]}"/>')
    b.append(f'<g class="chiprot"><circle cx="640" cy="360" r="104" stroke="{C["blue"]}" stroke-opacity=".35" stroke-dasharray="4 10"/></g>')
    b.append(text(640, 344, "INZOX", "d", 40, C["text"], "middle", 'letter-spacing="-1"'))
    b.append(text(640, 372, "DELIVERY ENGINE", "m", 12, C["aqua"], "middle", 'letter-spacing="3"'))
    b.append(text(640, 400, "Discover → Optimize", "m", 12, C["muted"], "middle"))
    # cards
    for i, ((ic, title, desc, tags, col), (x, y)) in enumerate(zip(cards, positions)):
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{C["panel"]}" fill-opacity=".92"/>')
        b.append(f'<rect class="c{i}" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" stroke="{col}" stroke-width="1.5"/>')
        b.append(f'<rect x="{x + 22}" y="{y + 22}" width="52" height="52" rx="12" fill="{col}" fill-opacity=".1"/>')
        b.append(icon(ic, x + 24, y + 24, col, 1.0))
        b.append(text(x + cw - 22, y + 40, f"0{i + 1}", "m", 13, C["dim"], "end", 'letter-spacing="2"'))
        b.append(text(x + 90, y + 56, title, "d", 22, C["text"], extra='letter-spacing="-.3"'))
        for k, line in enumerate(desc):
            b.append(text(x + 24, y + 106 + k * 22, line, "b", 15, C["soft"]))
        tx = x + 24
        for t in tags:
            c_svg, w_ = chip(tx, y + ch - 46, t, col, size=11, pad=10, h=24)
            b.append(c_svg)
            tx += w_ + 8
    write("capabilities.svg", svg(W, H, "".join(b), "What INZOX does",
          "Circuit-board diagram: the INZOX delivery engine connected to six capabilities — Cloud & FinOps, DevOps & Automation, "
          "DevSecOps & Security, AI & Innovation Lab, Software Engineering and Tech Academy.", css=css, defs=defs))


# ------------------------------------------------------------ devsecops loop
def devsecops():
    H = 600
    cx, cy, A = 640, 286, 460

    def lem(t):
        d = 1 + math.sin(t) ** 2
        return cx + A * math.cos(t) / d, cy + A * math.sin(t) * math.cos(t) / d

    n = 240
    pts = [lem(2 * math.pi * k / n) for k in range(n)]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    css = """
.comet{stroke-dasharray:70 930;animation:comet 8s linear infinite}
.comet2{stroke-dasharray:30 970;animation:comet 8s linear infinite;animation-delay:-4s}
@keyframes comet{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
.gate{animation:gate 4s ease-in-out infinite}
@keyframes gate{0%,100%{opacity:.55}50%{opacity:1}}
.shieldring{transform-origin:640px 286px;animation:spin 20s linear infinite}
"""
    defs = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<linearGradient id="loopg" gradientUnits="userSpaceOnUse" x1="{cx - A}" x2="{cx + A}" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{C["aqua"]}"/><stop offset=".5" stop-color="{C["mint"]}"/><stop offset="1" stop-color="{C["violet"]}"/></linearGradient>'
        f'<radialGradient id="sh"><stop offset="0" stop-color="{C["mint"]}" stop-opacity=".35"/><stop offset="1" stop-color="{C["mint"]}" stop-opacity="0"/></radialGradient>'
    )
    b = [stars(W, H, 40, seed=5)]
    b.append(f'<path id="lem" d="{path}" stroke="{C["line"]}" stroke-width="22" stroke-linejoin="round"/>')
    b.append(f'<path d="{path}" stroke="url(#loopg)" stroke-opacity=".5" stroke-width="2"/>')
    b.append(f'<path d="{path}" pathLength="1000" class="comet" stroke="url(#loopg)" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>')
    b.append(f'<path d="{path}" pathLength="1000" class="comet2" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/>')
    for k in range(5):
        b.append(
            f'<rect x="-5" y="-5" width="10" height="10" rx="2" fill="{C["aqua"] if k % 2 else C["lilac"]}">'
            f'<animateMotion dur="16s" begin="-{k * 3.2:.1f}s" repeatCount="indefinite" rotate="auto"><mpath href="#lem"/></animateMotion></rect>'
        )
    # lobe captions
    b.append(text(cx - A * 0.62, cy - 6, "DESIGN", "d", 30, C["text"], "middle", 'letter-spacing="2" opacity=".9"'))
    b.append(text(cx - A * 0.62, cy + 20, "plan · model · threat-model", "m", 12, C["muted"], "middle"))
    b.append(text(cx + A * 0.62, cy - 6, "DELIVER", "d", 30, C["text"], "middle", 'letter-spacing="2" opacity=".9"'))
    b.append(text(cx + A * 0.62, cy + 20, "ship · observe · improve", "m", 12, C["muted"], "middle"))

    # stage nodes (INZOX solutions framework)
    stages = [
        ("01", "DISCOVER", 2.55), ("02", "ANALYZE", math.pi), ("03", "ARCHITECT", 3.73),
        ("04", "DEVELOP", 5.69), ("05", "DEPLOY", 0.0), ("06", "OPTIMIZE", 0.59),
    ]
    for num, lab, t in stages:
        x, y = lem(t)
        w = measure(lab, "IZ MonoBold", 13, 1.5) + 58
        b.append(f'<rect x="{x - w / 2:.1f}" y="{y - 17:.1f}" width="{w:.1f}" height="34" rx="17" fill="{C["panel"]}" stroke="{C["sky"]}" stroke-opacity=".7"/>')
        b.append(text(x - w / 2 + 14, y + 4.5, num, "m", 12, C["aqua"]))
        b.append(text(x - w / 2 + 40, y + 4.5, lab, "mb", 13, C["text"], extra='letter-spacing="1.5"'))

    # security gates sitting on the loop
    gates = [
        ("THREAT MODEL", 3.37, -1), ("SECRETS SCAN", 4.22, 1), ("SAST · SCA", 5.2, 1),
        ("IaC POLICY", 5.98, -1), ("SBOM · SIGN", 0.33, 1), ("RUNTIME WATCH", 0.95, -1),
        ("LEAST PRIVILEGE", 2.2, -1), ("AUDIT TRAIL", 2.86, 1),
    ]
    for i, (lab, t, side) in enumerate(gates):
        x, y = lem(t)
        oy = 34 * side if abs(y - cy) < 60 else (36 if y > cy else -36)
        ty = y + oy
        b.append(
            f'<g class="gate" style="animation-delay:-{i * 0.5:.1f}s">'
            f'<rect x="{x - 6:.1f}" y="{y - 6:.1f}" width="12" height="12" fill="{C["void"]}" stroke="{C["mint"]}" stroke-width="2" transform="rotate(45 {x:.1f} {y:.1f})"/>'
            f'<line x1="{x:.1f}" y1="{y + (8 if oy > 0 else -8):.1f}" x2="{x:.1f}" y2="{ty - (12 if oy > 0 else -4):.1f}" stroke="{C["mint"]}" stroke-opacity=".5" stroke-dasharray="2 3"/>'
            + text(x, ty + (4 if oy > 0 else 0), lab, "m", 11, C["mint"], "middle", 'letter-spacing="1.2"')
            + "</g>"
        )

    # central shield where both loops cross
    b.append(f'<circle cx="{cx}" cy="{cy}" r="74" fill="url(#sh)"/>')
    b.append(f'<g class="shieldring"><circle cx="{cx}" cy="{cy}" r="56" stroke="{C["mint"]}" stroke-opacity=".6" stroke-dasharray="3 6"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="42" fill="{C["void"]}" stroke="{C["mint"]}" stroke-width="2"/>')
    b.append(icon("shield", cx - 24, cy - 26, C["mint"], 1.0, 2.6))
    b.append(f'<rect x="{cx - 70}" y="{cy + 66}" width="140" height="42" rx="8" fill="{C["deep"]}" fill-opacity=".9"/>')
    b.append(text(cx, cy + 82, "SECURITY GATES", "mb", 12, C["mint"], "middle", 'letter-spacing="3"'))
    b.append(text(cx, cy + 100, "on every pass", "m", 11, C["muted"], "middle"))

    # toolchain rail
    tools = ["GitHub Actions", "Terraform", "Ansible", "Kubernetes", "Docker", "AWS", "Azure", "Google Cloud"]
    widths = [measure(t, "IZ Mono", 12, 0.6) + 24 + 14 for t in tools]
    total = sum(widths) + 10 * (len(tools) - 1) + measure("TOOLCHAIN", "IZ MonoBold", 12, 3) + 24
    x = (W - total) / 2
    b.append(text(x, H - 39, "TOOLCHAIN", "mb", 12, C["muted"], extra='letter-spacing="3"'))
    x += measure("TOOLCHAIN", "IZ MonoBold", 12, 3) + 24
    for t in tools:
        c_svg, w_ = chip(x, H - 56, t, C["sky"], size=12)
        b.append(c_svg)
        x += w_ + 10
    write("devsecops.svg", svg(W, H, "".join(b), "INZOX DevSecOps delivery loop",
          "Animated infinity loop of the INZOX framework — Discover, Analyze, Architect, Develop, Deploy, Optimize — "
          "with security gates (threat model, secrets scan, SAST and SCA, IaC policy, SBOM and signing, runtime watch, "
          "least privilege, audit trail) and a shield at the centre where both loops cross.", css=css, defs=defs))


# -------------------------------------------------------------- ZOX showcase
def zox_mark(x, y, s=1.0):
    """The ZOX reticle, after the favicon at inzox.ai."""
    return (
        f'<g transform="translate({x},{y}) scale({s})">'
        f'<circle cx="16" cy="16" r="11" stroke="{C["cyan"]}" stroke-width="2"/>'
        f'<circle cx="16" cy="16" r="5.6" stroke="#1789C4" stroke-width="1.4"/>'
        f'<circle cx="16" cy="16" r="2" fill="{C["aqua"]}"/>'
        f'<path d="M16 1v3.4M16 27.6V31M1 16h3.4M27.6 16H31" stroke="#1789C4" stroke-width="1.4"/></g>'
    )


def zox():
    H = 680
    css = """
.rise{animation:rise 4.5s linear infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}10%{opacity:1}85%{opacity:1}100%{transform:translateY(-330px);opacity:0}}
.lay{animation:lay 6s ease-in-out infinite}
@keyframes lay{0%,100%{fill-opacity:.10}20%{fill-opacity:.42}40%{fill-opacity:.10}}
.blocked{animation:blk 3s ease-in-out infinite}
@keyframes blk{0%{transform:translateX(0);opacity:0}15%{opacity:1}55%{transform:translateX(118px);opacity:1}70%,100%{transform:translateX(118px);opacity:0}}
.x{animation:xx 3s ease-in-out infinite}
@keyframes xx{0%,50%{opacity:.25}58%,80%{opacity:1}100%{opacity:.25}}
"""
    defs = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<linearGradient id="zg" gradientUnits="userSpaceOnUse" x1="56" x2="520" y1="0" y2="0"><stop offset="0" stop-color="{C["aqua"]}"/>'
        f'<stop offset="1" stop-color="#1789C4"/></linearGradient>'
        f'<radialGradient id="brain" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></radialGradient>'
    )
    b = [f'<rect width="{W}" height="{H}" fill="#04070D" opacity=".55"/>']
    # ---- left copy
    x0 = 56
    b.append(zox_mark(x0, 54, 1.9))
    b.append(text(x0 + 78, 102, "ZOX", "d", 58, C["text"], extra='letter-spacing="2"'))
    b.append(text(x0 + 212, 84, "THE ENTERPRISE", "m", 12, C["cyan"], extra='letter-spacing="3"'))
    b.append(text(x0 + 212, 102, "AI BRAIN", "m", 12, C["cyan"], extra='letter-spacing="3"'))
    b.append(text(x0, 168, "Enterprise intelligence", "d", 34, C["text"], extra='letter-spacing="-.5"'))
    b.append(text(x0, 208, "that thinks inside", "d", 34, C["text"], extra='letter-spacing="-.5"'))
    b.append(text(x0, 248, "your own walls.", "d", 34, "url(#zg)", extra='letter-spacing="-.5"'))
    for k, line in enumerate(["A private AI platform that ingests your data,",
                              "reasons over it and returns decisions —",
                              "running entirely on hardware you control."]):
        b.append(text(x0, 288 + k * 23, line, "b", 16, C["soft"]))
    x = x0
    for t in ["SOVEREIGN", "AIR-GAPPED", "ZERO DATA EGRESS"]:
        c_svg, w_ = chip(x, 370, t, C["cyan"], size=11.5, h=28, fill="#04070D")
        b.append(c_svg)
        x += w_ + 8
    engines = [
        ("Business Intelligence Brain", "KPI synthesis across every source"),
        ("Strategic Reasoning Engine", "recommendations with an evidence trail"),
        ("Scenario Simulation", "test the decision before you live it"),
        ("Sovereign Architecture", "no external inference, no telemetry"),
    ]
    b.append(text(x0, 436, "FOUR ENGINES · ONE BRAIN", "m", 12, C["muted"], extra='letter-spacing="3"'))
    for k, (name, det) in enumerate(engines):
        y = 470 + k * 46
        b.append(f'<rect x="{x0}" y="{y - 16}" width="26" height="26" rx="7" fill="{C["cyan"]}" fill-opacity=".12" stroke="{C["cyan"]}" stroke-opacity=".5"/>')
        b.append(text(x0 + 13, y + 1.5, f"{k + 1}", "mb", 12, C["aqua"], "middle"))
        b.append(text(x0 + 40, y - 1, name, "d", 17, C["text"]))
        b.append(text(x0 + 40, y + 18, det, "m", 11.5, C["muted"]))

    # ---- right: perimeter + isometric layer stack
    px, py, pw, ph = 590, 40, 650, 600
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22" fill="url(#brain)"/>')
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="22" stroke="{C["cyan"]}" stroke-width="1.6" class="march"/>')
    pl = measure("YOUR PERIMETER · YOUR SILICON", "IZ MonoBold", 11.5, 1.6)
    b.append(f'<rect x="{px + 22}" y="{py - 10}" width="{pl + 24:.0f}" height="20" fill="#05091A"/>')
    b.append(text(px + 34, py + 5, "YOUR PERIMETER · YOUR SILICON", "mb", 11.5, C["cyan"], extra='letter-spacing="1.6"'))

    sx, w2, h2 = 800, 170, 52
    layers = [
        ("DECISION", "Recommendations · Actions", C["mint"]),
        ("REASONING", "Simulation · Risk evaluation", C["violet"]),
        ("INTELLIGENCE", "KPI synthesis · Correlation", C["blue"]),
        ("DATA", "Ingestion · Normalisation", C["cyan"]),
    ]
    ys = [196, 296, 396, 496]
    # vertical spine behind layers
    b.append(f'<line x1="{sx}" y1="{ys[0]}" x2="{sx}" y2="{ys[-1] + 70}" stroke="{C["cyan"]}" stroke-opacity=".35" stroke-dasharray="3 5"/>')
    for i in reversed(range(4)):
        name, det, col = layers[i]
        y = ys[i]
        pts = f"{sx},{y - h2} {sx + w2},{y} {sx},{y + h2} {sx - w2},{y}"
        b.append(f'<polygon points="{sx},{y - h2 + 12} {sx + w2},{y + 12} {sx},{y + h2 + 12} {sx - w2},{y + 12}" fill="{col}" fill-opacity=".06"/>')
        b.append(
            f'<polygon class="lay" style="animation-delay:-{(3 - i) * 1.5 - 4.5:.1f}s" points="{pts}" fill="{col}" stroke="{col}" stroke-width="1.5"/>'
        )
        # grid on top face
        for k in (1, 2, 3):
            f = k / 4
            b.append(
                f'<line x1="{sx - w2 + w2 * f:.0f}" y1="{y - h2 * f:.0f}" x2="{sx + w2 * f:.0f}" y2="{y + h2 - h2 * f:.0f}" stroke="{col}" stroke-opacity=".22"/>'
                f'<line x1="{sx - w2 * f:.0f}" y1="{y - h2 + h2 * f:.0f}" x2="{sx + w2 - w2 * f:.0f}" y2="{y + h2 * f:.0f}" stroke="{col}" stroke-opacity=".22"/>'
            )
        # label with leader
        lx = sx + w2 + 30
        b.append(f'<path d="M{sx + w2},{y} H{lx - 8}" stroke="{col}" stroke-opacity=".6"/><circle cx="{sx + w2}" cy="{y}" r="3" fill="{col}"/>')
        b.append(text(lx, y - 2, name, "mb", 14, col, extra='letter-spacing="2"'))
        b.append(text(lx, y + 17, det, "m", 11.5, C["soft"]))
    # data particles rising through the stack
    for k in range(9):
        ox = sx - 60 + (k * 37) % 120
        b.append(
            f'<rect x="{ox}" y="{ys[-1] + 40}" width="5" height="5" rx="1" fill="{[C["aqua"], C["mint"], C["lilac"]][k % 3]}" class="rise" '
            f'style="animation-delay:-{k * 0.5:.1f}s" filter="url(#glow)"/>'
        )
    # sources feeding the data layer
    srcs = ["ERP", "FINANCE", "OPERATIONS", "ARCHIVES"]
    widths = [measure(s_, "IZ Mono", 11, 0.6) + 24 + 14 for s_ in srcs]
    tx = sx - (sum(widths) + 8 * 3) / 2
    for s_ in srcs:
        c_svg, w_ = chip(tx, 590, s_, C["cyan"], size=11, h=24, fill="#04070D")
        b.append(c_svg)
        tx += w_ + 8
    # blocked egress
    ey = 120
    b.append(f'<path d="M{sx + 40},{ey} H{px + pw - 34}" stroke="{C["rose"]}" stroke-opacity=".35" stroke-dasharray="4 5"/>')
    b.append(f'<g class="blocked"><circle cx="{sx + 70}" cy="{ey}" r="5" fill="{C["rose"]}" filter="url(#glow)"/></g>')
    b.append(
        f'<g class="x"><circle cx="{px + pw - 20}" cy="{ey}" r="13" fill="#04070D" stroke="{C["rose"]}" stroke-width="2"/>'
        f'<path d="M{px + pw - 25},{ey - 5} l10,10 m0,-10 l-10,10" stroke="{C["rose"]}" stroke-width="2.4" stroke-linecap="round"/></g>'
    )
    b.append(text(sx + 40, ey - 14, "NO OUTBOUND CALL · ZERO DATA EGRESS", "m", 11, C["rose"], extra='letter-spacing="1.3"'))
    write("zox.svg", svg(W, H, "".join(b), "ZOX — the Enterprise AI Brain",
          "ZOX by INZOX: sovereign, air-gapped enterprise AI. A four-layer stack — Data, Intelligence, Reasoning, Decision — "
          "runs inside the customer perimeter with zero data egress. Four engines: Business Intelligence Brain, Strategic "
          "Reasoning Engine, Scenario Simulation and Sovereign Architecture.", css=css, defs=defs))


# ------------------------------------------------------------ product cards
def product_card(name, slug, title, lines, domain, tags, col, glyph, css):
    w, h = 640, 300
    b = [f'<circle cx="128" cy="150" r="104" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".25"/>',
         f'<circle cx="128" cy="150" r="122" stroke="{col}" stroke-opacity=".18" stroke-dasharray="2 6" class="spin" style="transform-origin:128px 150px"/>',
         glyph]
    x0 = 268
    b.append(text(x0, 64, "INZOX PRODUCT LAB", "m", 11, col, extra='letter-spacing="3"'))
    b.append(text(x0, 112, title, "d", 40, C["text"], extra='letter-spacing="-1"'))
    for k, ln in enumerate(lines):
        b.append(text(x0, 150 + k * 25, ln, "b", 17.5, C["soft"]))
    x = x0
    for t in tags:
        c_svg, w_ = chip(x, 206, t, col, size=11, pad=10, h=24)
        b.append(c_svg)
        x += w_ + 8
    dw = measure(domain + "  ↗", "IZ MonoBold", 14, 0.5) + 28
    b.append(f'<rect x="{x0}" y="244" width="{dw:.0f}" height="32" rx="9" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6"/>')
    b.append(text(x0 + 14, 265, domain + "  ↗", "mb", 14, col, extra='letter-spacing=".5"'))
    write(f"product-{slug}.svg", svg(w, h, "".join(b), f"{name} by INZOX", f"{name}: {' '.join(lines)} ({domain})", css=css))


def products():
    V, A, AM, M = C["lilac"], C["aqua"], C["amber"], C["mint"]
    # OX.Report: a page under an X-ray scanner with live audit scores
    ox = [f'<rect x="72" y="76" width="96" height="128" rx="10" fill="{C["panel2"]}" stroke="{V}" stroke-width="2"/>']
    for k in range(6):
        ox.append(f'<rect x="86" y="{96 + k * 16}" width="{[60, 44, 66, 38, 58, 50][k]}" height="5" rx="2.5" fill="{V}" fill-opacity=".45"/>')
    ox.append(f'<rect class="scan" x="64" y="76" width="112" height="3" rx="1.5" fill="{V}"/>')
    for k, (lab, wv) in enumerate([("SEC", 34), ("PERF", 28), ("SEO", 38), ("UX", 31)]):
        y = 96 + k * 30
        ox.append(text(180, y + 4, lab, "m", 9, C["muted"]))
        ox.append(f'<rect x="180" y="{y + 9}" width="40" height="5" rx="2.5" fill="{C["line"]}"/>')
        ox.append(f'<rect class="score" style="animation-delay:-{k * .4:.1f}s" x="180" y="{y + 9}" width="{wv}" height="5" rx="2.5" fill="{V}"/>')
    ox_css = (".scan{animation:scan 2.8s ease-in-out infinite}@keyframes scan{0%,100%{transform:translateY(0)}50%{transform:translateY(124px)}}"
              ".score{transform-box:fill-box;animation:score 2.8s ease-in-out infinite}@keyframes score{0%{transform:scaleX(.1)}60%,100%{transform:scaleX(1)}}")
    product_card("OX.Report", "ox", "OX.Report",
                 ["AI technical audit — security, performance,", "SEO and UX, with exact how-to-fix steps."],
                 "ox.report", ["SECURITY", "PERFORMANCE", "SEO", "UX"], V, "".join(ox), ox_css)

    # Docker.Boats: a container ship riding a wave
    hull = f'<path d="M50 160 H206 L190 190 H68 Z" fill="{C["panel2"]}" stroke="{A}" stroke-width="2.2" stroke-linejoin="round"/>'
    boxes = "".join(
        f'<rect x="{68 + c * 28}" y="{132 - r * 22}" width="24" height="18" rx="2" fill="{[C["blue"], A, C["violet"], C["mint"]][(c + r) % 4]}" fill-opacity=".85"/>'
        for r in range(3) for c in range(5) if not (r == 2 and c in (0, 4))
    )
    mast = f'<path d="M184 160 V104 h10" stroke="{A}" stroke-width="2"/><circle cx="196" cy="104" r="3" fill="{C["mint"]}" class="pulse"/>'
    wave = "M-60 200 " + " ".join(f"q 20 -12 40 0 t 40 0" for _ in range(5))
    db = (f'<g class="bob">{hull}{boxes}{mast}</g>'
          f'<g class="wave"><path d="{wave}" stroke="{A}" stroke-width="2.2" stroke-opacity=".8"/>'
          f'<path d="{wave}" transform="translate(-20 14)" stroke="{C["blue"]}" stroke-width="2" stroke-opacity=".5"/></g>')
    db_css = (".bob{transform-origin:128px 180px;animation:bob 3.2s ease-in-out infinite}@keyframes bob{0%,100%{transform:rotate(-2.5deg) translateY(0)}50%{transform:rotate(2.5deg) translateY(-4px)}}"
              ".wave{animation:wave 2.4s linear infinite}@keyframes wave{to{transform:translateX(80px)}}")
    product_card("Docker.Boats", "docker-boats", "Docker.Boats",
                 ["A command center for containers that", "think, heal and scale — guided by AI."],
                 "docker.boats", ["AI OPS", "SELF-HEALING", "FLEET"], A, f'<g clip-path="url(#gc)"><clipPath id="gc"><circle cx="128" cy="150" r="104"/></clipPath>{db}</g>', db_css)

    # HOURz: an hourglass where time is the currency
    hg = (f'<path d="M88 70 H168 M88 230 H168" stroke="{AM}" stroke-width="3" stroke-linecap="round"/>'
          f'<path d="M96 72 C96 120 124 136 124 150 C124 164 96 180 96 228 H160 C160 180 132 164 132 150 C132 136 160 120 160 72 Z" stroke="{AM}" stroke-width="2.2" fill="{AM}" fill-opacity=".05"/>'
          f'<path class="top" d="M104 92 H152 C150 118 132 132 128 142 C124 132 106 118 104 92 Z" fill="{AM}" fill-opacity=".8"/>'
          f'<path class="bot" d="M100 226 H156 C150 196 136 190 128 186 C120 190 106 196 100 226 Z" fill="{AM}" fill-opacity=".8"/>'
          f'<line x1="128" y1="146" x2="128" y2="222" stroke="{AM}" stroke-width="2" class="stream"/>'
          + "".join(f'<g class="coin" style="animation-delay:-{k * 1.2:.1f}s"><circle cx="{[200, 58, 210][k]}" cy="{[96, 118, 196][k]}" r="11" stroke="{AM}" stroke-width="1.6" fill="{C["deep"]}"/>'
                    f'<text x="{[200, 58, 210][k]}" y="{[100, 122, 200][k]}" class="mb" font-size="11" fill="{AM}" text-anchor="middle">H</text></g>' for k in range(3)))
    hz_css = (".top{transform-origin:128px 92px;animation:top 4s ease-in infinite}@keyframes top{from{transform:scaleY(1)}to{transform:scaleY(.15)}}"
              ".bot{transform-origin:128px 226px;animation:bot 4s ease-out infinite}@keyframes bot{from{transform:scaleY(.2)}to{transform:scaleY(1)}}"
              ".stream{stroke-dasharray:4 6;animation:march .6s linear infinite reverse}"
              ".coin{animation:coin 3.6s ease-in-out infinite}@keyframes coin{0%,100%{transform:translateY(0);opacity:.5}50%{transform:translateY(-8px);opacity:1}}")
    product_card("HOURz", "hourz", "HOURz",
                 ["A platform where time is the currency —", "buy and sell hours, seize the day."],
                 "hourz.ai", ["PRODUCTIVITY", "TIME ECONOMY"], AM, hg, hz_css)

    # CVmaker: a personal site assembling itself
    url = "maker.cv/your-name"
    uw = measure(url, "IZ Mono", 10.5)
    clip, caret = typing_clip("cvt", 76, 70, 20, uw, len(url), 0.4, 0.09, 2.4, 6)
    cv = [f'<defs>{clip}</defs>',
          f'<rect x="58" y="60" width="140" height="180" rx="12" fill="{C["panel2"]}" stroke="{M}" stroke-width="2"/>',
          f'<rect x="58" y="60" width="140" height="22" rx="12" fill="{M}" fill-opacity=".14"/>',
          f'<g clip-path="url(#cvt)">{text(76, 75, url, "m", 10.5, M)}</g>',
          f'<rect x="78" y="66" width="1.5" height="12" fill="{M}" class="blink">{caret}</rect>',
          f'<circle cx="92" cy="114" r="18" fill="{M}" fill-opacity=".25" stroke="{M}" stroke-width="1.6"/>',
          f'<circle cx="92" cy="109" r="6" fill="{M}"/><path d="M80 126 c4 -8 20 -8 24 0" stroke="{M}" stroke-width="2"/>']
    for k, (y, wv) in enumerate([(106, 70), (122, 52), (156, 104), (172, 92), (188, 104), (204, 72), (220, 86)]):
        cv.append(f'<rect class="ln" style="animation-delay:{k * .25:.2f}s" x="{118 if k < 2 else 76}" y="{y}" width="{wv if k < 2 else wv}" height="6" rx="3" fill="{M}" fill-opacity="{.75 if k < 2 else .35}"/>')
    cv_css = ".ln{transform-box:fill-box;animation:ln 6s ease-out infinite}@keyframes ln{0%,8%{transform:scaleX(0)}30%,90%{transform:scaleX(1)}100%{transform:scaleX(0)}}"
    product_card("CVmaker", "cvmaker", "CVmaker",
                 ["From your name to a live, shareable", "CV website — in minutes, no code."],
                 "maker.cv", ["NO-CODE", "PERSONAL SITES"], M, "".join(cv), cv_css)


# ------------------------------------------------------- stack constellation
def stack():
    H = 600
    cx, cy = 640, 300
    rings = [
        (200, 70, 46, C["aqua"], "INTELLIGENCE", ["LLMs", "PyTorch", "TensorFlow", "Hugging Face"]),
        (372, 146, 80, C["blue"], "PLATFORM", ["Kubernetes", "Docker", "Terraform", "Ansible", "GitHub Actions", "Linux", "Nginx"]),
        (548, 232, 130, C["violet"], "CLOUD & CODE", ["AWS", "Python", "Azure", "Node.js", "React", "Google Cloud",
                                                         "Laravel", "PostgreSQL", "TypeScript", "Redis"]),
    ]
    defs = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<radialGradient id="cg"><stop offset="0" stop-color="{C["blue"]}" stop-opacity=".45"/><stop offset="1" stop-color="{C["blue"]}" stop-opacity="0"/></radialGradient>'
    )
    b = [stars(W, H, 110, seed=3)]
    b.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="url(#cg)"/>')
    tilt = -8
    for k, (rx, ry, dur, col, lab, items) in enumerate(rings):
        d = f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0"
        b.append(f'<g transform="rotate({tilt} {cx} {cy})"><path id="o{k}" d="{d}" stroke="{col}" stroke-opacity=".38" stroke-dasharray="{"3 6" if k % 2 else "1 0"}"/></g>')
    # core
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="{C["void"]}" stroke="{C["sky"]}" stroke-width="2" filter="url(#glow)"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" stroke="{C["aqua"]}"><animate attributeName="r" values="44;90" dur="3s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".8;0" dur="3s" repeatCount="indefinite"/></circle>')
    b.append(text(cx, cy + 9, "IZ", "d", 28, C["text"], "middle", 'letter-spacing="-1"'))
    # orbiting chips: the orbit path is rotated, so wrap motion in the same rotation and keep text upright
    for k, (rx, ry, dur, col, lab, items) in enumerate(rings):
        n = len(items)
        for j, it in enumerate(items):
            w = measure(it, "IZ Mono", 13, 0.4) + 34
            beg = -dur * j / n
            b.append(
                f'<g transform="rotate({tilt} {cx} {cy})"><g><animateMotion dur="{dur}s" begin="{beg:.2f}s" repeatCount="indefinite"><mpath href="#o{k}"/></animateMotion>'
                f'<g transform="rotate({-tilt})">'
                f'<rect x="{-w / 2:.1f}" y="-15" width="{w:.1f}" height="30" rx="15" fill="{C["panel"]}" stroke="{col}" stroke-opacity=".75"/>'
                f'<circle cx="{-w / 2 + 14:.1f}" cy="0" r="3.5" fill="{col}"/>'
                + text(-w / 2 + 24, 4.6, it, "m", 13, C["text"], extra='letter-spacing=".4"')
                + "</g></g></g>"
            )
    # legend
    x = 40
    for rx, ry, dur, col, lab, items in rings:
        b.append(f'<circle cx="{x + 5}" cy="{H - 34}" r="5" fill="{col}"/>')
        b.append(text(x + 18, H - 29.5, lab, "m", 12, C["soft"], extra='letter-spacing="2.5"'))
        x += measure(lab, "IZ Mono", 12, 2.5) + 50
    b.append(text(W - 40, H - 29.5, "AWS · AZURE · GOOGLE CLOUD · ON-PREM · AIR-GAPPED", "m", 12, C["muted"], "end", 'letter-spacing="1.5"'))
    write("stack.svg", svg(W, H, "".join(b), "INZOX technology constellation",
          "Three orbits of technologies around the INZOX core. Intelligence: LLMs, PyTorch, TensorFlow, Hugging Face. "
          "Platform: Kubernetes, Docker, Terraform, Ansible, GitHub Actions, Linux, Nginx. Cloud and code: AWS, Azure, "
          "Google Cloud, Python, Node.js, TypeScript, React, Laravel, PostgreSQL, Redis.", defs=defs))


# --------------------------------------------------------------- global map
def _land_polys():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ne_110m_land.geojson")) as f:
        gj = json.load(f)
    polys = []
    for feat in gj["features"]:
        g = feat["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            ring = poly[0]
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            polys.append((ring, min(xs), max(xs), min(ys), max(ys)))
    return polys


def _inside(lon, lat, ring):
    hit = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def world():
    H = 640
    mx0, my0, mw = 40, 34, 1200
    lat_top, lat_bot = 80, -58
    sc = mw / 360
    mh = (lat_top - lat_bot) * sc

    def proj(lon, lat):
        return mx0 + (lon + 180) * sc, my0 + (lat_top - lat) * sc

    polys = _land_polys()
    step = 9
    segs = []
    y = my0 + step / 2
    while y < my0 + mh:
        x = mx0 + step / 2
        lat = lat_top - (y - my0) / sc
        while x < mx0 + mw:
            lon = (x - mx0) / sc - 180
            for ring, x1, x2, y1, y2 in polys:
                if x1 <= lon <= x2 and y1 <= lat <= y2 and _inside(lon, lat, ring):
                    segs.append(f"M{x:.0f} {y:.0f}h0")
                    break
            x += step
        y += step
    css = """
.scanl{animation:scanl 7s linear infinite}
@keyframes scanl{from{transform:translateX(-140px)}to{transform:translateX(1400px)}}
.flow{stroke-dasharray:5 7;animation:march .9s linear infinite}
.grow{stroke-dasharray:1000;animation:grow 6s ease-out infinite}
@keyframes grow{0%{stroke-dashoffset:1000}60%,100%{stroke-dashoffset:0}}
"""
    defs = (
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{C["aqua"]}" stop-opacity="0"/>'
        f'<stop offset=".85" stop-color="{C["aqua"]}" stop-opacity=".09"/><stop offset="1" stop-color="{C["aqua"]}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="tl" x1="0" x2="1"><stop offset="0" stop-color="{C["aqua"]}"/><stop offset=".7" stop-color="{C["blue"]}"/>'
        f'<stop offset="1" stop-color="{C["violet"]}"/></linearGradient>'
    )
    b = [f'<path d="{"".join(segs)}" stroke="{C["dim"]}" stroke-width="3.6" stroke-linecap="round"/>']
    b.append(f'<g class="scanl"><rect x="{mx0 - 120}" y="{my0}" width="120" height="{mh:.0f}" fill="url(#scan)"/></g>')
    sites = [
        ("ALEXANDRIA · EGYPT", "HQ · R&D · Engineering · Academy", 29.9, 31.2, C["aqua"], (1, -1)),
        ("DELAWARE · USA", "Business development", -75.5, 39.7, C["blue"], (-1, -1)),
        ("KUALA LUMPUR · MALAYSIA", "APAC operations", 101.7, 3.1, C["violet"], (1, 1)),
    ]
    hq = proj(sites[0][2], sites[0][3])
    for k, (_, _, lon, lat, col, _) in enumerate(sites[1:], 1):
        x, y = proj(lon, lat)
        mxp, myp = (hq[0] + x) / 2, min(hq[1], y) - (150 if k == 1 else 90)
        d = f"M{hq[0]:.1f},{hq[1]:.1f} Q{mxp:.1f},{myp:.1f} {x:.1f},{y:.1f}"
        b.append(f'<path d="{d}" stroke="{col}" stroke-width="1.5" stroke-opacity=".35"/>')
        b.append(f'<path id="arc{k}" d="{d}" stroke="{col}" stroke-width="2" class="flow"/>')
        b.append(f'<circle r="4" fill="#fff" filter="url(#glow)"><animateMotion dur="3.2s" begin="-{k * 1.3:.1f}s" repeatCount="indefinite"><mpath href="#arc{k}"/></animateMotion></circle>')
    for name, role, lon, lat, col, (sx, sy) in sites:
        x, y = proj(lon, lat)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{col}" filter="url(#glow)"/>')
        for dly in (0, 1.3):
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" stroke="{col}" stroke-width="1.5">'
                     f'<animate attributeName="r" values="7;34" dur="2.6s" begin="-{dly}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="1;0" dur="2.6s" begin="-{dly}s" repeatCount="indefinite"/></circle>')
        tw = max(measure(name, "IZ MonoBold", 12, 1.5), measure(role, "IZ Mono", 11.5)) + 28
        bx = x + 26 if sx > 0 else x - 26 - tw
        by = y - 70 if sy < 0 else y + 22
        b.append(f'<path d="M{x:.1f},{y:.1f} L{(bx if sx > 0 else bx + tw):.1f},{by + 24:.1f}" stroke="{col}" stroke-opacity=".6"/>')
        b.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{tw:.1f}" height="48" rx="10" fill="{C["void"]}" fill-opacity=".9" stroke="{col}" stroke-opacity=".7"/>')
        b.append(text(bx + 14, by + 20, name, "mb", 12, col, extra='letter-spacing="1.5"'))
        b.append(text(bx + 14, by + 37, role, "m", 11.5, C["soft"]))
    # timeline
    ty = 560
    pts = [("2018", "Founded in Alexandria, Egypt"), ("2020", "Expanded to the United States"),
           ("2024", "Venturing into Malaysia · APAC"), ("NEXT", "Building the future of DeepTech")]
    x1, x2 = 150, W - 170
    b.append(f'<line x1="{x1}" x2="{x2}" y1="{ty}" y2="{ty}" stroke="{C["line"]}" stroke-width="3"/>')
    b.append(f'<line x1="{x1}" x2="{x2}" y1="{ty}" y2="{ty}" stroke="url(#tl)" stroke-width="3" class="grow"/>')
    for k, (yr, lab) in enumerate(pts):
        x = x1 + k * (x2 - x1) / 3
        fut = yr == "NEXT"
        b.append(f'<circle cx="{x:.0f}" cy="{ty}" r="8" fill="{C["void"]}" stroke="{C["violet"] if fut else C["aqua"]}" stroke-width="2.5"'
                 + (' class="pulse"' if fut else "") + "/>")
        b.append(text(x, ty - 20, yr, "d", 20, C["text"], "middle"))
        b.append(text(x, ty + 32, lab, "m", 11.5, C["soft"], "middle"))
    write("global.svg", svg(W, H, "".join(b), "INZOX around the world",
          "Dotted world map with animated links from the Alexandria, Egypt headquarters to Delaware, USA and Kuala Lumpur, "
          "Malaysia, above a timeline: 2018 founded in Alexandria, 2020 expanded to the United States, 2024 Malaysia, "
          "next: building the future of DeepTech.", css=css, defs=defs))


# ------------------------------------------------------------------ contact
def cta():
    H = 300
    defs = (
        f'<linearGradient id="hg" gradientUnits="userSpaceOnUse" x1="300" x2="980" y1="0" y2="0"><stop offset="0" stop-color="#fff"/>'
        f'<stop offset=".6" stop-color="{C["ice"]}"/><stop offset="1" stop-color="{C["aqua"]}"/></linearGradient>'
        f'<linearGradient id="wv" x1="0" x2="1"><stop offset="0" stop-color="{C["aqua"]}" stop-opacity="0"/><stop offset=".5" stop-color="{C["blue"]}"/>'
        f'<stop offset="1" stop-color="{C["violet"]}" stop-opacity="0"/></linearGradient>'
    )
    css = ".w1{animation:wv 6s linear infinite}.w2{animation:wv 9s linear infinite reverse}@keyframes wv{to{transform:translateX(-320px)}}"
    b = [stars(W, H, 50, seed=21)]
    for k, (cls, amp, yy, op) in enumerate([("w1", 26, 210, .6), ("w2", 18, 222, .35)]):
        d = f"M-40 {yy} " + " ".join(f"q 80 {-amp} 160 0 t 160 0" for _ in range(6))
        b.append(f'<path class="{cls}" d="{d}" stroke="url(#wv)" stroke-width="2" opacity="{op}"/>')
    b.append(text(W / 2, 74, "WE DELIVER FIRST", "m", 14, C["aqua"], "middle", 'letter-spacing="6"'))
    b.append(text(W / 2, 136, "Let’s build something", "d", 50, "url(#hg)", "middle", 'letter-spacing="-1"'))
    b.append(text(W / 2, 192, "extraordinary together.", "d", 50, "url(#hg)", "middle", 'letter-spacing="-1"'))
    b.append(text(W / 2, 262, "Technology solutions  ·  Innovation  ·  Training  ·  Investment  ·  Partnerships", "m", 13, C["muted"], "middle", 'letter-spacing="1.2"'))
    write("contact.svg", svg(W, H, "".join(b), "Let's build something extraordinary together",
          "Closing banner: We Deliver First. Let's build something extraordinary together.", css=css, defs=defs))


BTN_ICONS = {
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
    "brain": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1" fill="currentColor"/><path d="M12 1v3M12 20v3M1 12h3M20 12h3"/>',
    "in": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 10.5V16M8 7.6v.1M11.5 16v-5.5M11.5 13c0-1.6 1-2.6 2.4-2.6S16 11.4 16 13v3"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M8 15h3"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>',
    "bag": '<rect x="3" y="7" width="18" height="13" rx="3"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 12h18"/>',
}


def buttons():
    items = [("website", "globe", "inzox.com", C["sky"]), ("zox", "brain", "inzox.ai", C["cyan"]),
             ("linkedin", "in", "LinkedIn", C["blue"]), ("call", "cal", "Book a call", C["mint"]),
             ("careers", "bag", "Careers", C["amber"]), ("email", "mail", "Email us", C["lilac"])]
    h = 56
    for slug, ic, label, col in items:
        tw = measure(label, "IZ Display", 17)
        w = int(tw + 112)
        css = (f".sh{{animation:sh 5s ease-in-out infinite}}@keyframes sh{{0%,60%{{transform:translateX(-80px)}}100%{{transform:translateX({w + 80}px)}}}}")
        defs = (f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/>'
                f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="c"><rect width="{w}" height="{h}" rx="{h / 2}"/></clipPath>')
        b = (f'<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{C["deep"]}"/>'
             f'<rect class="sh" x="0" y="0" width="60" height="{h}" fill="url(#g)" transform="skewX(-20)"/></g>'
             f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{h / 2 - .75}" stroke="{col}" stroke-opacity=".7" stroke-width="1.5"/>'
             f'<g transform="translate(22 16)" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" color="{col}">{BTN_ICONS[ic]}</g>'
             + text(58, 34, label, "d", 17, C["text"])
             + f'<path d="M{w - 34} {h / 2 + 5} l9 -9 m-6 0 h6 v6" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        write(f"btn-{slug}.svg", svg(w, h, b, label, f"{label} button", css=css, defs=defs, panel=False))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero()
    manifesto()
    sections = [
        ("01", "WHAT WE DO", "Six disciplines. One delivery engine."),
        ("02", "HOW WE SHIP", "Security on every pass of the loop."),
        ("03", "SOVEREIGN AI", "ZOX — the Enterprise AI Brain."),
        ("04", "PRODUCT LAB", "Born in our DeepTech R&D lab."),
        ("05", "THE STACK", "The toolchain behind the work."),
        ("06", "GLOBAL", "Three branches. One engineering culture."),
        ("07", "CONNECT", "Weeks of work. Minutes to start."),
    ]
    for idx, eb, title in sections:
        header(f"section-{idx}.svg", idx, eb, title)
    capabilities()
    devsecops()
    zox()
    products()
    stack()
    world()
    cta()
    buttons()
