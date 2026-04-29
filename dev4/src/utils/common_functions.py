"""
common_functions.py – Fonctions utilitaires partagées entre les pages.
"""

import os
import sqlite3
import pandas as pd

import config
from src.utils.clean_data import run_pipeline


def load_data() -> pd.DataFrame:
    """Charge le dataset nettoyé depuis SQLite."""
    if os.path.exists(config.DB_FILE):
        conn = sqlite3.connect(config.DB_FILE)
        try:
            return pd.read_sql_query("SELECT * FROM meteorites", conn)
        finally:
            conn.close()
    return run_pipeline()


def top_classes(n: int = 15) -> pd.DataFrame:
    """Retourne les n classes les plus représentées."""
    df = load_data()
    return (
        df.groupby("classe", observed=True)
        .agg(nombre=("nom", "count"), masse_moy_g=("masse_g", "mean"))
        .sort_values("nombre", ascending=False)
        .head(n)
        .reset_index()
    )


def discoveries_by_year() -> pd.DataFrame:
    """Agrège les découvertes par année."""
    df = load_data()
    return (
        df.dropna(subset=["annee"])
        .groupby("annee")
        .agg(nombre=("nom", "count"), masse_moy_g=("masse_g", "mean"))
        .reset_index()
        .sort_values("annee")
    )


def format_number(value: float, decimals: int = 0) -> str:
    """Formate un nombre avec séparateur de milliers."""
    fmt = f"{{:,.{decimals}f}}"
    return fmt.format(value).replace(",", "\u202f")
