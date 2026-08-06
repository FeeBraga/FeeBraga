#!/usr/bin/env python3
"""
Gera o card de linguagens principais usando a API do GitHub.
"""

import os
from collections import Counter

import requests

from profile_theme import build_card_svg, safe_pill

PILL_MAP = {
    "Python": "PY",
    "JavaScript": "JS",
    "TypeScript": "TS",
    "C#": "C#",
    "C++": "C++",
    "HTML": "HTML",
    "CSS": "CSS",
    "Go": "GO",
    "Rust": "RUST",
    "Java": "JAVA",
}


def fetch_language_stats() -> list[tuple[str, int]]:
    username = "FeeBraga"
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }
    headers = {key: value for key, value in headers.items() if value is not None}

    try:
        repos_response = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100",
            headers=headers,
            timeout=20,
        )
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        language_counter = Counter()
        for repo in repos_data:
            if isinstance(repo, dict) and repo.get("language"):
                language_counter[repo["language"]] += 1

        top_languages = language_counter.most_common(5)
        return top_languages or [("Python", 1), ("TypeScript", 1), ("C#", 1), ("JavaScript", 1), ("Other", 1)]
    except Exception as error:
        print(f"Error fetching language stats: {error}")
        return [("Python", 1), ("TypeScript", 1), ("C#", 1), ("JavaScript", 1), ("Other", 1)]


def generate_languages_svg(languages: list[tuple[str, int]]) -> None:
    total = sum(count for _, count in languages) or 1
    
    # Cores cyberpunk para o gráfico de pizza
    colors = {
        "Python": "#00FF94",
        "JavaScript": "#FF00FF", 
        "TypeScript": "#00FFFF",
        "C#": "#FF6B6B",
        "C++": "#FFD43B",
        "HTML": "#E34F26",
        "CSS": "#1572B6",
        "Go": "#00ADD8",
        "Rust": "#DEA584",
        "Java": "#007396",
    }
    
    # Gerar gráfico de pizza SVG mais aesthetic
    pie_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 140" width="400" height="140">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <rect width="400" height="140" fill="#0D1117" rx="12" stroke="#30363D" stroke-width="1" />
  
  <text x="200" y="28" font-family="Arial" font-size="16" fill="#00FFFF" text-anchor="middle" font-weight="bold" letter-spacing="1">TOP LANGUAGES</text>
  <line x1="50" y1="38" x2="350" y2="38" stroke="#FF00FF" stroke-width="1" opacity="0.5" />
"""
    
    # Criar gráfico de pizza
    cx, cy, r = 120, 85, 35
    circumference = 2 * 3.14159 * r
    
    current_angle = -90  # Começa do topo
    
    legend_y = 55
    for language, count in languages[:5]:
        percentage = (count / total) * 100
        color = colors.get(language, "#8B949E")
        
        # Calcular o ângulo para esta fatia
        angle = (count / total) * 360
        dash_array = f"{(angle / 360) * circumference} {circumference}"
        
        pie_svg += f"""
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="20" stroke-dasharray="{dash_array}" transform="rotate({current_angle} {cx} {cy})" filter="url(#glow)" />
"""
        current_angle += angle
        
        # Adicionar legenda mais bonita
        pie_svg += f"""
  <rect x="230" y="{legend_y - 8}" width="8" height="8" rx="2" fill="{color}" />
  <text x="245" y="{legend_y}" font-family="Arial" font-size="12" fill="#F0F6FC">{language}</text>
  <text x="380" y="{legend_y}" font-family="Arial" font-size="12" fill="#8B949E" text-anchor="end">{percentage:.0f}%</text>
"""
        legend_y += 18
    
    pie_svg += """
  <line x1="50" y1="130" x2="350" y2="130" stroke="#00FFFF" stroke-width="1" opacity="0.3" />
</svg>"""

    os.makedirs("profile", exist_ok=True)
    with open("profile/languages.svg", "w", encoding="utf-8") as file:
        file.write(pie_svg)

    print("Generated languages.svg with improved pie chart")


if __name__ == "__main__":
    generate_languages_svg(fetch_language_stats())
