"""
header.py – Composant en-tête de page.
"""

from dash import html


def create_header(title: str, subtitle: str = "") -> html.Div:
    """Construit l'en-tête d'une page avec titre et sous-titre."""
    return html.Div(
        style={
            "padding": "2rem 2rem 1rem",
            "borderBottom": "1px solid #333",
        },
        children=[
            html.H2(title, style={"color": "#E2E8F0", "margin": 0}),
            html.P(subtitle, style={"color": "#94A3B8", "marginTop": "0.4rem"})
            if subtitle else None,
        ],
    )
