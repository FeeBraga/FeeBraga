#!/usr/bin/env python3
"""
Gera o card de linguagens principais usando a API do GitHub com o design customizado.
"""

import os
from collections import Counter
import requests

USERNAME = "FeeBraga"

# Cores das linguagens
LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#F1E05A",
    "TypeScript": "#3178C6",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
    "C#": "#239120",
    "C++": "#F34B7D",
    "Java": "#B07219",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "Shell": "#89E051",
    "Jupyter Notebook": "#DA5B0B",
}

# Abreviações das linguagens
LANGUAGE_ABBR = {
    "Python": "Py",
    "JavaScript": "JS",
    "TypeScript": "TS",
    "HTML": "H5",
    "CSS": "CS",
    "Go": "Go",
    "Rust": "Rs",
    "C#": "C#",
    "C++": "C++",
    "Java": "Java",
    "Ruby": "Rb",
    "PHP": "PHP",
    "Swift": "Sw",
    "Kotlin": "Kt",
    "Dart": "Dt",
    "Shell": "Sh",
    "Jupyter Notebook": "Ip",
}


def fetch_language_stats() -> list[tuple[str, int]]:
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }
    headers = {k: v for k, v in headers.items() if v is not None}

    try:
        page = 1
        all_repos = []

        while True:
    repos_response = requests.get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}",
        headers=headers,
        timeout=20,
    )

    repos_response.raise_for_status()
    repos_data = repos_response.json()

    if not repos_data:
        break

    all_repos.extend(repos_data)
    page += 1

    # Limitar a 300 repositórios para evitar excesso de requisições
    if len(all_repos) >= 300:
        break

        # AQUI COMEÇA O BLOCO
        language_bytes = Counter()

        for repo in all_repos:

            if not isinstance(repo, dict):
                continue

            if (
                repo.get("fork")
                or repo.get("archived")
                or repo.get("is_template")
                or repo.get("size", 0) == 0
            ):
                continue

            try:
                languages_response = requests.get(
                    repo["languages_url"],
                    headers=headers,
                    timeout=20,
                )

                languages_response.raise_for_status()

                languages = languages_response.json()

                for language, bytes_code in languages.items():
                    language_bytes[language] += bytes_code

            except Exception as error:
                print(f"Erro em {repo['name']}: {error}")

        if not language_bytes:
            return [
                ("Python", 1),
                ("TypeScript", 1),
                ("C#", 1),
                ("JavaScript", 1),
                ("HTML", 1),
                ("CSS", 1),
            ]

        return language_bytes.most_common(6)

    except Exception as error:
        print(f"Error fetching language stats: {error}")
        return [
            ("Python", 1),
            ("TypeScript", 1),
            ("C#", 1),
            ("JavaScript", 1),
            ("HTML", 1),
            ("CSS", 1),
        ]

def get_language_color(language: str) -> str:
    """Retorna a cor da linguagem ou uma cor padrão."""
    return LANGUAGE_COLORS.get(language, "#58A6FF")


def get_language_abbr(language: str) -> str:
    """Retorna a abreviação da linguagem."""
    return LANGUAGE_ABBR.get(language, language[:2].upper())


def calculate_bar_width(percentage: float, max_width: int = 1040) -> int:
    """Calcula largura da barra baseada na porcentagem."""
    return int((percentage / 100) * max_width)


def generate_languages_svg(languages: list[tuple[str, int]]) -> None:
    """Gera o SVG de linguagens com o design customizado."""
    
    total = sum(count for _, count in languages) or 1
    max_bar_width = 1040
    
    # Gerar linhas para cada linguagem
    language_rows = []
    y_positions = [100, 160, 220, 280, 340, 400]
    
    for index, (language, count) in enumerate(languages[:6]):
        if index >= len(y_positions):
            break
            
        y_pos = y_positions[index]
        percentage = (count / total) * 100
        color = get_language_color(language)
        abbr = get_language_abbr(language)
        bar_width = calculate_bar_width(percentage, max_bar_width)
        
        # Criar gradiente específico para a linguagem
        gradient_id = f"{language.lower()}Gradient"
        
        language_rows.append(f'''
  <!-- Language {index + 1}: {language} -->
  <g transform="translate(60, {y_pos})">
    <!-- Language Icon -->
    <g transform="translate(0, 0)">
      <rect width="40" height="40" rx="8" fill="{color}" opacity="0.2">
        <animate attributeName="opacity" values="0;0.2" dur="{1.5 + index * 0.3}s" fill="freeze" />
      </rect>
      <text x="20" y="26" text-anchor="middle" font-family="'Segoe UI', system-ui, sans-serif" font-size="16" font-weight="700" fill="{color}">
        <animate attributeName="opacity" values="0;1" dur="{1.8 + index * 0.3}s" fill="freeze" />
        {abbr}
      </text>
    </g>
    
    <!-- Language Name -->
    <text x="60" y="25" font-family="'Segoe UI', system-ui, sans-serif" font-size="16" font-weight="600" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="{1.5 + index * 0.3}s" fill="freeze" />
      {language}
    </text>
    
    <!-- Percentage -->
    <text x="1100" y="25" font-family="'Segoe UI', system-ui, sans-serif" font-size="16" font-weight="600" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="{2 + index * 0.3}s" fill="freeze" />
      {percentage:.1f}%
    </text>
    
    <!-- Background Bar -->
    <rect x="60" y="35" width="1040" height="12" rx="6" fill="#30363D" opacity="0.3">
      <animate attributeName="opacity" values="0;0.3" dur="{1.5 + index * 0.3}s" fill="freeze" />
    </rect>
    
    <!-- Progress Bar -->
    <rect x="60" y="35" width="0" height="12" rx="6" fill="{color}" filter="url(#glow)">
      <animate attributeName="width" values="0;{bar_width}" dur="2s" fill="freeze" begin="{0.5 + index * 0.3}s" />
    </rect>
    
    <!-- Shine Effect -->
    <rect x="60" y="35" width="1040" height="12" rx="6" fill="url(#shineGradient)" clip-path="url(#barClip)" opacity="0.5">
      <animate attributeName="x" values="-1040;1040" dur="{8 + index}s" repeatCount="indefinite" begin="{2 + index * 0.5}s" />
    </rect>
  </g>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 500" width="1200" height="500">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0D1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#161B22;stop-opacity:1" />
    </linearGradient>

    <!-- Shine Effect Gradient -->
    <linearGradient id="shineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0" />
      <stop offset="50%" style="stop-color:#FFFFFF;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#FFFFFF;stop-opacity:0" />
    </linearGradient>

    <!-- Glow Filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="coloredBlur" />
      <feMerge>
        <feMergeNode in="coloredBlur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Grid Pattern -->
    <pattern id="gridPattern" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#30363D" stroke-width="0.5" opacity="0.05" />
    </pattern>

    <!-- Clip Path for Shine Animation -->
    <clipPath id="barClip">
      <rect x="0" y="0" width="800" height="30" rx="4" />
    </clipPath>
  </defs>

  <!-- Main Background -->
  <rect width="1200" height="500" fill="url(#bgGradient)" />
  <rect width="1200" height="500" fill="url(#gridPattern)" opacity="0.5" />

  <!-- Title -->
  <text x="60" y="50" font-family="'Segoe UI', system-ui, sans-serif" font-size="24" font-weight="600" fill="#F0F6FC">
    <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze" />
    Top Languages
  </text>
  <line x1="60" y1="65" x2="200" y2="65" stroke="#58A6FF" stroke-width="2" opacity="0.5">
    <animate attributeName="opacity" values="0;0.5" dur="1.5s" fill="freeze" />
  </line>
{''.join(language_rows)}

  <!-- Decorative Elements -->
  <g opacity="0.1">
    <circle cx="1150" cy="50" r="2" fill="#58A6FF">
      <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite" />
    </circle>
    <circle cx="1170" cy="70" r="1.5" fill="#58A6FF">
      <animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite" />
    </circle>
    <circle cx="1130" cy="80" r="1" fill="#58A6FF">
      <animate attributeName="opacity" values="0;1;0" dur="5s" repeatCount="indefinite" />
    </circle>
  </g>

  <!-- Bottom Line -->
  <line x1="60" y1="470" x2="1140" y2="470" stroke="#30363D" stroke-width="1" opacity="0.3">
    <animate attributeName="opacity" values="0;0.3" dur="4s" fill="freeze" />
  </line>
</svg>'''

    os.makedirs("profile", exist_ok=True)
    with open("profile/languages.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated languages.svg")


if __name__ == "__main__":
    generate_languages_svg(fetch_language_stats())
