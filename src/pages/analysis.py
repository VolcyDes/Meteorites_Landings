"""
analysis.py – Page Analyses statistiques du dashboard.

Optimisations perf :
  - Figure catégorie de masse pré-calculée au chargement du module.
  - Callbacks histogramme et série temporelle optimisés (pas de .copy()).
  - Filtres vectorisés avec masques booléens.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_data, discoveries_by_year

# Données chargées une seule fois
_df      = load_data()
_by_year = discoveries_by_year()

_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=config.COLORS["text"],
    xaxis=dict(gridcolor="#1E3A5F", title_font_color=config.COLORS["text_muted"],
               tickfont=dict(color=config.COLORS["text_muted"])),
    yaxis=dict(gridcolor="#1E3A5F", title_font_color=config.COLORS["text_muted"],
               tickfont=dict(color=config.COLORS["text_muted"])),
    margin=dict(t=20, b=40, l=60, r=20),
    legend=dict(font=dict(color=config.COLORS["text_muted"]), bgcolor="rgba(0,0,0,0)"),
)


# ── Figure statique pré-calculée ───────────────────────────────────────────

def _build_masse_cat_fig() -> go.Figure:
    """Barres groupées par catégorie de masse et statut."""
    grp = (
        _df.groupby(["categorie_masse", "statut"], observed=True)
        .size()
        .reset_index(name="nombre")
    )
    cat_order = [c for c in config.MASS_LABELS if c in grp["categorie_masse"].values]
    grp["categorie_masse"] = pd.Categorical(grp["categorie_masse"],
                                            categories=cat_order, ordered=True)
    grp = grp.sort_values("categorie_masse")

    fig = px.bar(
        grp, x="categorie_masse", y="nombre", color="statut",
        barmode="group",
        color_discrete_map={"Found": "#0EA5E9", "Fell": "#F59E0B"},
        labels={"categorie_masse": "Catégorie de masse", "nombre": "Nombre", "statut": "Statut"},
    )
    fig.update_layout(**_LAYOUT)
    fig.update_layout(xaxis_tickangle=-20)
    return fig


_FIG_MASSE_CAT = _build_masse_cat_fig()

# Plage d'années pour le slider
_YEAR_MIN = int(_by_year["annee"].min())
_YEAR_MAX = int(_by_year["annee"].max())


# ── Layout ─────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Construit le layout de la page d'analyses statistiques."""
    return html.Div([
        create_header(
            "Analyses Statistiques",
            "Distribution des masses, évolution temporelle et répartition par catégorie.",
        ),

        html.Div(className="page-content", children=[

            # ── Histogramme des masses ─────────────────────────────────────
            html.Div(className="graph-card", children=[
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between",
                           "alignItems": "center", "marginBottom": "0.5rem"},
                    children=[
                        html.Div("Distribution des masses — échelle logarithmique",
                                 className="section-title", style={"marginBottom": 0}),
                        dcc.Dropdown(
                            id="hist-statut-filter",
                            options=[
                                {"label": "Tous",               "value": "all"},
                                {"label": "Trouvée (Found)",    "value": "Found"},
                                {"label": "Observée (Fell)",    "value": "Fell"},
                            ],
                            value="all", clearable=False,
                            style={"width": "200px",
                                   "backgroundColor": config.COLORS["bg_card2"],
                                   "color": "#0D0A1E", "fontSize": "0.85rem"},
                        ),
                    ],
                ),
                dcc.Graph(id="hist-masse",
                          config={"displayModeBar": False},
                          style={"height": "320px"}),
            ]),

            # ── Évolution temporelle ───────────────────────────────────────
            html.Div(className="graph-card", children=[
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between",
                           "alignItems": "center", "marginBottom": "0.5rem"},
                    children=[
                        html.Div("Évolution des découvertes par année",
                                 className="section-title", style={"marginBottom": 0}),
                        dcc.RangeSlider(
                            id="time-year-slider",
                            min=1800, max=_YEAR_MAX,
                            value=[1900, _YEAR_MAX],
                            marks={y: {"label": str(y),
                                       "style": {"color": "#64748B", "fontSize": "0.72rem"}}
                                   for y in range(1900, _YEAR_MAX + 1, 20)},
                            tooltip={"placement": "bottom", "always_visible": False},
                            step=1, allowCross=False,
                            updatemode="mouseup",  # déclenche seulement au relâché
                        ),
                    ],
                ),
                dcc.Graph(id="time-series",
                          config={"displayModeBar": False},
                          style={"height": "300px"}),
            ]),

            # ── Répartition par catégorie (statique) ──────────────────────
            html.Div(className="graph-card", children=[
                html.Div("Répartition par catégorie de masse et statut",
                         className="section-title"),
                dcc.Graph(figure=_FIG_MASSE_CAT,
                          config={"displayModeBar": False},
                          style={"height": "300px"}),
            ]),

        ]),
        create_footer(),
    ])


# ── Callbacks ─────────────────────────────────────────────────────────────

@callback(
    Output("hist-masse", "figure"),
    Input("hist-statut-filter", "value"),
)
def update_histogram(statut: str) -> go.Figure:
    """Met à jour l'histogramme des masses selon le filtre statut."""
    mask = _df["masse_g"] > 0
    if statut != "all":
        mask &= _df["statut"] == statut

    data = _df.loc[mask, "masse_g"].values

    color_map = {"Found": "#0EA5E9", "Fell": "#F59E0B", "all": "#38BDF8"}
    color = color_map.get(statut, "#38BDF8")

    # Bins log calculés une fois
    log_data = np.log10(data[data > 0])
    bins = np.linspace(log_data.min(), log_data.max(), 81)

    fig = go.Figure(go.Histogram(
        x=np.log10(data[data > 0]),
        xbins=dict(start=bins[0], end=bins[-1], size=(bins[-1]-bins[0])/80),
        marker_color=color,
        marker_line_color=config.COLORS["bg_dark"],
        marker_line_width=0.3,
        opacity=0.85,
        name=statut if statut != "all" else "Tous",
        hovertemplate="log₁₀(masse) : %{x:.2f}<br>Nombre : %{y}<extra></extra>",
    ))

    fig.update_layout(**_LAYOUT)
    fig.update_layout(
        xaxis_title="log₁₀(Masse en grammes)",
        yaxis_title="Nombre de météorites",
        yaxis_type="log",
        showlegend=False,
    )
    return fig


@callback(
    Output("time-series", "figure"),
    Input("time-year-slider", "value"),
)
def update_timeseries(year_range: list) -> go.Figure:
    """Met à jour la courbe temporelle selon la plage d'années."""
    mask = (_by_year["annee"] >= year_range[0]) & (_by_year["annee"] <= year_range[1])
    sub  = _by_year[mask]

    fig = go.Figure(go.Scatter(
        x=sub["annee"].values,
        y=sub["nombre"].values,
        mode="lines",
        fill="tozeroy",
        line=dict(color=config.COLORS["primary_lt"], width=2),
        fillcolor="rgba(14,165,233,0.12)",
        hovertemplate="<b>%{x}</b><br>%{y} météorite(s)<extra></extra>",
    ))

    fig.update_layout(**_LAYOUT)
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Découvertes",
        showlegend=False,
        uirevision="timeseries",
    )
    return fig
