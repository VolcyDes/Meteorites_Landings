"""
footer.py – Pied de page du dashboard.
"""

from dash import html


def create_footer() -> html.Div:
    """
    Construit le pied de page avec la source des données et les auteurs.

    Returns:
        Composant Dash représentant le footer.
    """
    return html.Div(
        className="footer-custom",
        children=[
            html.Span("Source des données : "),
            html.A(
                "NASA Open Data Portal – The Meteoritical Society",
                href="https://data.nasa.gov/dataset/meteorite-landings",
                target="_blank",
                style={"color": "#2563EB"},
            ),
            html.Span(" | Projet E4-FD Python 2 – ESIEE Paris"),
        ],
    )
