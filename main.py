"""
main.py – Point d'entrée du dashboard Météorites (version initiale).

Usage :
    $ python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import html, dcc

import config

app = dash.Dash(__name__)
app.title = config.APP_TITLE

app.layout = html.Div(
    style={"fontFamily": "sans-serif", "padding": "2rem"},
    children=[
        html.H1("🌠 Chutes de Météorites – Analyse Mondiale"),
        html.P("Dashboard en cours de construction..."),
    ],
)

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
