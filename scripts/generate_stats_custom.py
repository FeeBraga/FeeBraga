#!/usr/bin/env python3
"""
Gera o card de estatísticas do GitHub usando a API com o design customizado.
"""

import os
import requests

USERNAME = "FeeBraga"


def fetch_github_stats() -> dict[str, int]:
    """Busca estatísticas do GitHub via API."""
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Authorization": f"token {token}" if token else None,
        "Accept": "application/vnd.github.v3+json",
    }
    headers = {key: value for key, value in headers.items() if value is not None}

    try:
        # Buscar dados do usuário
        user_response = requests.get(
            f"https://api.github.com/users/{USERNAME}",
            headers=headers,
            timeout=20,
        )
        user_response.raise_for_status()
        user_data = user_response.json()

        # Buscar repositórios
        repos_response = requests.get(
            f"https://api.github.com/users/{USERNAME}/repos?per_page=100",
            headers=headers,
            timeout=20,
        )
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        # Calcular estatísticas
        stars = sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict))
        forks = sum(repo.get("forks_count", 0) for repo in repos_data if isinstance(repo, dict))

        # Buscar contribuições (último ano)
        contributions_response = requests.get(
            f"https://api.github.com/users/{USERNAME}/events/public?per_page=100",
            headers=headers,
            timeout=20,
        )
        contributions_response.raise_for_status()
        events_data = contributions_response.json()
        
        # Contar commits e PRs
        commits = 0
        pull_requests = 0
        issues = 0
        
        for event in events_data:
            if isinstance(event, dict):
                event_type = event.get("type", "")
                if event_type == "PushEvent":
                    commits += len(event.get("payload", {}).get("commits", []))
                elif event_type == "PullRequestEvent":
                    pull_requests += 1
                elif event_type == "IssuesEvent":
                    issues += 1

        return {
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "stars": stars,
            "forks": forks,
            "commits": commits,
            "pull_requests": pull_requests,
            "issues": issues,
            "contributions": user_data.get("total_private_repos", 0) + user_data.get("public_repos", 0),  # Aproximação
        }
    except Exception as error:
        print(f"Error fetching GitHub stats: {error}")
        return {
            "public_repos": 0,
            "followers": 0,
            "stars": 0,
            "forks": 0,
            "commits": 0,
            "pull_requests": 0,
            "issues": 0,
            "contributions": 0,
        }


def format_number(value: int) -> str:
    """Formata número com separador de milhar."""
    return f"{value:,}".replace(",", ".")


def calculate_bar_width(value: int, max_value: int, max_width: int = 150) -> int:
    """Calcula largura da barra baseada no valor máximo."""
    if max_value == 0:
        return 0
    ratio = value / max_value
    return int(ratio * max_width)


def generate_stats_svg(stats: dict[str, int]) -> None:
    """Gera o SVG de estatísticas com o design customizado."""
    
    # Calcular valores máximos para as barras
    max_repos = max(stats["public_repos"], 50)
    max_stars = max(stats["stars"], 100)
    max_forks = max(stats["forks"], 50)
    max_followers = max(stats["followers"], 50)
    max_commits = max(stats["commits"], 500)
    max_prs = max(stats["pull_requests"], 50)
    max_issues = max(stats["issues"], 30)
    max_contributions = max(stats["contributions"], 1000)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="2100" height="700">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0D1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#161B22;stop-opacity:1" />
    </linearGradient>

    <!-- Card Gradient -->
    <linearGradient id="cardGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#161B22;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1C2128;stop-opacity:1" />
    </linearGradient>

    <!-- Bar Gradient -->
    <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#58A6FF;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#79C0FF;stop-opacity:1" />
    </linearGradient>

    <!-- Bar Glow Gradient -->
    <linearGradient id="barGlowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#58A6FF;stop-opacity:0" />
      <stop offset="50%" style="stop-color:#58A6FF;stop-opacity:0.5" />
      <stop offset="100%" style="stop-color:#58A6FF;stop-opacity:0" />
    </linearGradient>

    <!-- Icon Glow -->
    <radialGradient id="iconGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#58A6FF;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#58A6FF;stop-opacity:0" />
    </radialGradient>

    <!-- Glow Filter -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="coloredBlur" />
      <feMerge>
        <feMergeNode in="coloredBlur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Card Shadow Filter -->
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000000" flood-opacity="0.3" />
    </filter>

    <!-- Grid Pattern -->
    <pattern id="gridPattern" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#30363D" stroke-width="0.5" opacity="0.05" />
    </pattern>
  </defs>

  <!-- Main Background -->
  <rect width="1200" height="400" fill="url(#bgGradient)" />
  <rect width="1200" height="400" fill="url(#gridPattern)" opacity="0.5" />

  <!-- Title -->
  <text x="60" y="50" font-family="'Segoe UI', system-ui, sans-serif" font-size="24" font-weight="600" fill="#F0F6FC">
    <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze" />
    Statistics
  </text>
  <line x1="60" y1="65" x2="180" y2="65" stroke="#58A6FF" stroke-width="2" opacity="0.5">
    <animate attributeName="opacity" values="0;0.5" dur="1.5s" fill="freeze" />
  </line>

  <!-- Card 1: Total Repositories -->
  <g transform="translate(60, 100)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="1.5s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <path d="M 15 0 L 15 30 L 0 30 L 0 0 Z" fill="none" stroke="#58A6FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="opacity" values="0;1" dur="1.5s" fill="freeze" />
      </path>
      <path d="M 5 8 L 10 8" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="1.8s" fill="freeze" />
      </path>
      <path d="M 5 15 L 10 15" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2s" fill="freeze" />
      </path>
      <path d="M 5 22 L 10 22" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.2s" fill="freeze" />
      </path>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="2s" fill="freeze" />
      Repositories
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="2.5s" fill="freeze" />
      {format_number(stats["public_repos"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["public_repos"], max_repos, 120)}" dur="2s" fill="freeze" begin="1s" />
    </rect>
  </g>

  <!-- Card 2: Total Stars -->
  <g transform="translate(340, 100)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="1.2s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="1.7s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <polygon points="15,2 18,12 29,12 20,19 23,29 15,23 7,29 10,19 1,12 12,12" fill="none" stroke="#58A6FF" stroke-width="2" stroke-linejoin="round">
        <animate attributeName="opacity" values="0;1" dur="1.7s" fill="freeze" />
      </polygon>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="2.2s" fill="freeze" />
      Total Stars
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="2.7s" fill="freeze" />
      {format_number(stats["stars"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["stars"], max_stars, 100)}" dur="2s" fill="freeze" begin="1.2s" />
    </rect>
  </g>

  <!-- Card 3: Total Forks -->
  <g transform="translate(620, 100)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="1.4s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="1.9s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <path d="M 15 2 L 15 10" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="1.9s" fill="freeze" />
      </path>
      <path d="M 15 10 L 15 18" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2s" fill="freeze" />
      </path>
      <path d="M 15 18 L 8 25" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.1s" fill="freeze" />
      </path>
      <path d="M 15 18 L 22 25" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.2s" fill="freeze" />
      </path>
      <circle cx="8" cy="27" r="2" fill="#58A6FF">
        <animate attributeName="opacity" values="0;1" dur="2.3s" fill="freeze" />
      </circle>
      <circle cx="22" cy="27" r="2" fill="#58A6FF">
        <animate attributeName="opacity" values="0;1" dur="2.4s" fill="freeze" />
      </circle>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="2.4s" fill="freeze" />
      Total Forks
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="2.9s" fill="freeze" />
      {format_number(stats["forks"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["forks"], max_forks, 80)}" dur="2s" fill="freeze" begin="1.4s" />
    </rect>
  </g>

  <!-- Card 4: Followers -->
  <g transform="translate(900, 100)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="1.6s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="2.1s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <circle cx="15" cy="10" r="6" fill="none" stroke="#58A6FF" stroke-width="2">
        <animate attributeName="opacity" values="0;1" dur="2.1s" fill="freeze" />
      </circle>
      <path d="M 5 28 Q 15 18 25 28" fill="none" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.2s" fill="freeze" />
      </path>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="2.6s" fill="freeze" />
      Followers
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="3.1s" fill="freeze" />
      {format_number(stats["followers"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["followers"], max_followers, 90)}" dur="2s" fill="freeze" begin="1.6s" />
    </rect>
  </g>

  <!-- Card 5: Commits -->
  <g transform="translate(60, 250)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="1.8s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="2.3s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <circle cx="8" cy="15" r="3" fill="none" stroke="#58A6FF" stroke-width="2">
        <animate attributeName="opacity" values="0;1" dur="2.3s" fill="freeze" />
      </circle>
      <circle cx="22" cy="15" r="3" fill="none" stroke="#58A6FF" stroke-width="2">
        <animate attributeName="opacity" values="0;1" dur="2.4s" fill="freeze" />
      </circle>
      <line x1="11" y1="15" x2="19" y2="15" stroke="#58A6FF" stroke-width="2">
        <animate attributeName="opacity" values="0;1" dur="2.5s" fill="freeze" />
      </line>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="2.8s" fill="freeze" />
      Commits
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="3.3s" fill="freeze" />
      {format_number(stats["commits"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["commits"], max_commits, 140)}" dur="2s" fill="freeze" begin="1.8s" />
    </rect>
  </g>

  <!-- Card 6: Pull Requests -->
  <g transform="translate(340, 250)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="2s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="2.5s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <path d="M 5 15 L 10 10 L 15 15" fill="none" stroke="#58A6FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="opacity" values="0;1" dur="2.5s" fill="freeze" />
      </path>
      <path d="M 10 10 L 10 25" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.6s" fill="freeze" />
      </path>
      <path d="M 25 15 L 20 10 L 15 15" fill="none" stroke="#58A6FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="opacity" values="0;1" dur="2.7s" fill="freeze" />
      </path>
      <path d="M 20 10 L 20 25" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.8s" fill="freeze" />
      </path>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="3s" fill="freeze" />
      Pull Requests
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="3.5s" fill="freeze" />
      {format_number(stats["pull_requests"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["pull_requests"], max_prs, 110)}" dur="2s" fill="freeze" begin="2s" />
    </rect>
  </g>

  <!-- Card 7: Issues -->
  <g transform="translate(620, 250)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="2.2s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="2.7s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <circle cx="15" cy="15" r="10" fill="none" stroke="#58A6FF" stroke-width="2">
        <animate attributeName="opacity" values="0;1" dur="2.7s" fill="freeze" />
      </circle>
      <circle cx="15" cy="10" r="1.5" fill="#58A6FF">
        <animate attributeName="opacity" values="0;1" dur="2.8s" fill="freeze" />
      </circle>
      <line x1="15" y1="14" x2="15" y2="20" stroke="#58A6FF" stroke-width="2" stroke-linecap="round">
        <animate attributeName="opacity" values="0;1" dur="2.9s" fill="freeze" />
      </line>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="3.2s" fill="freeze" />
      Issues
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="3.7s" fill="freeze" />
      {format_number(stats["issues"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["issues"], max_issues, 70)}" dur="2s" fill="freeze" begin="2.2s" />
    </rect>
  </g>

  <!-- Card 8: Contributions -->
  <g transform="translate(900, 250)">
    <rect width="250" height="120" rx="12" fill="url(#cardGradient)" stroke="#30363D" stroke-width="1" filter="url(#cardShadow)">
      <animate attributeName="opacity" values="0;1" dur="2.4s" fill="freeze" />
    </rect>
    <circle cx="45" cy="45" r="25" fill="url(#iconGlow)" opacity="0.5">
      <animate attributeName="opacity" values="0;0.5" dur="2.9s" fill="freeze" />
    </circle>
    <g transform="translate(30, 30)">
      <rect x="2" y="18" width="4" height="10" rx="1" fill="#58A6FF" opacity="0.4">
        <animate attributeName="opacity" values="0;1" dur="2.9s" fill="freeze" />
      </rect>
      <rect x="8" y="12" width="4" height="16" rx="1" fill="#58A6FF" opacity="0.6">
        <animate attributeName="opacity" values="0;1" dur="3s" fill="freeze" />
      </rect>
      <rect x="14" y="8" width="4" height="20" rx="1" fill="#58A6FF" opacity="0.8">
        <animate attributeName="opacity" values="0;1" dur="3.1s" fill="freeze" />
      </rect>
      <rect x="20" y="14" width="4" height="14" rx="1" fill="#58A6FF" opacity="0.5">
        <animate attributeName="opacity" values="0;1" dur="3.2s" fill="freeze" />
      </rect>
    </g>
    <text x="85" y="40" font-family="'Segoe UI', system-ui, sans-serif" font-size="14" fill="#8B949E">
      <animate attributeName="opacity" values="0;1" dur="3.4s" fill="freeze" />
      Contributions
    </text>
    <text x="85" y="75" font-family="'Segoe UI', system-ui, sans-serif" font-size="32" font-weight="700" fill="#F0F6FC">
      <animate attributeName="opacity" values="0;1" dur="3.9s" fill="freeze" />
      {format_number(stats["contributions"])}
    </text>
    <rect x="85" y="90" width="0" height="4" rx="2" fill="url(#barGradient)">
      <animate attributeName="width" values="0;{calculate_bar_width(stats["contributions"], max_contributions, 150)}" dur="2s" fill="freeze" begin="2.4s" />
    </rect>
  </g>

  <!-- Decorative Technical Lines -->
  <g opacity="0.2">
    <line x1="60" y1="390" x2="1140" y2="390" stroke="#58A6FF" stroke-width="1" stroke-dasharray="5,5">
      <animate attributeName="opacity" values="0;0.2" dur="4s" fill="freeze" />
    </line>
    <circle cx="60" cy="390" r="3" fill="#58A6FF">
      <animate attributeName="opacity" values="0;1" dur="4.5s" fill="freeze" />
    </circle>
    <circle cx="1140" cy="390" r="3" fill="#58A6FF">
      <animate attributeName="opacity" values="0;1" dur="4.5s" fill="freeze" />
    </circle>
  </g>
 <g transform="translate(1098 248)" shape-rendering="crispEdges" opacity="0.64">
    <g transform="translate(0 14)">
      <animateTransform attributeName="transform" type="rotate" values="0 4 6;10 4 6;0 4 6;-6 4 6;0 4 6" dur="7s" repeatCount="indefinite" />
      <rect x="0" y="8" width="4" height="4" fill="#30363D" />
      <rect x="4" y="4" width="4" height="4" fill="#30363D" />
      <rect x="8" y="0" width="4" height="4" fill="#30363D" />
      <rect x="8" y="4" width="4" height="4" fill="#30363D" />
      <rect x="8" y="8" width="4" height="4" fill="#30363D" />
    </g>
    <g>
      <rect x="12" y="0" width="4" height="4" fill="#30363D" />
      <rect x="24" y="0" width="4" height="4" fill="#30363D" />
      <rect x="8" y="4" width="4" height="4" fill="#30363D" />
      <rect x="12" y="4" width="4" height="4" fill="#30363D" />
      <rect x="16" y="4" width="4" height="4" fill="#30363D" />
      <rect x="20" y="4" width="4" height="4" fill="#30363D" />
      <rect x="24" y="4" width="4" height="4" fill="#30363D" />
      <rect x="28" y="4" width="4" height="4" fill="#30363D" />
      <rect x="8" y="8" width="4" height="4" fill="#30363D" />
      <rect x="12" y="8" width="4" height="4" fill="#30363D" />
      <rect x="16" y="8" width="4" height="4" fill="#30363D" />
      <rect x="20" y="8" width="4" height="4" fill="#30363D" />
      <rect x="24" y="8" width="4" height="4" fill="#30363D" />
      <rect x="28" y="8" width="4" height="4" fill="#30363D" />
      <rect x="8" y="12" width="4" height="4" fill="#30363D" />
      <rect x="12" y="12" width="4" height="4" fill="#30363D" />
      <rect x="16" y="12" width="4" height="4" fill="#30363D" />
      <rect x="20" y="12" width="4" height="4" fill="#30363D" />
      <rect x="24" y="12" width="4" height="4" fill="#30363D" />
      <rect x="28" y="12" width="4" height="4" fill="#30363D" />
      <rect x="12" y="16" width="4" height="4" fill="#30363D" />
      <rect x="16" y="16" width="4" height="4" fill="#30363D" />
      <rect x="20" y="16" width="4" height="4" fill="#30363D" />
      <rect x="24" y="16" width="4" height="4" fill="#30363D" />
      <rect x="12" y="20" width="4" height="4" fill="#30363D" />
      <rect x="16" y="20" width="4" height="4" fill="#30363D" />
      <rect x="20" y="20" width="4" height="4" fill="#30363D" />
      <rect x="24" y="20" width="4" height="4" fill="#30363D" />
      <rect x="12" y="24" width="4" height="4" fill="#30363D" />
      <rect x="24" y="24" width="4" height="4" fill="#30363D" />
      <rect x="12" y="28" width="4" height="4" fill="#30363D" />
      <rect x="24" y="28" width="4" height="4" fill="#30363D" />
    </g>
    <g fill="#F0F6FC">
      <rect x="16" y="12" width="4" height="4">
        <animate attributeName="opacity" values="1;1;1;0;1;1" dur="6.5s" repeatCount="indefinite" />
      </rect>
      <rect x="24" y="12" width="4" height="4">
        <animate attributeName="opacity" values="1;1;1;0;1;1" dur="6.5s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
  
</svg>'''

    os.makedirs("profile", exist_ok=True)
    with open("profile/stats.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated stats.svg")


if __name__ == "__main__":
    generate_stats_svg(fetch_github_stats())
