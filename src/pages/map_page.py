"""
map_page.py – Page Carte mondiale du dashboard.

Optimisations perf :
  - Données géo pré-chargées et échantillonnées (MAP_MAX_POINTS).
  - Filtres appliqués sur le sous-ensemble déjà en mémoire.
  - uirevision pour conserver le zoom/pan entre les updates.
"""

import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, callback, Input, Output

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_geo_data

# Données géo pré-chargées au démarrage (cache LRU)
_df_geo: pd.DataFrame = load_geo_data()

_YEAR_MIN = int(_df_geo["annee"].min(skipna=True))
_YEAR_MAX = int(_df_geo["annee"].max(skipna=True))

# Colorscale Deep Space : du bleu nuit au cyan puis à l'or stellaire
_COLORSCALE = [
    [0.0,  "#0B1629"],
    [0.4,  "#0EA5E9"],
    [0.75, "#F59E0B"],
    [1.0,  "#FCD34D"],
]


# ── Layout ─────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Construit le layout de la page carte."""
    return html.Div([
        create_header(
            "🗺️ Carte Mondiale des Météorites",
            f"Répartition géographique — {len(_df_geo):,} météorites géolocalisées.".replace(",", "\u202f"),
        ),

        html.Div(className="page-content", children=[

            # ── Filtres ───────────────────────────────────────────────────
            html.Div(className="graph-card", style={"marginBottom": "1rem"}, children=[
                html.Div("Filtres", className="section-title"),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "2fr 1fr 1fr", "gap": "1.5rem", "alignItems": "end"},
                    children=[
                        html.Div([
                            html.Label("Plage d'années",
                                       style={"color": config.COLORS["text_muted"], "fontSize": "0.85rem",
                                              "marginBottom": "0.5rem", "display": "block"}),
                            dcc.RangeSlider(
                                id="map-year-slider",
                                min=_YEAR_MIN, max=_YEAR_MAX,
                                value=[1800, _YEAR_MAX],
                                marks={y: {"label": str(y), "style": {"color": "#64748B", "fontSize": "0.75rem"}}
                                       for y in range(1800, _YEAR_MAX + 1, 50)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                step=1,
                                updatemode="mouseup",   # ← ne déclenche le callback qu'au relâché
                            ),
                        ]),
                        html.Div([
                            html.Label("Statut",
                                       style={"color": config.COLORS["text_muted"], "fontSize": "0.85rem",
                                              "marginBottom": "0.5rem", "display": "block"}),
                            dcc.Dropdown(
                                id="map-statut-filter",
                                options=[
                                    {"label": "Tous",               "value": "all"},
                                    {"label": "🔵 Trouvée (Found)", "value": "Found"},
                                    {"label": "🟣 Observée (Fell)", "value": "Fell"},
                                ],
                                value="all", clearable=False,
                                style={"backgroundColor": config.COLORS["bg_card2"], "color": "#0D0A1E"},
                            ),
                        ]),
                        html.Div([
                            html.Label("Catégorie de masse",
                                       style={"color": config.COLORS["text_muted"], "fontSize": "0.85rem",
                                              "marginBottom": "0.5rem", "display": "block"}),
                            dcc.Dropdown(
                                id="map-masse-filter",
                                options=[{"label": "Toutes", "value": "all"}] +
                                        [{"label": m, "value": m} for m in config.MASS_LABELS],
                                value="all", clearable=False,
                                style={"backgroundColor": config.COLORS["bg_card2"], "color": "#0D0A1E"},
                            ),
                        ]),
                    ],
                ),
                html.Div(id="map-count-label",
                         style={"color": config.COLORS["text_muted"], "fontSize": "0.82rem", "marginTop": "0.8rem"}),
            ]),

            # ── Carte ─────────────────────────────────────────────────────
            html.Div(className="graph-card", children=[
                dcc.Graph(
                    id="world-map",
                    config={"scrollZoom": True, "displayModeBar": True,
                            "modeBarButtonsToRemove": ["toImage", "select2d", "lasso2d"]},
                    style={"height": "580px"},
                ),
            ]),
        ]),
        create_footer(),
    ])


# ── Callback ───────────────────────────────────────────────────────────────

@callback(
    Output("world-map",        "figure"),
    Output("map-count-label",  "children"),
    Input("map-year-slider",   "value"),
    Input("map-statut-filter", "value"),
    Input("map-masse-filter",  "value"),
)
def update_map(year_range: list, statut: str, masse_cat: str) -> tuple:
    """
    Met à jour la carte en fonction des filtres.
    Utilise go.Scattergeo (plus léger que px.scatter_geo).

    Args:
        year_range: [année_min, année_max].
        statut:     'all', 'Found' ou 'Fell'.
        masse_cat:  Catégorie de masse ou 'all'.

    Returns:
        Tuple (figure Plotly, texte compteur).
    """
    df = _df_geo

    # Filtres vectorisés (opérations sur colonnes, sans copie inutile)
    mask = (df["annee"] >= year_range[0]) & (df["annee"] <= year_range[1])
    if statut != "all":
        mask &= df["statut"] == statut
    if masse_cat != "all":
        mask &= df["categorie_masse"] == masse_cat

    df = df[mask]
    count = len(df)

    layout_base = dict(
        paper_bgcolor=config.COLORS["bg_card"],
        plot_bgcolor=config.COLORS["bg_card"],
        font_color=config.COLORS["text"],
        margin=dict(t=0, b=0, l=0, r=0),
        uirevision="map",  # ← préserve le zoom/pan entre les updates
    )

    if count == 0:
        fig = go.Figure()
        fig.update_layout(
            **layout_base,
            annotations=[dict(text="Aucune météorite pour ces filtres.",
                              showarrow=False,
                              font=dict(size=16, color=config.COLORS["text_muted"]))],
        )
        return fig, "0 météorite"

    # Normalisation de la taille des marqueurs (log scale, plafonné)
    import numpy as np
    log_mass = np.log1p(df["masse_kg"].fillna(0).clip(lower=0).values)
    max_log  = log_mass.max() if log_mass.max() > 0 else 1
    marker_size = (log_mass / max_log * 14 + 3).clip(3, 18)

    fig = go.Figure(go.Scattergeo(
        lat=df["latitude"].values,
        lon=df["longitude"].values,
        mode="markers",
        marker=dict(
            size=marker_size,
            color=df["masse_kg"].values,
            colorscale=_COLORSCALE,
            cmax=float(df["masse_kg"].quantile(0.99)),
            cmin=0,
            opacity=0.8,
            line=dict(width=0),
            colorbar=dict(
                title="Masse (kg)",
                tickfont=dict(color=config.COLORS["text_muted"]),
                titlefont=dict(color=config.COLORS["text_muted"]),
                bgcolor=config.COLORS["bg_card"],
                bordercolor=config.COLORS["border"],
                thickness=12,
            ),
        ),
        text=df["nom"].values,
        customdata=df[["classe", "statut", "masse_kg", "annee"]].values,
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Classe : %{customdata[0]}<br>"
            "Statut : %{customdata[1]}<br>"
            "Masse  : %{customdata[2]:.3f} kg<br>"
            "Année  : %{customdata[3]}<extra></extra>"
        ),
    ))

    fig.update_layout(
        **layout_base,
        geo=dict(
            bgcolor=config.COLORS["bg_dark"],
            landcolor="#0F2040",
            oceancolor="#020817",
            showocean=True,
            showland=True,
            showcountries=True,
            countrycolor="#1E3A5F",
            showframe=False,
            coastlinecolor="#1E3A5F",
            projection_type="natural earth",
        ),
    )

    label = f"{count:,} météorite{'s' if count > 1 else ''} affichée{'s' if count > 1 else ''}".replace(",", "\u202f")
    return fig, label
