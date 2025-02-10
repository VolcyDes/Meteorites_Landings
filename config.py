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

# ── Application ───────────────────────────────────────────────────────────
APP_TITLE = "Chutes de Météorites – Analyse Mondiale"
APP_HOST  = "127.0.0.1"
APP_PORT  = 8050
DEBUG     = True
