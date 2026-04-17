"""
config.py – Centralise les paramètres de configuration du projet.
"""

import os

# ── Chemins ───────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR    = os.path.join(BASE_DIR, "data", "raw")
DATA_CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")

RAW_FILE     = os.path.join(DATA_RAW_DIR,     "Meteorite_Landings.csv")
CLEANED_FILE = os.path.join(DATA_CLEANED_DIR, "meteorites_clean.csv")
DB_FILE      = os.path.join(DATA_CLEANED_DIR, "meteorites.db")
# ── Source de données ─────────────────────────────────────────────────────────
# On utilise le lien direct vers le CSV fourni par la NASA
NASA_API_URL = "https://data.nasa.gov/docs/legacy/meteorite_landings/Meteorite_Landings.csv"

# ── Application ───────────────────────────────────────────────────────────
APP_TITLE = "Chutes de Météorites – Analyse Mondiale"
APP_HOST  = "127.0.0.1"
APP_PORT  = 8050
DEBUG     = True

# ── Catégories de masse ───────────────────────────────────────────────────
MASS_BINS   = [0, 10, 100, 1_000, 10_000, float("inf")]
MASS_LABELS = ["Micro (<10g)", "Petite (10–100g)", "Moyenne (0.1–1kg)",
               "Grande (1–10kg)", "Géante (>10kg)"]
