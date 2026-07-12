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


from collections import Counter
import os
import requests

USERNAME = "FeeBraga"


def fetch_language_stats():
    token = os.environ.get("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    language_bytes = Counter()

    page = 1

    while True:
        repos = requests.get(
            f"https://api.github.com/users/{USERNAME}/repos",
            headers=headers,
            params={
                "per_page": 100,
                "page": page,
                "sort": "updated"
            },
            timeout=30,
        )

        repos.raise_for_status()

        repos = repos.json()

        if not repos:
            break

        for repo in repos:

            # ignora forks
            if repo["fork"]:
                continue

            languages = requests.get(
                repo["languages_url"],
                headers=headers,
                timeout=30,
            )

            languages.raise_for_status()

            for lang, bytes_code in languages.json().items():
                language_bytes[lang] += bytes_code

        page += 1

    if not language_bytes:
        return [
            ("C#",1),
            ("TypeScript",1),
            ("Python",1),
            ("HTML",1),
            ("CSS",1),
            ("JavaScript",1),
        ]

    return language_bytes.most_common(6)


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
