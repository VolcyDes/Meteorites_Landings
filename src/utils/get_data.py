"""
get_data.py – Charge les données brutes depuis le CSV local dans data/raw/.
Si le fichier n'existe pas, indique à l'utilisateur de le placer.

Usage:
    python -m src.utils.get_data
"""

import os
import sys

# Ajout de la racine du projet au PYTHONPATH pour permettre l'import de config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd

import config


def fetch_raw_data(force: bool = False) -> str:
    """
    Point d'entrée principal : charge les données brutes depuis le CSV local.
    Si le fichier n'existe pas, lève une erreur.

    Args:
        force: Ignoré, gardé pour compatibilité.

    Returns:
        Chemin vers le fichier CSV brut chargé.

    Raises:
        FileNotFoundError: Si le fichier CSV n'existe pas.
    """
    dest = config.RAW_FILE

    if not os.path.exists(dest):
        raise FileNotFoundError(
            f"Fichier de données brutes introuvable : {dest}\n"
            "Placez le fichier 'Meteorite_Landings.csv' dans le dossier data/raw/."
        )

    print(f"Données brutes chargées depuis : {dest}")
    return dest


if __name__ == "__main__":
    fetch_raw_data()
