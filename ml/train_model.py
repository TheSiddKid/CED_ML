from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "data" / "raw" / "owid_co2_data.csv"
SAMPLE_INPUT_PATH = ROOT / "data" / "processed" / "sample_input.csv"
MODELS_DIR = ROOT / "models"

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
TARGET_COLUMN = "co2"
UNIT = "million tonnes CO2"

NUMERIC_FEATURES = [
    "year",
    "population",
    "gdp",
    "cement_co2",
    "coal_co2",
    "oil_co2",
    "gas_co2",
    "flaring_co2",
]
CATEGORICAL_FEATURES = ["country"]


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run: python -m ml.download_dataset"
        )

    df = pd.read_csv(path)
    required = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    df = df[required].copy()
    df = df[df[TARGET_COLUMN].notna()].copy()
    df = df.dropna(subset=["country", "year"])
    df["year"] = df["year"].astype(int)
    return df


def chronological_split(df: pd.DataFrame, ratio: float = 0.8) -> tuple[pd.DataFrame, pd.DataFrame]:
    unique_years = sorted(df["year"].unique())
    split_index = int(len(unique_years) * ratio)
    split_index = max(1, min(split_index, len(unique_years) - 1))
    train_years = set(unique_years[:split_index])
    test_years = set(unique_years[split_index:])

    train_df = df[df["year"].isin(train_years)].copy()
    test_df = df[df["year"].isin(test_years)].copy()
    return train_df, test_df


def build_preprocessor() -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_dataset(RAW_DATA_PATH)
    train_df, test_df = chronological_split(df)

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[TARGET_COLUMN]
    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[TARGET_COLUMN]

    preprocessor = build_preprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=24,
        random_state=42,
        n_jobs=-1,
        min_samples_split=4,
        min_samples_leaf=2,
    )
    model.fit(X_train_transformed, y_train)

    preds = model.predict(X_test_transformed)

    mae = float(mean_absolute_error(y_test, preds))
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    r2 = float(r2_score(y_test, preds))

    metrics = {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "unit": UNIT,
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
    }

    feature_names = preprocessor.get_feature_names_out()
    fi_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    predictions_df = test_df[["country", "year", TARGET_COLUMN]].copy()
    predictions_df["predicted_co2"] = preds

    preprocessor_path = MODELS_DIR / "preprocessor.joblib"
    model_path = MODELS_DIR / "random_forest_model.joblib"
    metrics_path = MODELS_DIR / "metrics.json"
    importance_path = MODELS_DIR / "feature_importance.csv"
    prediction_eval_path = MODELS_DIR / "test_predictions.csv"
    metadata_path = MODELS_DIR / "metadata.json"

    joblib.dump(preprocessor, preprocessor_path)
    joblib.dump(model, model_path)

    fi_df.to_csv(importance_path, index=False)
    predictions_df.to_csv(prediction_eval_path, index=False)

    metadata = {
        "dataset_name": "Our World in Data CO2 and Greenhouse Gas Emissions",
        "dataset_url": "https://github.com/owid/co2-data",
        "dataset_file": str(RAW_DATA_PATH.relative_to(ROOT)),
        "trained_at_utc": datetime.utcnow().isoformat() + "Z",
        "features": FEATURE_COLUMNS,
        "target": TARGET_COLUMN,
        "target_unit": UNIT,
        "train_year_range": [int(train_df["year"].min()), int(train_df["year"].max())],
        "test_year_range": [int(test_df["year"].min()), int(test_df["year"].max())],
        "random_seed": 42,
    }

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    sample_input = X_test.head(20).copy()
    sample_input.to_csv(SAMPLE_INPUT_PATH, index=False)

    print("Training complete")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
