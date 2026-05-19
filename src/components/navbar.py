"""
navbar.py – Barre de navigation principale du dashboard.
"""

from dash import html, dcc


def create_navbar() -> html.Div:
    """
    Construit la barre de navigation avec les liens vers les 3 pages.

    Returns:
        Composant Dash représentant la navbar.
    """
    return html.Div(
        className="navbar-custom",
        children=[
            # Logo / titre
            dcc.Link(
                "MÉTÉORITES",
                href="/",
                className="navbar-brand-text",
                style={"marginRight": "2rem"},
            ),
            # Liens de navigation
            html.Div(
                style={"display": "flex", "gap": "0.5rem"},
                children=[
                    dcc.Link("Accueil",      href="/",         className="nav-link-custom", id="nav-home"),
                    dcc.Link("Carte mondiale", href="/carte",    className="nav-link-custom", id="nav-map"),
                    dcc.Link("Analyses",       href="/analyses", className="nav-link-custom", id="nav-analysis"),
                ],
            ),
        ],
    )
