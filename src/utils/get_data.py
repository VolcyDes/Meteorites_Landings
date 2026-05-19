"""
get_data.py – Récupère les données brutes depuis l'Open Data de la NASA.
Télécharge le fichier CSV et l'enregistre dans data/raw/.

Usage:
    python -m src.utils.get_data
"""

import os
import sys
import requests

# Ajout de la racine du projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config

def fetch_raw_data(force: bool = False) -> str:
    """
    Télécharge le CSV depuis l'URL de la NASA si nécessaire.

    Args:
        force: Si True, retélécharge le fichier même s'il existe déjà.

    Returns:
        Chemin vers le fichier CSV brut.
    """
    dest = config.RAW_FILE
    url = config.NASA_API_URL  # Utilise l'URL CSV définie dans config.py

    # 1. Vérifier si on doit télécharger
    if os.path.exists(dest) and not force:
        print(f"Le fichier existe déjà : {dest}")
        return dest

    # 2. Créer le dossier data/raw s'il n'existe pas
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    # 3. Téléchargement
    print("Téléchargement des données depuis la NASA...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Vérifie si le téléchargement a réussi

        with open(dest, "wb") as f:
            f.write(response.content)

        print(f"Téléchargement terminé : {dest}")
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        # Si le téléchargement échoue mais que le fichier existe, on continue
        if not os.path.exists(dest):
            raise e

    return dest

if __name__ == "__main__":
    fetch_raw_data(force=True) # On force pour tester le premier téléchargement
