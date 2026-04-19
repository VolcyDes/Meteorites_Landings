"""
main.py – Point d'entrée du dashboard Météorites (avec routing multi-pages).

Usage :
    $ python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import html, dcc, Input, Output

import config
from src.utils.clean_data import run_pipeline
from src.components.navbar import create_navbar
from src.pages import home

if not os.path.exists(config.DB_FILE):
    print("Première exécution : nettoyage des données...")
    run_pipeline()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = config.APP_TITLE

app.layout = html.Div(
    style={"backgroundColor": "#0f0f1a", "minHeight": "100vh"},
    children=[
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        html.Div(id="page-content"),
    ],
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname: str) -> html.Div:
    if pathname in ("/", ""):
        return home.layout()
    return html.Div(
        style={"padding": "2rem", "color": "#94A3B8"},
        children=[html.H3("Page en construction..."),
                  dcc.Link("← Retour à l'accueil", href="/")],
    )


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
