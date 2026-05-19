"""
config.py – Centralise tous les paramètres de configuration du projet.
"""

import os

# ── Chemins ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")

RAW_FILE = os.path.join(DATA_RAW_DIR, "Meteorite_Landings.csv")
CLEANED_FILE = os.path.join(DATA_CLEANED_DIR, "meteorites_clean.csv")
DB_FILE = os.path.join(DATA_CLEANED_DIR, "meteorites.db")

# ── Source de données ─────────────────────────────────────────────────────────
# On utilise le lien direct vers le CSV fourni par la NASA
NASA_API_URL = "https://data.nasa.gov/docs/legacy/meteorite_landings/Meteorite_Landings.csv"

# ── Application ───────────────────────────────────────────────────────────────
APP_TITLE = "Chutes de Météorites – Analyse Mondiale"
APP_HOST = "127.0.0.1"
APP_PORT = 8050
DEBUG = False

# ── Palette Deep Space ────────────────────────────────────────────────────────
# Inspiré des images Hubble : fond espace profond, cyan nébuleuse, or stellaire
COLORS = {
    "bg_dark":    "#020817",   # noir espace quasi-total
    "bg_card":    "#0B1629",   # bleu nuit profond
    "bg_card2":   "#0F2040",   # bleu marine
    "primary":    "#0EA5E9",   # cyan clair – nébuleuse
    "primary_lt": "#38BDF8",   # cyan lumineux
    "accent":     "#F59E0B",   # or ambré – étoile
    "accent_lt":  "#FCD34D",   # or pâle
    "text":       "#E2E8F0",   # blanc cassé très lisible
    "text_muted": "#94A3B8",   # gris bleuté
    "border":     "#1E3A5F",   # bleu ardoise
    "success":    "#10B981",   # vert émeraude
    "danger":     "#F43F5E",   # rouge
}

# ── Performances ──────────────────────────────────────────────────────────────
# Nombre max de points affichés sur la carte (pour fluidité)
MAP_MAX_POINTS = 6_000

# ── Catégories de masse ───────────────────────────────────────────────────────
MASS_BINS   = [0, 10, 100, 1_000, 10_000, float("inf")]
MASS_LABELS = ["Micro (<10g)", "Petite (10–100g)", "Moyenne (0.1–1kg)",
               "Grande (1–10kg)", "Géante (>10kg)"]
