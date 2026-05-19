"""
main.py – Point d'entrée du dashboard Météorites.

Lance l'application Dash avec le routing multi-pages.
Usage :
    $ python main.py
"""

import sys
import os

# Permet les imports absolus depuis la racine du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import html, dcc, Input, Output

import config
from src.utils.clean_data import run_pipeline
from src.components.navbar import create_navbar
from src.pages import home, map_page, analysis


# ── Initialisation des données ─────────────────────────────────────────────
if not os.path.exists(config.DB_FILE):
    print("Première exécution : nettoyage des données en cours...")
    run_pipeline()


# ── Application Dash ──────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,  # nécessaire pour le routing multi-pages
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = config.APP_TITLE

# ── Layout principal ───────────────────────────────────────────────────────
app.layout = html.Div(
    style={"backgroundColor": config.COLORS["bg_dark"], "minHeight": "100vh"},
    children=[
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        html.Div(id="page-content"),
    ],
)


# ── Routing ────────────────────────────────────────────────────────────────

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname: str) -> html.Div:
    """
    Retourne le contenu de la page correspondant à l'URL.

    Args:
        pathname: Chemin URL courant (ex. '/', '/carte', '/analyses').

    Returns:
        Layout Dash de la page demandée.
    """
    if pathname in ("/", ""):
        return home.layout()
    if pathname == "/carte":
        return map_page.layout()
    if pathname == "/analyses":
        return analysis.layout()

    # Page 404
    return html.Div(
        style={"textAlign": "center", "padding": "4rem", "color": config.COLORS["text_muted"]},
        children=[
            html.H2("404 – Page introuvable", style={"color": config.COLORS["text"]}),
            html.P(f"La page « {pathname} » n'existe pas."),
            dcc.Link("← Retour à l'accueil", href="/", style={"color": config.COLORS["primary_lt"]}),
        ],
    )


# ── Lancement ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\nDashboard Météorites démarré sur http://{config.APP_HOST}:{config.APP_PORT}\n")
    app.run(
        host=config.APP_HOST,
        port=config.APP_PORT,
        debug=config.DEBUG,
    )
