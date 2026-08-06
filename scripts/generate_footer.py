#!/usr/bin/env python3
"""
Gera o rodapé do perfil.
"""

import os

from profile_theme import build_footer_svg


def generate_footer_svg() -> None:
    svg_content = build_footer_svg(
        name="Felipe Braga",
        message="Obrigado pela visita. Este perfil é atualizado automaticamente.",
    )

    os.makedirs("profile", exist_ok=True)
    with open("profile/footer.svg", "w", encoding="utf-8") as file:
        file.write(svg_content)

    print("✓ Generated footer.svg")


if __name__ == "__main__":
    generate_footer_svg()
