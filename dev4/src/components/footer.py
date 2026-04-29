"""
footer.py – Pied de page du dashboard.
"""

from dash import html


def create_footer() -> html.Div:
    """Construit le pied de page."""
    return html.Div(
        style={
            "textAlign": "center",
            "padding": "1.5rem",
            "color": "#64748B",
            "fontSize": "0.8rem",
            "borderTop": "1px solid #1E3A5F",
            "marginTop": "2rem",
        },
        children=[
            html.Span("Projet E4-DSIA – Python 2 – ESIEE Paris · "),
            html.Span("Données : NASA Meteorite Landings Open Data"),
        ],
    )
