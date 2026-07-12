#!/usr/bin/env python3
"""
Gera o card de linguagens principais usando a API do GitHub.
"""

import os
from collections import Counter

import requests

from profile_theme import build_card_svg, safe_pill

USERNAME = "FeeBraga"

PILL_MAP = {
    "Python": "PY",
    "JavaScript": "JS",
    "TypeScript": "TS",
    "C#": "C#",
    ".NET": "NET",
    "C++": "C++",
    "HTML": "HTML",
    "CSS": "CSS",
    "Go": "GO",
    "Rust": "RUST",
    "Java": "JAVA",
}

# Linguagens que normalmente não fazem sentido exibir
IGNORE_LANGUAGES = {
    "Dockerfile",
    "Batchfile",
    "ShaderLab",
    "GLSL",
}


def fetch_language_stats():
    """Busca estatísticas reais das linguagens usando a API /languages."""

    try:
        token = os.environ.get("GITHUB_TOKEN")

        headers = {
            "Accept": "application/vnd.github+json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        language_bytes = Counter()

        page = 1
        repo_count = 0

        while True:
            repos_response = requests.get(
                f"https://api.github.com/users/{USERNAME}/repos",
                headers=headers,
                params={
                    "per_page": 100,
                    "page": page,
                    "sort": "size",
                },
                timeout=30,
            )

            repos_response.raise_for_status()

            repos = repos_response.json()

            if not repos:
                break

            for repo in repos:

                # Ignorar repositórios que não representam código do usuário
                if (
                    repo["fork"]
                    or repo["archived"]
                    or repo["is_template"]
                    or repo["size"] == 0
                ):
                    continue

                try:
                    languages_response = requests.get(
                        repo["languages_url"],
                        headers=headers,
                        timeout=30,
                    )

                    languages_response.raise_for_status()

                    languages = languages_response.json()

                    for language, bytes_code in languages.items():

                        if language in IGNORE_LANGUAGES:
                            continue

                        language_bytes[language] += bytes_code

                except Exception as error:
                    print(f"Erro em {repo['name']}: {error}")

                repo_count += 1

                # Limita a 300 repositórios
                if repo_count >= 300:
                    break

            page += 1

            # Limita a 300 repositórios
            if repo_count >= 300:
                break

        if not language_bytes:
            return [
                ("C#", 1),
                ("TypeScript", 1),
                ("Python", 1),
                ("HTML", 1),
                ("CSS", 1),
                ("JavaScript", 1),
            ]

        return language_bytes.most_common(6)

    except Exception as error:
        print(f"Error fetching language stats: {error}")
        return [
            ("C#", 1),
            ("TypeScript", 1),
            ("Python", 1),
            ("HTML", 1),
            ("CSS", 1),
            ("JavaScript", 1),
        ]


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
