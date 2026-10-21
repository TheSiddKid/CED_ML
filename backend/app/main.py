from __future__ import annotations

import io

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .data_service import compute_dashboard_data, filter_records
from .model_service import FEATURE_COLUMNS, ModelArtifacts, baseline_for_country, get_recommendations
from .schemas import PredictionInput, PredictionResponse

app = FastAPI(title="CED ML API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    artifacts = ModelArtifacts()
except Exception as exc:  # pragma: no cover
    artifacts = None
    startup_error = str(exc)
else:
    startup_error = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": artifacts is not None, "error": startup_error}


@app.get("/api/metrics")
def metrics() -> dict:
    if artifacts is None:
        raise HTTPException(status_code=503, detail=f"Model artifacts unavailable: {startup_error}")
    return {
        "metrics": artifacts.metrics,
        "metadata": artifacts.metadata,
        "feature_importance": artifacts.feature_importance.head(20).to_dict(orient="records"),
    }


@app.get("/api/options")
def options() -> dict:
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Model artifacts unavailable")
    df = artifacts.dataset
    return {
        "countries": sorted(df["country"].dropna().unique().tolist()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "categories": ["co2", "coal_co2", "oil_co2", "gas_co2", "cement_co2", "flaring_co2"],
    }


@app.get("/api/dashboard")
def dashboard() -> dict:
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Model artifacts unavailable")
    return {
        **compute_dashboard_data(artifacts.dataset, artifacts.eval_predictions),
        "metrics": artifacts.metrics,
        "feature_importance": artifacts.feature_importance.head(20).to_dict(orient="records"),
    }


@app.get("/api/records")
def records(
    country: str | None = None,
    year_from: int | None = Query(None, ge=1900, le=2100),
    year_to: int | None = Query(None, ge=1900, le=2100),
    category: str | None = None,
    limit: int = Query(200, ge=1, le=1000),
) -> dict:
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Model artifacts unavailable")

    items = filter_records(
        artifacts.dataset,
        country=country,
        year_from=year_from,
        year_to=year_to,
        category=category,
        limit=limit,
    )
    return {"records": items, "count": len(items)}


@app.post("/api/predict", response_model=PredictionResponse)
def predict(input_data: PredictionInput) -> PredictionResponse:
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Model artifacts unavailable")

    payload = input_data.model_dump()
    pred = artifacts.predict(payload)
    baseline = baseline_for_country(artifacts.dataset, payload["country"], payload["year"])
    comparison = None
    if baseline is not None and baseline != 0:
        comparison = ((pred - baseline) / abs(baseline)) * 100

    recommendations = get_recommendations(payload, pred)
    return PredictionResponse(
        predicted_co2=pred,
        unit=artifacts.metrics.get("unit", "million tonnes CO2"),
        baseline_co2=baseline,
        comparison_vs_baseline_pct=comparison,
        recommendations=recommendations,
    )


@app.post("/api/predict/batch")
async def predict_batch(file: UploadFile = File(...)) -> dict:
    if artifacts is None:
        raise HTTPException(status_code=503, detail="Model artifacts unavailable")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    try:
        frame = pd.read_csv(io.StringIO(content.decode("utf-8")))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {exc}") from exc

    missing = [col for col in FEATURE_COLUMNS if col not in frame.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"CSV missing required columns: {', '.join(missing)}",
        )

    inputs = frame[FEATURE_COLUMNS].copy()
    transformed = artifacts.preprocessor.transform(inputs)
    preds = artifacts.model.predict(transformed)

    output = frame.copy()
    output["predicted_co2"] = preds
    return {
        "count": int(len(output)),
        "unit": artifacts.metrics.get("unit", "million tonnes CO2"),
        "records": output.head(200).to_dict(orient="records"),
    }


@app.get("/api/recycling-methods")
def recycling_methods() -> dict:
    return {
        "disclaimer": "Educational module only. This application does not physically capture or recycle CO2.",
        "methods": [
            {
                "name": "Chemical Utilization",
                "how_it_works": "Captured CO2 is converted into fuels, chemicals, or polymers through catalytic or electrochemical routes.",
                "applications": "Methanol synthesis, urea production, synthetic fuels.",
                "benefits": "Can create marketable products and partially offset fossil carbon demand.",
                "limitations": "High energy requirements and catalyst costs; lifecycle benefits depend on clean energy use.",
                "reference": "Qin et al., Journal of CO2 Utilization (2022), DOI:10.1016/j.jcou.2022.102260",
            },
            {
                "name": "Biological Utilization",
                "how_it_works": "Microalgae or microbes assimilate CO2 into biomass and biochemical products.",
                "applications": "Biofuels, feed additives, bioplastics precursors.",
                "benefits": "Integrates with circular bioeconomy and can co-produce valuable compounds.",
                "limitations": "Scale-up complexity, land/water use constraints, and process stability challenges.",
                "reference": "Qin et al., Journal of CO2 Utilization (2022), DOI:10.1016/j.jcou.2022.102260",
            },
            {
                "name": "Mineralization",
                "how_it_works": "CO2 reacts with alkaline minerals or industrial residues to form stable carbonates.",
                "applications": "Construction aggregates, concrete curing, mine tailings treatment.",
                "benefits": "Provides durable carbon storage and potentially useful building materials.",
                "limitations": "Material transport, reaction kinetics, and site-specific economics.",
                "reference": "Qin et al., Journal of CO2 Utilization (2022), DOI:10.1016/j.jcou.2022.102260",
            },
            {
                "name": "Integrated Capture and Storage Pathways",
                "how_it_works": "CO2 is captured from point sources, purified, compressed, transported, and stored or used in downstream systems.",
                "applications": "Power, cement, steel, and industrial decarbonization programs.",
                "benefits": "Supports deep emissions mitigation where direct electrification is difficult.",
                "limitations": "Requires infrastructure, monitoring, and robust regulatory frameworks.",
                "reference": "Qin et al., Journal of CO2 Utilization (2022), DOI:10.1016/j.jcou.2022.102260",
            },
        ],
    }


@app.get("/api/research")
def research() -> dict:
    return {
        "papers": [
            {
                "title": "Research progress on CO₂ capture and utilization technology",
                "publication": "Journal of CO2 Utilization, 2022",
                "link": "https://doi.org/10.1016/j.jcou.2022.102260",
                "module_relation": "Informs capture/utilization/recycling educational module and comparison table.",
            },
            {
                "title": "A Scalable Explainable Deep Learning Framework for Predictive Analysis and Interpretability of CO₂ Emissions Patterns",
                "publication": "Scientific Reports, 2026",
                "link": "https://www.nature.com/articles/s41598-026-61829-4",
                "module_relation": "Guides framing of explainability and predictive analytics scope; implementation uses Random Forest for syllabus compliance.",
            },
            {
                "title": "Estimating Carbon Dioxide Emissions from Power Plant Water Vapor Plumes Using Satellite Imagery and Machine Learning",
                "publication": "Remote Sensing, 2024",
                "link": "https://www.mdpi.com/2072-4292/16/7/1290",
                "module_relation": "Motivates satellite-based future extension messaging and remote-sensing transparency notes.",
            },
        ],
        "notes": [
            "Primary implemented model is RandomForestRegressor from scikit-learn to align with syllabus requirements.",
            "Feature importance is used as an interpretability aid and not as proof of causation.",
            "Satellite plume estimation is marked as future work unless validated plume datasets are integrated.",
        ],
    }
