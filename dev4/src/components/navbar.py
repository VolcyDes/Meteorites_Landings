"""
navbar.py – Barre de navigation principale du dashboard.
"""

from dash import html, dcc


def create_navbar() -> html.Div:
    """Construit la barre de navigation avec les liens vers les 3 pages."""
    return html.Div(
        style={
            "backgroundColor": "#1a1a2e",
            "padding": "0 2rem",
            "height": "60px",
            "display": "flex",
            "alignItems": "center",
            "borderBottom": "1px solid #333",
        },
        children=[
            dcc.Link(
                "🌠 MÉTÉORITES",
                href="/",
                style={"color": "#f0a500", "fontWeight": "700",
                       "fontSize": "1.1rem", "marginRight": "2rem",
                       "textDecoration": "none"},
            ),
            dcc.Link("🏠 Accueil", href="/",
                     style={"color": "#aaa", "marginRight": "1rem", "textDecoration": "none"}),
            dcc.Link("🗺️ Carte mondiale", href="/carte",
                     style={"color": "#aaa", "marginRight": "1rem", "textDecoration": "none"}),
            dcc.Link("📊 Analyses", href="/analyses",
                     style={"color": "#aaa", "textDecoration": "none"}),
        ],
    )
