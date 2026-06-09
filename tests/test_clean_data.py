"""
test_clean_data.py – Tests unitaires pour le module clean_data.

Vérifie les étapes de nettoyage : renommage, types, filtrage et colonnes dérivées.
"""

import sys
import os
import pandas as pd
import pytest

# Ajoute la racine du projet au PYTHONPATH pour permettre l'import de config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.clean_data import clean


# ── Fixture ─────────────────────────────────────────────────────────────────

@pytest.fixture
def raw_sample() -> pd.DataFrame:
    """Retourne un petit DataFrame au format brut NASA pour les tests."""
    return pd.DataFrame({
        "name":        ["Hoba", "Canyon Diablo", "Sikhote-Alin", "Bad Entry", "Future"],
        "id":          [1, 2, 3, 4, 5],
        "nametype":    ["Valid", "Valid", "Valid", "Valid", "Valid"],
        "recclass":    ["Iron, IAB", "Iron, IAB", "Iron, IIAB", "L5", "H6"],
        "mass (g)":    [60_000_000, 450_000, 23_000, None, 500],
        "fall":        ["Found", "Found", "Fell", "Found", "Found"],
        "year":        [1920.0, 1891.0, 1947.0, 1800.0, 2030.0],
        "reclat":      [-19.583, 35.033, 46.117, 0.0, 0.0],
        "reclong":     [17.917, -111.017, 134.65, 0.0, 0.0],
        "GeoLocation": ["(-19.583, 17.917)", "(35.033, -111.017)", "(46.117, 134.65)", None, None],
    })


# ── Tests ────────────────────────────────────────────────────────────────────

class TestRenommage:
    """Vérifie que les colonnes sont correctement renommées."""

    def test_colonne_nom(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "nom" in df.columns, "La colonne 'name' doit être renommée en 'nom'"

    def test_colonne_masse_g(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "masse_g" in df.columns

    def test_colonne_statut(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "statut" in df.columns

    def test_colonne_annee(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "annee" in df.columns


class TestFiltrage:
    """Vérifie les règles de filtrage (lignes supprimées)."""

    def test_supprime_sans_masse(self, raw_sample: pd.DataFrame) -> None:
        """La ligne avec masse NaN doit être supprimée."""
        df = clean(raw_sample)
        assert df["masse_g"].isna().sum() == 0

    def test_supprime_annee_future(self, raw_sample: pd.DataFrame) -> None:
        """Les météorites avec année > 2025 doivent être supprimées."""
        df = clean(raw_sample)
        annees_valides = df["annee"].dropna()
        assert (annees_valides > 2025).sum() == 0


class TestColonnesDerivees:
    """Vérifie les colonnes calculées."""

    def test_masse_kg_presence(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "masse_kg" in df.columns

    def test_masse_kg_valeur(self, raw_sample: pd.DataFrame) -> None:
        """masse_kg doit valoir masse_g / 1000."""
        df = clean(raw_sample)
        hoba = df[df["nom"] == "Hoba"].iloc[0]
        assert abs(hoba["masse_kg"] - 60_000.0) < 0.01

    def test_categorie_masse_presence(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "categorie_masse" in df.columns

    def test_siecle_presence(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert "siecle" in df.columns

    def test_siecle_valeur(self, raw_sample: pd.DataFrame) -> None:
        """Hoba découverte en 1920 → 20e siècle."""
        df = clean(raw_sample)
        hoba = df[df["nom"] == "Hoba"].iloc[0]
        assert hoba["siecle"] == "20e siècle"


class TestTypes:
    """Vérifie les types de données après nettoyage."""

    def test_type_annee(self, raw_sample: pd.DataFrame) -> None:
        """L'année doit être de type entier nullable."""
        df = clean(raw_sample)
        assert str(df["annee"].dtype) == "Int64"

    def test_type_masse_g(self, raw_sample: pd.DataFrame) -> None:
        df = clean(raw_sample)
        assert pd.api.types.is_float_dtype(df["masse_g"])
