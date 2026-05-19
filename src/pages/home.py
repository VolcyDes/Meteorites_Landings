"""
home.py – Page d'accueil du dashboard.

Optimisations perf :
  - Figures pré-calculées une fois au chargement du module.
  - Données chargées via cache LRU (une seule lecture disque).
"""

import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_data, top_classes, format_number

# ── Chargement unique ──────────────────────────────────────────────────────
_df = load_data()

# ── Figures pré-calculées (une seule fois au démarrage) ───────────────────

def _build_pie() -> go.Figure:
    counts = _df["statut"].value_counts().reset_index()
    counts.columns = ["statut", "nombre"]
    fig = px.pie(
        counts, names="statut", values="nombre",
        color_discrete_sequence=["#0EA5E9", "#F59E0B"],
        hole=0.45,
    )
    fig.update_traces(textinfo="percent+label", textfont_color="#F1F5F9")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#F1F5F9",
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(font=dict(color="#94A3B8")),
    )
    return fig


def _build_bar_classes() -> go.Figure:
    tc = top_classes(n=10).sort_values("nombre")
    fig = px.bar(
        tc, x="nombre", y="classe", orientation="h",
        labels={"nombre": "Nombre", "classe": "Classe"},
        color="nombre",
        color_continuous_scale=["#0B1629", "#0EA5E9", "#F59E0B"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#F1F5F9",
        xaxis=dict(gridcolor="#2D1B69", title_font_color="#94A3B8"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", title_font_color="#94A3B8"),
        coloraxis_showscale=False,
        margin=dict(t=10, b=30, l=10, r=10),
    )
    return fig


# Figures calculées une seule fois
_FIG_PIE    = _build_pie()
_FIG_CLASSES = _build_bar_classes()


# ── Helper KPI ─────────────────────────────────────────────────────────────

def _kpi_card(value: str, label: str, color: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        style={"flex": "1", "minWidth": "140px"},
        children=[
            html.Div(value, className="kpi-value", style={"color": color}),
            html.Div(label, className="kpi-label"),
        ],
    )


# ── Layout ─────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """
    Construit et retourne le layout de la page d'accueil.
    Toutes les figures sont pré-calculées, pas de calcul à chaque visite.
    """
    total        = len(_df)
    avec_gps     = int(_df.dropna(subset=["latitude"]).shape[0])
    fell_count   = int((_df["statut"] == "Fell").sum())
    masse_max_kg = float(_df["masse_kg"].max())
    annee_active = int(_df.dropna(subset=["annee"]).groupby("annee").size().idxmax())

    kpis = [
        _kpi_card(format_number(total),       "Météorites recensées",       config.COLORS["accent"]),
        _kpi_card(format_number(avec_gps),    "Avec coordonnées GPS",       config.COLORS["primary_lt"]),
        _kpi_card(format_number(fell_count),  "Observées tomber (Fell)",    config.COLORS["success"]),
        _kpi_card(
            f"{masse_max_kg:,.0f} kg".replace(",", "\u202f"),
            "Masse max. (Hoba, Namibie)", config.COLORS["danger"]
        ),
        _kpi_card(str(annee_active), "Année la plus active", "#C084FC"),
    ]

    return html.Div([
        create_header(
            "Chutes de Météorites – Analyse Mondiale",
            "Exploration de 45 000+ météorites répertoriées par la Meteoritical Society "
            "et la NASA depuis l'an 860 jusqu'à aujourd'hui.",
        ),

        html.Div(className="page-content", children=[

            # KPIs
            html.Div(
                style={"display": "flex", "gap": "1rem", "flexWrap": "wrap", "marginBottom": "1.5rem"},
                children=kpis,
            ),

            # Graphiques
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "1fr 2fr", "gap": "1rem"},
                children=[
                    html.Div(className="graph-card", children=[
                        html.Div("Trouvées vs Observées", className="section-title"),
                        dcc.Graph(figure=_FIG_PIE,
                                  config={"displayModeBar": False},
                                  style={"height": "320px"}),
                    ]),
                    html.Div(className="graph-card", children=[
                        html.Div("Top 10 des classes de météorites", className="section-title"),
                        dcc.Graph(figure=_FIG_CLASSES,
                                  config={"displayModeBar": False},
                                  style={"height": "320px"}),
                    ]),
                ],
            ),

            # Encart info
            html.Div(
                style={
                    "background":   config.COLORS["bg_card"],
                    "border":       f"1px solid {config.COLORS['border']}",
                    "borderLeft":   f"4px solid {config.COLORS['accent']}",
                    "borderRadius": "8px",
                    "padding":      "1rem 1.5rem",
                    "marginTop":    "1rem",
                    "color":        config.COLORS["text_muted"],
                    "fontSize":     "0.9rem",
                    "lineHeight":   "1.7",
                },
                children=[
                    html.Strong("À propos : ", style={"color": config.COLORS["text"]}),
                    "Données issues de la ",
                    html.A("NASA Open Data Portal",
                           href="https://data.nasa.gov/dataset/meteorite-landings",
                           target="_blank", style={"color": config.COLORS["primary_lt"]}),
                    ". Naviguez vers la ",
                    html.Strong("Carte mondiale", style={"color": config.COLORS["accent"]}),
                    " pour la répartition géographique, ou vers les ",
                    html.Strong("Analyses", style={"color": config.COLORS["accent"]}),
                    " pour les statistiques détaillées.",
                ],
            ),
        ]),

        create_footer(),
    ])
