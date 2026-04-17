"""
main.py – Point d'entrée du dashboard Météorites.

Usage :
    $ python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import html, dcc

import config
from src.utils.clean_data import run_pipeline

# Pipeline de données au premier lancement
if not os.path.exists(config.DB_FILE):
    print("Première exécution : nettoyage des données...")
    run_pipeline()

app = dash.Dash(__name__)
app.title = config.APP_TITLE

app.layout = html.Div(
    style={"fontFamily": "sans-serif", "padding": "2rem"},
    children=[
        html.H1(" Chutes de Météorites – Analyse Mondiale"),
        html.P("Pipeline de données opérationnel. Pages en cours de construction..."),
    ],
)

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
