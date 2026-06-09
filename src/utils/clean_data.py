"""
clean_data.py – Nettoie et enrichit les données brutes de météorites.
Stocke le résultat dans data/cleaned/ (Format SQLite et CSV).

Usage:
    python -m src.utils.clean_data
"""

import os
import sys
import sqlite3
import pandas as pd

# Ajout de la racine du projet au PYTHONPATH pour permettre l'import de config
# Cela évite l'erreur "ModuleNotFoundError: No module named 'config'"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from src.utils.get_data import fetch_raw_data

def load_raw(path: str) -> pd.DataFrame:
    """Charge le CSV brut depuis le chemin fourni."""
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique toutes les étapes de nettoyage sur le DataFrame brut.
    """
    # 1. Renommage des colonnes
    df = df.rename(columns={
        "name":      "nom",
        "id":        "id",
        "nametype":  "type_nom",
        "recclass":  "classe",
        "mass (g)":  "masse_g",
        "fall":      "statut",
        "year":      "annee",
        "reclat":    "latitude",
        "reclong":   "longitude",
        "GeoLocation": "geolocation",
    })

    # 2. Conversion des types
    df["masse_g"] = pd.to_numeric(df["masse_g"], errors="coerce")
    df["annee"]   = pd.to_numeric(df["annee"],   errors="coerce")

    # 3. Suppression des lignes inutilisables (sans masse)
    df = df.dropna(subset=["masse_g"]).copy()

    # 4. Filtrage des années aberrantes
    df = df[(df["annee"] >= 860) | df["annee"].isna()].copy()
    df = df[df["annee"] <= 2025].copy()
    df["annee"] = df["annee"].astype("Int64")

    # 5. Colonnes dérivées
    df["masse_kg"] = (df["masse_g"] / 1000).round(4)

    df["categorie_masse"] = pd.cut(
        df["masse_g"],
        bins=config.MASS_BINS,
        labels=config.MASS_LABELS,
        right=False,
    ).astype(str)

    df["siecle"] = df["annee"].apply(
        lambda y: f"{int((y - 1) // 100 + 1)}e siècle" if pd.notna(y) else "Inconnu"
    )

    return df.reset_index(drop=True)


def save_cleaned(df_raw: pd.DataFrame, df_clean: pd.DataFrame, db_path: str, csv_path: str) -> None:
    """
    Sauvegarde les données brutes ET nettoyées dans SQLite, plus un CSV nettoyé.

    Args:
        df_raw:   DataFrame brut (table ``raw``).
        df_clean: DataFrame nettoyé (table ``cleaned``).
        db_path:  Chemin vers la base SQLite.
        csv_path: Chemin vers le CSV nettoyé.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        # Table raw : données brutes sans modification
        df_raw.to_sql("raw", conn, if_exists="replace", index=False)
        # Table cleaned : données nettoyées et enrichies
        df_clean.to_sql("cleaned", conn, if_exists="replace", index=False)
        print(f" Base SQLite mise à jour : {db_path} (tables 'raw' et 'cleaned')")
    finally:
        conn.close()

    df_clean.to_csv(csv_path, index=False, encoding="utf-8")
    print(f" Fichier CSV généré : {csv_path}")
    print(f" Total : {len(df_clean):,} lignes nettoyées.")


def run_pipeline() -> pd.DataFrame:
    """Lance le pipeline complet : téléchargement → nettoyage → double sauvegarde."""

    # 1. ÉTAPE NOUVELLE : On déclenche le téléchargement si nécessaire
    print(" Vérification/Téléchargement des données brutes en cours...")
    fetch_raw_data()

    # 2. Récupération des chemins
    raw_path     = config.RAW_FILE
    db_path      = config.DB_FILE
    csv_path     = config.CLEANED_FILE

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Fichier brut introuvable : {raw_path}")

    print(" Démarrage du pipeline de nettoyage...")
    df_raw = load_raw(raw_path)
    df_clean = clean(df_raw)

    save_cleaned(df_raw, df_clean, db_path, csv_path)
    return df_clean


if __name__ == "__main__":
    run_pipeline()