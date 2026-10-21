from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def compute_dashboard_data(df: pd.DataFrame, eval_df: pd.DataFrame) -> dict[str, Any]:
    usable = df[df["co2"].notna()].copy()

    trends = (
        usable.groupby("year", as_index=False)["co2"]
        .sum()
        .tail(25)
        .rename(columns={"co2": "total_co2"})
    )

    by_country = (
        usable.groupby("country", as_index=False)["co2"]
        .sum()
        .sort_values("co2", ascending=False)
        .head(12)
    )

    sectors = ["coal_co2", "oil_co2", "gas_co2", "cement_co2", "flaring_co2"]
    sector_values = []
    for col in sectors:
        if col in usable.columns:
            sector_values.append({"sector": col.replace("_co2", "").title(), "value": float(usable[col].fillna(0).sum())})

    actual_vs_pred = (
        eval_df.groupby("year", as_index=False)
        .agg(actual_co2=("co2", "mean"), predicted_co2=("predicted_co2", "mean"))
        .tail(15)
    )

    return {
        "summary": {
            "total_dataset_emissions": float(usable["co2"].sum()),
            "record_count": int(len(usable)),
            "countries": int(usable["country"].nunique()),
            "latest_year": int(usable["year"].max()),
            "average_test_prediction": float(eval_df["predicted_co2"].mean()),
        },
        "trends": trends.to_dict(orient="records"),
        "by_country": by_country.to_dict(orient="records"),
        "sectors": sector_values,
        "actual_vs_predicted": actual_vs_pred.to_dict(orient="records"),
    }


def filter_records(
    df: pd.DataFrame,
    country: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    category: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    filtered = df.copy()
    if country:
        filtered = filtered[filtered["country"] == country]
    if year_from:
        filtered = filtered[filtered["year"] >= year_from]
    if year_to:
        filtered = filtered[filtered["year"] <= year_to]

    columns = [
        "country",
        "year",
        "co2",
        "coal_co2",
        "oil_co2",
        "gas_co2",
        "cement_co2",
        "flaring_co2",
        "population",
        "gdp",
    ]

    if category and category in filtered.columns:
        columns = ["country", "year", category, "co2", "population", "gdp"]

    available = [c for c in columns if c in filtered.columns]
    out = filtered[available].fillna(np.nan).replace({np.nan: None}).head(limit)
    return out.to_dict(orient="records")
