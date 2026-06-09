"""
header.py – En-tête hero affiché en haut de chaque page.
"""

from dash import html


def create_header(title: str, subtitle: str = "") -> html.Div:
    """
    Construit un bloc hero avec titre et sous-titre.

    Args:
        title:    Titre principal de la page.
        subtitle: Sous-titre descriptif (optionnel).

    Returns:
        Composant Dash représentant le header.
    """
    children = [
        html.H1(title, className="hero-title"),
    ]
    if subtitle:
        children.append(html.P(subtitle, className="hero-subtitle"))

    return html.Div(className="hero-section", children=children)
