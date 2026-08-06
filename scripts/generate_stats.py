#!/usr/bin/env python3
"""
Gera o card de estatísticas do GitHub usando a API.
"""

import os

import requests

from profile_theme import build_card_svg, format_number


def fetch_github_stats() -> dict[str, int]:
    username = "FeeBraga"
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }
    headers = {key: value for key, value in headers.items() if value is not None}

    try:
        user_response = requests.get(
            f"https://api.github.com/users/{username}",
            headers=headers,
            timeout=20,
        )
        user_response.raise_for_status()
        user_data = user_response.json()

        repos_response = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100",
            headers=headers,
            timeout=20,
        )
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        return {
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "stars": sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict)),
            "forks": sum(repo.get("forks_count", 0) for repo in repos_data if isinstance(repo, dict)),
        }
    except Exception as error:
        print(f"Error fetching GitHub stats: {error}")
        return {
            "public_repos": 0,
            "followers": 0,
            "following": 0,
            "stars": 0,
            "forks": 0,
        }


def generate_stats_svg(stats: dict[str, int]) -> None:
    metrics = [
        ("Repositories", stats["public_repos"], "#00FF94"),
        ("Followers", stats["followers"], "#FF00FF"),
        ("Following", stats["following"], "#00FFFF"),
        ("Stars", stats["stars"], "#FFD43B"),
        ("Forks", stats["forks"], "#FF6B6B"),
    ]

    # Gerar SVG compacto cyberpunk
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 140" width="400" height="140">
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
  
  <text x="200" y="28" font-family="Arial" font-size="16" fill="#00FF94" text-anchor="middle" font-weight="bold" letter-spacing="1">GITHUB STATS</text>
  <line x1="50" y1="38" x2="350" y2="38" stroke="#00FF94" stroke-width="1" opacity="0.5" />
"""

    y = 55
    for label, value, color in metrics:
        svg_content += f"""
  <rect x="30" y="{y - 12}" width="340" height="24" rx="6" fill="#161B22" stroke="#21262D" stroke-width="1" />
  <text x="45" y="{y + 4}" font-family="Arial" font-size="12" fill="#8B949E">{label}</text>
  <text x="355" y="{y + 4}" font-family="Arial" font-size="12" fill="{color}" text-anchor="end" font-weight="bold">{format_number(value)}</text>
"""
        y += 20

    svg_content += """
  <line x1="50" y1="130" x2="350" y2="130" stroke="#FF00FF" stroke-width="1" opacity="0.3" />
</svg>"""

    os.makedirs("profile", exist_ok=True)
    with open("profile/stats.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("Generated stats.svg")


if __name__ == "__main__":
    generate_stats_svg(fetch_github_stats())
