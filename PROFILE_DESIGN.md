# INZOX GitHub organization profile: design notes

This document covers how the public profile at
[github.com/INZOX-LLC](https://github.com/INZOX-LLC) is built, what was
changed, how it was validated against GitHub's rendering rules, and what to do
next.

---

## 1. What changed

| Before | After |
| --- | --- |
| 39-line plain-text README with emoji bullets and placeholder `[ repo 1 ]` links | Visual story in 7 chapters, made of 25 original animated SVGs |
| No brand assets | Brand system: palette, embedded typography, icon set, motion language |
| No source for artwork | Reproducible generator (`tools/build_assets.py`), so edits are code, not hand-drawn files |

**Files**

```
profile/
  README.md                 ← the rendered profile (HTML-in-Markdown)
  assets/                   ← generated SVGs (do not hand-edit)
tools/
  build_assets.py           ← one function per asset
  brand.py                  ← palette, font embedding, text measuring, helpers
  fonts/                    ← Space Grotesk + JetBrains Mono (SIL OFL 1.1, licences included)
  ne_110m_land.geojson      ← Natural Earth land outlines (public domain), used for the dotted map
PROFILE_DESIGN.md           ← this file
.gitignore                  ← keeps public_html/ (website source, contains .env) out of the repo
```

---

## 2. The story the page tells

| # | Asset | What it shows | Motion |
|---|---|---|---|
| — | `hero.svg` | INZOX wordmark, "Turning weeks into minutes.", a reticle-shaped AI core (it echoes the ZOX favicon) labelled AI Engineering / Cloud & FinOps / DevSecOps / Automation | Radar sweep, counter-rotating rings, orbiting satellites, a perspective grid rolling forward, packets dropping into the grid, a terminal typing `inzox deliver --weeks-to-minutes` → `✓ We Deliver First`, a shimmer across the wordmark |
| — | `manifesto.svg` | An 8-week Gantt chart of delivery phases next to the mission line and stats (7+ years, 300+ projects, 100+ team members, 3 offices) | The Gantt compresses into minutes, "Weeks" gets struck through, and the caption swaps to "With INZOX · Minutes" |
| 01 | `capabilities.svg` | Circuit board: the INZOX delivery engine wired to six capability cards with custom icons | Signal pulses run along the traces, and each card's border lights up as its pulse arrives |
| 02 | `devsecops.svg` | Infinity loop of the INZOX solutions framework (Discover → Analyze → Architect → Develop → Deploy → Optimize), with 8 security gates on the path and a shield where the loops cross | A comet trail and packets circle the loop, gates pulse, the shield ring rotates |
| 03 | `zox.svg` | ZOX, the Enterprise AI Brain: an isometric 4-layer stack (Data → Intelligence → Reasoning → Decision) inside a "your perimeter" boundary, four engines, deployment badges | Data rises through the layers, layers light up in sequence, the perimeter border marches, an outbound packet is blocked at the wall (zero egress) |
| 04 | `product-*.svg` ×4 | OX.Report, Docker.Boats, HOURz, CVmaker cards, each with its own animated glyph | X-ray scan with audit scores, a container ship bobbing on waves, a running hourglass with "H" tokens, a CV site assembling itself while its URL types out |
| 05 | `stack.svg` | Technology constellation: three tilted orbits (Intelligence / Platform / Cloud & Code) | Chips orbit the core and stay upright as they move |
| 06 | `global.svg` | Dotted world map built from Natural Earth data, with Alexandria (HQ), Delaware and Kuala Lumpur, plus the 2018 → 2020 → 2024 → Next timeline | Packets fly along arcs from HQ, nodes pulse, a scan beam crosses the map, the timeline draws itself |
| 07 | `contact.svg` + `btn-*.svg` ×6 | "Let's build something extraordinary together." and buttons for inzox.com, inzox.ai, LinkedIn, Book a call, Careers, Email | Waveforms, a shine passing over each button |
| | `section-0N.svg` ×7 | Chapter headers: outlined numeral, eyebrow, gradient title | A packet travels the rail |

A collapsible **"Read this profile as plain text"** section at the bottom
repeats the content as real text, for screen readers, search engines and
anyone who browses with images off.

**Mermaid is not used anywhere.** Every diagram is a hand-built SVG.

---

## 3. Sources of truth (authentic content only)

Every fact on the page came from INZOX's own properties:

- **inzox.com** and the website source (`public_html/database/seeders/*`):
  the "We Deliver First" eyebrow, "Turning Weeks Into Minutes Through
  DeepTech Innovation", the stats (`ImpactStatSeeder`), services
  (`ServiceSeeder`, `InnovationTechAreaSeeder`), the six-step framework
  (`SolutionsFrameworkStepSeeder`), offices and timeline (`OfficeSeeder`,
  `TimelineEventSeeder`), the tech list (`TechPartnerSeeder`) and contact
  links (`SiteSettingSeeder`).
- **Product pages** (`inzox.com/products/*`): copy for OX.Report,
  Docker.Boats, HOURz and CVmaker, and the product domains.
- **inzox.ai**: ZOX positioning, the four engines, the four-layer
  architecture, deployment modes and the zero-egress messaging, all taken
  from the site's own catalogue copy. The ZOX reticle mark is redrawn from
  `inzox.ai/favicon.svg`.
- **GitHub org** (`gh api orgs/INZOX-LLC`, `gh repo list`): all four
  product repos are **private**, so none are named or linked on the public
  page.

Nothing on the page claims a customer, certification or metric that INZOX
does not already publish. The "Traditional delivery" Gantt chart is
explicitly an illustration.

---

## 4. GitHub rendering rules, and how each was validated

| Constraint | How the design handles it | Verified by |
|---|---|---|
| The README sanitizer strips `<style>`, `<script>`, `class`, `id` and `style` | Layout uses only `align`, `width`, `height`, `<a>`, `<img>`, `<br>`, `<details>` and `<sub>` | Rendered through `gh api markdown` (GFM mode): all 25 images and attributes survived |
| SVGs load as `<img>`, so no scripts, no external fetches and no interaction | Every SVG is self-contained. Animation is CSS `@keyframes` and SMIL (`animate`, `animateMotion`, `animateTransform`) | Audit: no `http` hrefs, `<script>` or `<image>` in any asset |
| No web fonts on GitHub | Fonts are subset per asset to only the glyphs it uses, then embedded as base64 WOFF2 (≈5–15 KB each) with system fallbacks | Viewed on github.com: Space Grotesk and JetBrains Mono render under GitHub's `default-src 'none'` SVG CSP |
| Relative paths on org profiles | Root-relative `/profile/assets/…` paths (the same pattern Appwrite uses) | Viewed on github.com: all images resolve; served as `image/svg+xml` |
| Light and dark themes | Each scene is a self-contained dark "console" panel with rounded corners, so it reads the same in both themes. Section headers are transparent and use mid-tone blue/violet, which works on white and on `#0d1117` | Full-page previews in light and dark GitHub chrome |
| Responsive layout | Every image is `width="100%"` or `49%`, and buttons use a fixed `height`, so they wrap on narrow screens | Previews at desktop and narrow widths |
| Motion sensitivity | `@media (prefers-reduced-motion: reduce)` stops CSS animation in every asset | Present in the shared base CSS |
| Page weight | 25 files, about 457 KB total. The largest is about 45 KB | Build output |
| Clickable images | Each scene links somewhere useful (services, DevOps, inzox.ai, the product sites, contact). Headers fall back to GitHub's default image link | Rendered HTML |
| Accessibility | Every `<img>` has descriptive `alt`, every SVG has `role="img"` plus `<title>`/`<desc>`, and a plain-text `<details>` fallback is included | — |

Animation was confirmed frame by frame in real Chrome via the DevTools
protocol: typing, radar, orbits, Gantt compression, arcs and orbiting chips
all advance.

---

## 5. Design system

**Palette.** INZOX web blues fused with ZOX cyans:

| Token | Hex | Use |
|---|---|---|
| void / deep | `#030614` / `#060D24` | Panel backgrounds |
| blue | `#1684FF` | Primary brand (inzox.com) |
| sky / ice | `#52A4F6` / `#87C3FF` | Secondary strokes, wordmark gradient |
| cyan / aqua | `#2EB8EA` / `#4FD2FF` | ZOX and "minutes" accents |
| violet | `#9747FF` | Gradient end, reasoning layer |
| mint | `#22E3A6` | Security, success states |
| amber / rose | `#FFB547` / `#FF5C7A` | Academy and HOURz / blocked and danger |

**Type.** Space Grotesk 700 (display), Space Grotesk 500 (body),
JetBrains Mono 500/700 (labels, eyebrows, terminal). Mono text in capitals
with wide tracking gives the "engineering console" voice.

**Motion.** Slow ambient motion (orbits at 15–130 s, rings at 14–48 s) plus
one short "story" loop per scene (6–9 s). Nothing flashes.

---

## 6. Regenerating the artwork

```bash
python3 -m venv .venv
.venv/bin/pip install fonttools brotli
.venv/bin/python tools/build_assets.py      # writes profile/assets/*.svg
```

- Change copy, stats or products in `tools/build_assets.py`. Each asset has
  its own function, and section titles are listed in `__main__`.
- Change colours or fonts in `tools/brand.py`. Text widths are measured from
  the real font metrics, so chips and labels resize themselves.
- Validate with `xmllint --noout profile/assets/*.svg`, then preview on a
  branch at `github.com/INZOX-LLC/.github/blob/<branch>/profile/README.md`
  before merging to `main`.

---

## 7. Recommendations

**Org settings** (Settings → Profile; these need an org owner):
1. Add a **description** ("DeepTech R&D lab: AI, DevSecOps, Cloud
   Engineering. We Deliver First."), **website** `https://inzox.com`,
   **location** "Alexandria · Delaware · Kuala Lumpur" and the **LinkedIn**
   social link. The API currently returns `description: null`.
2. **Verify the domains** `inzox.com` and `inzox.ai` to get the "Verified"
   badge next to the org name.
3. Upload a **high-resolution avatar**. The current `logo.png` is only
   195×57; a square mark on `#030614` would match this profile.

**Content**
4. **Publish at least one public repository** (an SDK, a Terraform module, a
   GitHub Action, or a docs/samples repo for ZOX or Docker.Boats) and **pin**
   it. Pinned repos show directly under the README and are the strongest
   credibility signal for an engineering company.
5. Add a **members-only profile** (`INZOX-LLC/.github-private` →
   `profile/README.md`) for internal onboarding links. It shows only to org
   members.
6. Add community health defaults to this repo (`SECURITY.md`,
   `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates). They apply to
   every public repo in the org, and `SECURITY.md` fits the DevSecOps story.
7. Keep stats in sync with inzox.com. They appear in `manifesto()`.

**Optional enhancements**
8. Add a GitHub Action that runs `tools/build_assets.py` on push and fails if
   `profile/assets` is out of date.
9. Set a custom **social preview image** on public repos, using the hero
   artwork rendered to PNG at 1280×640.
10. If the org adds GitHub Discussions or events (for example GITEX 2026), a
    small "Now" strip can be added under the hero as another generated SVG.

**Guardrails**
- Never add `public_html/` to this repo. It contains the website's `.env`,
  and `.gitignore` already excludes it.
- Keep private repo names off the public profile.
- Don't use Mermaid or third-party stat widgets. They break the visual system
  and add external dependencies.
