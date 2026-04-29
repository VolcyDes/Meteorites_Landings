"""
analysis.py – Page Analyses statistiques du dashboard (version initiale).
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_data, discoveries_by_year

_by_year = discoveries_by_year()
_YEAR_MIN = int(_by_year["annee"].min())
_YEAR_MAX = int(_by_year["annee"].max())


def layout() -> html.Div:
    """Construit le layout de la page d'analyses statistiques."""
    df = load_data()

    # Répartition par catégorie de masse
    grp = (
        df.groupby(["categorie_masse", "statut"], observed=True)
        .size()
        .reset_index(name="nombre")
    )
    fig_cat = px.bar(
        grp, x="categorie_masse", y="nombre", color="statut",
        barmode="group",
        color_discrete_map={"Found": "#0EA5E9", "Fell": "#F59E0B"},
    )
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0",
        margin=dict(t=20, b=40, l=60, r=20),
    )

    return html.Div([
        create_header(
            "📊 Analyses Statistiques",
            "Distribution des masses, évolution temporelle et répartition par catégorie.",
        ),
        html.Div(
            style={"padding": "1.5rem 2rem"},
            children=[
                # Histogramme
                html.Div(
                    style={"background": "#0B1629", "border": "1px solid #333",
                           "borderRadius": "8px", "padding": "1rem", "marginBottom": "1rem"},
                    children=[
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between",
                                   "alignItems": "center"},
                            children=[
                                html.H4("Distribution des masses (log₁₀)",
                                        style={"color": "#E2E8F0", "margin": 0}),
                                dcc.Dropdown(
                                    id="hist-statut-filter",
                                    options=[
                                        {"label": "Tous",    "value": "all"},
                                        {"label": "Found",   "value": "Found"},
                                        {"label": "Fell",    "value": "Fell"},
                                    ],
                                    value="all", clearable=False,
                                    style={"width": "180px"},
                                ),
                            ],
                        ),
                        dcc.Graph(id="hist-masse", config={"displayModeBar": False},
                                  style={"height": "300px"}),
                    ],
                ),
                # Série temporelle
                html.Div(
                    style={"background": "#0B1629", "border": "1px solid #333",
                           "borderRadius": "8px", "padding": "1rem", "marginBottom": "1rem"},
                    children=[
                        html.H4("Évolution des découvertes par année",
                                style={"color": "#E2E8F0", "marginTop": 0}),
                        dcc.RangeSlider(
                            id="time-year-slider",
                            min=1800, max=_YEAR_MAX,
                            value=[1900, _YEAR_MAX],
                            marks={y: str(y) for y in range(1900, _YEAR_MAX + 1, 20)},
                            step=1,
                        ),
                        dcc.Graph(id="time-series", config={"displayModeBar": False},
                                  style={"height": "280px"}),
                    ],
                ),
                # Catégories de masse (statique)
                html.Div(
                    style={"background": "#0B1629", "border": "1px solid #333",
                           "borderRadius": "8px", "padding": "1rem"},
                    children=[
                        html.H4("Répartition par catégorie de masse",
                                style={"color": "#E2E8F0", "marginTop": 0}),
                        dcc.Graph(figure=fig_cat, config={"displayModeBar": False},
                                  style={"height": "300px"}),
                    ],
                ),
            ],
        ),
        create_footer(),
    ])


@callback(Output("hist-masse", "figure"), Input("hist-statut-filter", "value"))
def update_histogram(statut: str) -> go.Figure:
    df = load_data()
    mask = df["masse_g"] > 0
    if statut != "all":
        mask &= df["statut"] == statut
    data = df.loc[mask, "masse_g"].values
    log_data = np.log10(data[data > 0])
    color = {"Found": "#0EA5E9", "Fell": "#F59E0B"}.get(statut, "#38BDF8")
    fig = go.Figure(go.Histogram(
        x=log_data, marker_color=color, opacity=0.85,
        hovertemplate="log₁₀(masse) : %{x:.2f}<br>Nombre : %{y}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", xaxis_title="log₁₀(Masse en g)",
        yaxis_title="Nombre de météorites", showlegend=False,
        margin=dict(t=20, b=40, l=60, r=20),
    )
    return fig


@callback(Output("time-series", "figure"), Input("time-year-slider", "value"))
def update_timeseries(year_range: list) -> go.Figure:
    mask = (_by_year["annee"] >= year_range[0]) & (_by_year["annee"] <= year_range[1])
    sub = _by_year[mask]
    fig = go.Figure(go.Scatter(
        x=sub["annee"].values, y=sub["nombre"].values,
        mode="lines", fill="tozeroy",
        line=dict(color="#0EA5E9", width=2),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", showlegend=False,
        margin=dict(t=20, b=40, l=60, r=20),
    )
    return fig
