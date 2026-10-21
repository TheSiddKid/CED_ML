from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"
DATASET_PATH = ROOT / "data" / "raw" / "owid_co2_data.csv"

FEATURE_COLUMNS = [
    "country",
    "year",
    "population",
    "gdp",
    "cement_co2",
    "coal_co2",
    "oil_co2",
    "gas_co2",
    "flaring_co2",
]


class ModelArtifacts:
    def __init__(self) -> None:
        self.preprocessor = joblib.load(MODELS_DIR / "preprocessor.joblib")
        self.model = joblib.load(MODELS_DIR / "random_forest_model.joblib")
        self.metrics = self._read_json("metrics.json")
        self.metadata = self._read_json("metadata.json")
        self.feature_importance = pd.read_csv(MODELS_DIR / "feature_importance.csv")
        self.eval_predictions = pd.read_csv(MODELS_DIR / "test_predictions.csv")
        self.dataset = pd.read_csv(DATASET_PATH)

    def _read_json(self, file_name: str) -> dict:
        with (MODELS_DIR / file_name).open("r", encoding="utf-8") as f:
            return json.load(f)

    def predict(self, payload: dict) -> float:
        frame = pd.DataFrame([payload], columns=FEATURE_COLUMNS)
        transformed = self.preprocessor.transform(frame)
        pred = self.model.predict(transformed)[0]
        return float(pred)


def get_recommendations(row: dict, predicted: float) -> list[str]:
    suggestions: list[str] = []

    if row.get("coal_co2", 0) and row["coal_co2"] > max(row.get("gas_co2", 0), row.get("oil_co2", 0)):
        suggestions.append(
            "Prioritize coal-to-renewables transition and boiler efficiency upgrades for high coal-linked emissions."
        )
    if row.get("oil_co2", 0) and row["oil_co2"] > 50:
        suggestions.append(
            "Improve fuel switching and logistics optimization to reduce oil-related combustion demand."
        )
    if row.get("cement_co2", 0) and row["cement_co2"] > 20:
        suggestions.append(
            "For cement-heavy profiles, evaluate clinker substitution and carbon-cured concrete pathways."
        )
    if predicted > 500:
        suggestions.append(
            "High predicted emissions indicate a need for phased carbon-capture feasibility assessment and energy-intensity audits."
        )

    suggestions.append(
        "Track reductions against yearly baselines and verify with direct measurement or validated remote-sensing methods where possible."
    )
    return suggestions


def baseline_for_country(df: pd.DataFrame, country: str, year: int) -> float | None:
    country_df = df[(df["country"] == country) & (df["year"] < year) & (df["co2"].notna())]
    if country_df.empty:
        return None
    return float(country_df.sort_values("year").tail(1)["co2"].iloc[0])
