"""
common_functions.py – Fonctions utilitaires partagées entre les pages.

Optimisations :
  - Données chargées une seule fois grâce à lru_cache (singleton pattern).
  - Agrégations pré-calculées au premier appel puis mises en cache.
"""

import os
import functools
import sqlite3
import pandas as pd

import config
from src.utils.clean_data import run_pipeline


@functools.lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """
    Charge le dataset nettoyé en mémoire une seule fois (cache LRU).

    Returns:
        DataFrame prêt à l'emploi pour les graphiques.
    """
    if os.path.exists(config.DB_FILE):
        conn = sqlite3.connect(config.DB_FILE)
        try:
            df = pd.read_sql_query("SELECT * FROM meteorites", conn)
            # Forcer les types pour éviter les inférences lentes
            df = df.astype({
                "nom":           "string",
                "classe":        "category",
                "statut":        "category",
                "type_nom":      "category",
                "categorie_masse": "category",
                "siecle":        "category",
            })
            return df
        finally:
            conn.close()
    return run_pipeline()


@functools.lru_cache(maxsize=1)
def load_geo_data() -> pd.DataFrame:
    """
    Retourne uniquement les météorites géolocalisées, échantillonnées
    pour garder MAP_MAX_POINTS points maximum sur la carte.

    Returns:
        DataFrame filtré et ordonné pour la carte.
    """
    df = load_data()
    df_geo = df.dropna(subset=["latitude", "longitude"]).copy()

    # Priorité aux météorites les plus massives pour l'échantillon
    df_geo = df_geo.sort_values("masse_g", ascending=False)

    # On garde toutes les "Fell" (rares, ~1 100) + le reste jusqu'à la limite
    fell = df_geo[df_geo["statut"] == "Fell"]
    found = df_geo[df_geo["statut"] == "Found"]

    remaining = config.MAP_MAX_POINTS - len(fell)
    if remaining > 0:
        found_sample = found.head(remaining)
    else:
        found_sample = pd.DataFrame(columns=df_geo.columns)

    return pd.concat([fell, found_sample], ignore_index=True)


@functools.lru_cache(maxsize=1)
def top_classes(n: int = 15) -> pd.DataFrame:
    """
    Retourne les n classes les plus représentées (résultat mis en cache).

    Args:
        n: Nombre de classes à retourner.

    Returns:
        DataFrame agrégé trié par nombre décroissant.
    """
    df = load_data()
    return (
        df.groupby("classe", observed=True)
        .agg(
            nombre=("nom", "count"),
            masse_moy_g=("masse_g", "mean"),
            masse_totale_kg=("masse_kg", "sum"),
        )
        .sort_values("nombre", ascending=False)
        .head(n)
        .reset_index()
    )


@functools.lru_cache(maxsize=1)
def discoveries_by_year() -> pd.DataFrame:
    """
    Agrège les découvertes par année (résultat mis en cache).

    Returns:
        DataFrame avec colonnes [annee, nombre, masse_moy_g].
    """
    df = load_data()
    return (
        df.dropna(subset=["annee"])
        .groupby("annee")
        .agg(nombre=("nom", "count"), masse_moy_g=("masse_g", "mean"))
        .reset_index()
        .sort_values("annee")
    )


def format_number(value: float, decimals: int = 0) -> str:
    """Formate un nombre avec séparateur de milliers (espace fine)."""
    fmt = f"{{:,.{decimals}f}}"
    return fmt.format(value).replace(",", "\u202f")
