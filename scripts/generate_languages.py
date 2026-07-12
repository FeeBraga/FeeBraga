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
    rows = [
        {
            "pill": PILL_MAP.get(language, safe_pill(language)),
            "label": language,
            "value": f"{(count / total) * 100:.1f}%",
            "ratio": count / total,
        }
        for language, count in languages[:5]
    ]

    svg_content = build_card_svg(
        title="Top Languages",
        rows=rows,
        description="Card com as linguagens mais utilizadas no GitHub em layout minimalista.",
    )

    os.makedirs("profile", exist_ok=True)
    with open("profile/languages.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated languages.svg")


if __name__ == "__main__":
    generate_languages_svg(fetch_language_stats())
