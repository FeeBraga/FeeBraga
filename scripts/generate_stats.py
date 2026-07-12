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
        ("REPO", "Repositories", stats["public_repos"]),
        ("SOCIAL", "Followers", stats["followers"]),
        ("NETWORK", "Following", stats["following"]),
        ("STARS", "Stars", stats["stars"]),
        ("FORKS", "Forks", stats["forks"]),
    ]
    max_value = max((value for _, _, value in metrics), default=1) or 1

    rows = [
        {
            "pill": pill,
            "label": label,
            "value": format_number(value),
            "ratio": value / max_value,
        }
        for pill, label, value in metrics
    ]

    svg_content = build_card_svg(
        title="GitHub Stats",
        rows=rows,
        description="Card com estatísticas principais do GitHub em layout minimalista.",
    )

    os.makedirs("profile", exist_ok=True)
    with open("profile/stats.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated stats.svg")


if __name__ == "__main__":
    generate_stats_svg(fetch_github_stats())
