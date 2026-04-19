"""
home.py – Page d'accueil du dashboard (version initiale).
"""

import plotly.express as px
from dash import html, dcc

import config
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.common_functions import load_data, top_classes, format_number


def layout() -> html.Div:
    """Construit le layout de la page d'accueil."""
    df = load_data()
    total = len(df)
    avec_gps = int(df.dropna(subset=["latitude"]).shape[0])
    fell_count = int((df["statut"] == "Fell").sum())

    # Répartition Fell / Found
    counts = df["statut"].value_counts().reset_index()
    counts.columns = ["statut", "nombre"]
    fig_pie = px.pie(
        counts, names="statut", values="nombre",
        color_discrete_sequence=["#0EA5E9", "#F59E0B"],
        hole=0.4,
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", margin=dict(t=10, b=10, l=10, r=10),
    )

    # Top 10 classes
    tc = top_classes(n=10).sort_values("nombre")
    fig_bar = px.bar(
        tc, x="nombre", y="classe", orientation="h",
        color="nombre",
        color_continuous_scale=["#0B1629", "#0EA5E9", "#F59E0B"],
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", coloraxis_showscale=False,
        margin=dict(t=10, b=30, l=10, r=10),
    )

    return html.Div([
        create_header(
            "🌠 Chutes de Météorites – Analyse Mondiale",
            "Exploration de 45 000+ météorites répertoriées par la NASA.",
        ),
        html.Div(
            style={"padding": "1.5rem 2rem"},
            children=[
                # KPIs simples
                html.Div(
                    style={"display": "flex", "gap": "1rem", "marginBottom": "1.5rem"},
                    children=[
                        html.Div([html.H3(format_number(total), style={"color": "#F59E0B", "margin": 0}),
                                  html.P("Météorites recensées", style={"color": "#94A3B8", "margin": 0})],
                                 style={"background": "#0B1629", "border": "1px solid #333",
                                        "borderRadius": "8px", "padding": "1rem", "flex": "1"}),
                        html.Div([html.H3(format_number(avec_gps), style={"color": "#0EA5E9", "margin": 0}),
                                  html.P("Avec coordonnées GPS", style={"color": "#94A3B8", "margin": 0})],
                                 style={"background": "#0B1629", "border": "1px solid #333",
                                        "borderRadius": "8px", "padding": "1rem", "flex": "1"}),
                        html.Div([html.H3(format_number(fell_count), style={"color": "#10B981", "margin": 0}),
                                  html.P("Observées tomber (Fell)", style={"color": "#94A3B8", "margin": 0})],
                                 style={"background": "#0B1629", "border": "1px solid #333",
                                        "borderRadius": "8px", "padding": "1rem", "flex": "1"}),
                    ],
                ),
                # Graphiques
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 2fr", "gap": "1rem"},
                    children=[
                        html.Div([
                            html.H4("Trouvées vs Observées",
                                    style={"color": "#E2E8F0", "marginTop": 0}),
                            dcc.Graph(figure=fig_pie, config={"displayModeBar": False},
                                      style={"height": "300px"}),
                        ], style={"background": "#0B1629", "border": "1px solid #333",
                                  "borderRadius": "8px", "padding": "1rem"}),
                        html.Div([
                            html.H4("Top 10 des classes",
                                    style={"color": "#E2E8F0", "marginTop": 0}),
                            dcc.Graph(figure=fig_bar, config={"displayModeBar": False},
                                      style={"height": "300px"}),
                        ], style={"background": "#0B1629", "border": "1px solid #333",
                                  "borderRadius": "8px", "padding": "1rem"}),
                    ],
                ),
            ],
        ),
        create_footer(),
    ])
