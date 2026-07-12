#!/usr/bin/env python3
"""
Gera o cabeçalho principal do perfil.
"""

import os

from profile_theme import build_header_svg


def generate_header_svg() -> None:
    svg_content = build_header_svg(
        name="Felipe Braga",
        role="Desenvolvedor Full Stack",
        tagline="Interfaces limpas, APIs robustas e foco em produto.",
        chips=["Python & .NET", "React & TypeScript", "Arquitetura e UX"],
    )

    os.makedirs("profile", exist_ok=True)
    with open("profile/header.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated header.svg")


if __name__ == "__main__":
    generate_header_svg()
