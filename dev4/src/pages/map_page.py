"""
map_page.py – Page Carte mondiale du dashboard (version initiale).
"""

import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_data


def layout() -> html.Div:
    """Construit le layout de la page carte."""
    df = load_data()
    df_geo = df.dropna(subset=["latitude", "longitude"])
    year_min = int(df_geo["annee"].min(skipna=True))
    year_max = int(df_geo["annee"].max(skipna=True))

    return html.Div([
        create_header(
            "🗺️ Carte Mondiale des Météorites",
            f"Répartition géographique — {len(df_geo):,} météorites géolocalisées.".replace(",", "\u202f"),
        ),
        html.Div(
            style={"padding": "1.5rem 2rem"},
            children=[
                # Filtres
                html.Div(
                    style={"background": "#0B1629", "border": "1px solid #333",
                           "borderRadius": "8px", "padding": "1rem", "marginBottom": "1rem"},
                    children=[
                        html.H4("Filtres", style={"color": "#E2E8F0", "marginTop": 0}),
                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "1.5rem"},
                            children=[
                                html.Div([
                                    html.Label("Plage d'années",
                                               style={"color": "#94A3B8", "fontSize": "0.85rem"}),
                                    dcc.RangeSlider(
                                        id="map-year-slider",
                                        min=year_min, max=year_max,
                                        value=[1800, year_max],
                                        marks={y: str(y) for y in range(1800, year_max + 1, 50)},
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        step=1,
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Statut",
                                               style={"color": "#94A3B8", "fontSize": "0.85rem"}),
                                    dcc.Dropdown(
                                        id="map-statut-filter",
                                        options=[
                                            {"label": "Tous",     "value": "all"},
                                            {"label": "Found",    "value": "Found"},
                                            {"label": "Fell",     "value": "Fell"},
                                        ],
                                        value="all", clearable=False,
                                    ),
                                ]),
                            ],
                        ),
                        html.Div(id="map-count-label",
                                 style={"color": "#94A3B8", "fontSize": "0.82rem", "marginTop": "0.5rem"}),
                    ],
                ),
                # Carte
                html.Div(
                    style={"background": "#0B1629", "border": "1px solid #333",
                           "borderRadius": "8px", "padding": "0.5rem"},
                    children=[
                        dcc.Graph(id="world-map", style={"height": "550px"}),
                    ],
                ),
            ],
        ),
        create_footer(),
    ])


@callback(
    Output("world-map", "figure"),
    Output("map-count-label", "children"),
    Input("map-year-slider", "value"),
    Input("map-statut-filter", "value"),
)
def update_map(year_range: list, statut: str) -> tuple:
    df = load_data()
    df_geo = df.dropna(subset=["latitude", "longitude"])

    mask = (df_geo["annee"] >= year_range[0]) & (df_geo["annee"] <= year_range[1])
    if statut != "all":
        mask &= df_geo["statut"] == statut
    df_filtered = df_geo[mask]

    fig = px.scatter_geo(
        df_filtered,
        lat="latitude", lon="longitude",
        hover_name="nom",
        color="masse_kg",
        size_max=8,
        color_continuous_scale=["#0B1629", "#0EA5E9", "#F59E0B"],
        projection="natural earth",
    )
    fig.update_layout(
        paper_bgcolor="#0B1629", plot_bgcolor="#0B1629",
        font_color="#E2E8F0",
        geo=dict(bgcolor="#020817", landcolor="#0F2040",
                 showocean=True, oceancolor="#020817",
                 showcountries=True, countrycolor="#1E3A5F"),
        margin=dict(t=0, b=0, l=0, r=0),
    )
    count = len(df_filtered)
    label = f"{count:,} météorite(s) affichée(s)".replace(",", "\u202f")
    return fig, label
