#!/usr/bin/env python3
"""
Tema compartilhado para os assets do perfil do GitHub.
"""

from html import escape

PALETTE = {
    "bg": "#0D1117",
    "panel": "#161B22",
    "surface": "#21262D",
    "border": "#30363D",
    "accent": "#58A6FF",
    "accent_soft": "#79C0FF",
    "text": "#F0F6FC",
    "muted": "#8B949E",
}

FONT_STACK = "'Segoe UI', Inter, system-ui, sans-serif"


def format_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def safe_pill(label: str) -> str:
    cleaned = "".join(ch for ch in label.upper() if ch.isalnum())
    return (cleaned[:8] or "DEV")


def render_pixel_cat(x: int, y: int, opacity: float = 0.72) -> str:
    return f"""
  <g transform="translate({x} {y})" shape-rendering="crispEdges" opacity="{opacity}">
    <g transform="translate(0 14)">
      <animateTransform attributeName="transform" type="rotate" values="0 4 6;10 4 6;0 4 6;-6 4 6;0 4 6" dur="7s" repeatCount="indefinite" />
      <rect x="0" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="4" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="0" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="8" width="4" height="4" fill="{PALETTE['border']}" />
    </g>
    <g>
      <rect x="12" y="0" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="0" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="16" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="20" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="28" y="4" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="16" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="20" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="28" y="8" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="8" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="16" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="20" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="28" y="12" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="16" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="16" y="16" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="20" y="16" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="16" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="20" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="16" y="20" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="20" y="20" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="20" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="24" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="24" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="12" y="28" width="4" height="4" fill="{PALETTE['border']}" />
      <rect x="24" y="28" width="4" height="4" fill="{PALETTE['border']}" />
    </g>
    <g fill="{PALETTE['text']}">
      <rect x="16" y="12" width="4" height="4">
        <animate attributeName="opacity" values="1;1;1;0;1;1" dur="6.5s" repeatCount="indefinite" />
      </rect>
      <rect x="24" y="12" width="4" height="4">
        <animate attributeName="opacity" values="1;1;1;0;1;1" dur="6.5s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>"""


def panel_frame(width: int, height: int) -> str:
    return f"""
  <rect width="{width}" height="{height}" rx="28" fill="{PALETTE['bg']}" />
  <rect x="14" y="14" width="{width - 28}" height="{height - 28}" rx="26" fill="url(#panelFill)" stroke="{PALETTE['border']}" stroke-width="2" />
  <rect x="34" y="34" width="{width - 68}" height="{height - 68}" rx="22" fill="none" stroke="{PALETTE['surface']}" stroke-width="1" />"""


def base_defs(extra: str = "") -> str:
    return f"""
  <defs>
    <linearGradient id="panelFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{PALETTE['panel']}" />
      <stop offset="100%" stop-color="{PALETTE['bg']}" />
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{PALETTE['accent']}" />
      <stop offset="100%" stop-color="{PALETTE['accent_soft']}" />
    </linearGradient>
    <style>
      text {{ font-family: {FONT_STACK}; }}
      .title {{ fill: {PALETTE['text']}; font-size: 24px; font-weight: 600; text-anchor: middle; }}
      .label {{ fill: {PALETTE['text']}; font-size: 18px; font-weight: 600; }}
      .value {{ fill: {PALETTE['muted']}; font-size: 18px; font-weight: 600; text-anchor: end; }}
      .pill-text {{ fill: {PALETTE['accent_soft']}; font-size: 14px; font-weight: 700; text-anchor: middle; dominant-baseline: middle; }}
      .eyebrow {{ fill: {PALETTE['accent_soft']}; font-size: 14px; font-weight: 700; text-anchor: middle; letter-spacing: 1.2px; }}
      .headline {{ fill: {PALETTE['text']}; font-size: 54px; font-weight: 700; text-anchor: middle; }}
      .subtitle {{ fill: {PALETTE['muted']}; font-size: 20px; font-weight: 500; text-anchor: middle; }}
      .body {{ fill: {PALETTE['muted']}; font-size: 16px; font-weight: 400; text-anchor: middle; }}
      .chip-text {{ fill: {PALETTE['text']}; font-size: 15px; font-weight: 600; text-anchor: middle; dominant-baseline: middle; }}
    </style>
    {extra}
  </defs>"""


def build_card_svg(title: str, rows: list[dict], description: str) -> str:
    width = 1200
    height = 540
    top = 132
    row_height = 56
    gap = 14
    bar_x = 520
    bar_w = 430
    row_blocks = []

    for index, row in enumerate(rows):
        y = top + index * (row_height + gap)
        delay = 0.12 + index * 0.08
        pill = escape(row["pill"])
        label = escape(row["label"])
        value = escape(row["value"])
        ratio = max(0.0, min(1.0, float(row["ratio"])))
        row_blocks.append(
            f"""
    <g transform="translate(72 {y})">
      <animateTransform attributeName="transform" type="translate" values="72 {y + 8};72 {y}" dur="{0.42 + index * 0.05:.2f}s" fill="freeze" />
      <animate attributeName="opacity" values="0;1" dur="{0.42 + index * 0.05:.2f}s" fill="freeze" />
      <rect width="1056" height="{row_height}" rx="16" fill="{PALETTE['bg']}" stroke="{PALETTE['surface']}" stroke-width="2" />
      <rect x="18" y="13" width="94" height="30" rx="15" fill="{PALETTE['panel']}" stroke="{PALETTE['border']}" stroke-width="1.5" />
      <text x="65" y="28" class="pill-text">{pill}</text>
      <text x="136" y="28" class="label">{label}</text>
      <text x="1020" y="28" class="value">{value}</text>
      <rect x="{bar_x}" y="23" width="{bar_w}" height="10" rx="5" fill="{PALETTE['surface']}" />
      <rect x="{bar_x}" y="23" width="0" height="10" rx="5" fill="url(#accent)">
        <animate attributeName="width" values="0;{bar_w * ratio:.1f}" dur="0.85s" begin="{delay:.2f}s" fill="freeze" />
      </rect>
      <rect x="{bar_x}" y="23" width="{bar_w}" height="10" rx="5" fill="none" stroke="{PALETTE['border']}" stroke-width="1" />
    </g>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
{base_defs()}
{panel_frame(width, height)}
  <text x="{width / 2:.0f}" y="84" class="title">{escape(title)}</text>
  <line x1="520" y1="100" x2="680" y2="100" stroke="url(#accent)" stroke-width="4" stroke-linecap="round" opacity="0.9" />
  <g>
{''.join(row_blocks)}
  </g>
{render_pixel_cat(1100, 474)}
</svg>
"""


def build_header_svg(name: str, role: str, tagline: str, chips: list[str]) -> str:
    width = 1200
    height = 320
    chip_centers = [420, 600, 780]
    chip_blocks = []
    for x, chip in zip(chip_centers, chips[:3]):
        chip_blocks.append(
            f"""
  <g transform="translate({x} 238)">
    <rect x="-88" y="-18" width="176" height="36" rx="18" fill="{PALETTE['bg']}" stroke="{PALETTE['surface']}" stroke-width="1.5" />
    <text x="0" y="2" class="chip-text">{escape(chip)}</text>
  </g>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(name)}</title>
  <desc id="desc">Cabeçalho minimalista do portfólio no GitHub.</desc>
{base_defs()}
{panel_frame(width, height)}
  <g opacity="0.55">
    <line x1="94" y1="88" x2="286" y2="88" stroke="{PALETTE['border']}" stroke-width="1" />
    <line x1="914" y1="88" x2="1106" y2="88" stroke="{PALETTE['border']}" stroke-width="1" />
    <line x1="94" y1="232" x2="286" y2="232" stroke="{PALETTE['border']}" stroke-width="1" />
    <line x1="914" y1="232" x2="1106" y2="232" stroke="{PALETTE['border']}" stroke-width="1" />
  </g>
  <text x="600" y="86" class="eyebrow">GITHUB PROFILE</text>
  <text x="600" y="146" class="headline">{escape(name)}</text>
  <line x1="500" y1="164" x2="700" y2="164" stroke="url(#accent)" stroke-width="4" stroke-linecap="round" opacity="0.9" />
  <text x="600" y="196" class="subtitle">{escape(role)}</text>
  <text x="600" y="224" class="body">{escape(tagline)}</text>
  {''.join(chip_blocks)}
{render_pixel_cat(1098, 248, 0.64)}
</svg>
"""


def build_footer_svg(name: str, message: str) -> str:
    width = 1200
    height = 120
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
  <title id="title">Footer</title>
  <desc id="desc">Rodapé minimalista do perfil.</desc>
{base_defs()}
{panel_frame(width, height)}
  <line x1="160" y1="42" x2="1040" y2="42" stroke="{PALETTE['border']}" stroke-width="1" />
  <line x1="510" y1="42" x2="690" y2="42" stroke="url(#accent)" stroke-width="3" stroke-linecap="round" opacity="0.9" />
  <text x="600" y="76" class="subtitle">{escape(name)}</text>
  <text x="600" y="98" class="body">{escape(message)}</text>
{render_pixel_cat(1088, 62, 0.62)}
</svg>
"""
